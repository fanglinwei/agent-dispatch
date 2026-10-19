"""Live stdlib regression; run explicitly, not as part of offline npm test."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


OBSERVATIONS = {}
HARNESS = Path(__file__).with_name('recovery-harness.py')


class RecoveryTimeoutTest(unittest.TestCase):
    def test_timeout_kills_and_reaps_child_before_propagating_failure(self):
        namespace = runpy.run_path(str(HARNESS))
        real_popen = subprocess.Popen
        children = []
        with tempfile.TemporaryDirectory(prefix='recovery-timeout-') as directory:
            base = Path(directory)
            ready = base / 'ready'
            source = ('import pathlib, time\n'
                      'print(\'{"status":"saved"}\', flush=True)\n'
                      'import sys; print("child waiting", file=sys.stderr, flush=True)\n'
                      f'pathlib.Path({str(ready)!r}).write_text("ready")\n'
                      'time.sleep(2)\n')

            class HangingChild(real_popen):
                def __init__(self, command, **kwargs):
                    super().__init__([sys.executable, '-u', '-c', source], **kwargs)
                    self.kill_calls = 0
                    children.append(self)
                    deadline = time.monotonic() + 5
                    while not ready.exists():
                        if self.poll() is not None or time.monotonic() >= deadline:
                            self.kill()
                            self.communicate()
                            raise AssertionError('test child did not become ready')
                        time.sleep(0.005)

                def communicate(self, input=None, timeout=None):
                    return super().communicate(input=input, timeout=0.05 if timeout is not None else None)

                def kill(self):
                    self.kill_calls += 1
                    return super().kill()

            started = time.monotonic()
            with patch.object(subprocess, 'Popen', HangingChild):
                with self.assertRaises(subprocess.TimeoutExpired) as caught:
                    namespace['invoke'](base, base, base / 'request.json')
            elapsed = time.monotonic() - started
            child = children[0]
            error = caught.exception
            reaped = child.returncode is not None
            if os.name == 'posix':
                try:
                    os.waitpid(child.pid, os.WNOHANG)
                except ChildProcessError:
                    pass
                else:
                    reaped = False
            OBSERVATIONS.update({'elapsedSeconds': elapsed, 'upperBoundSeconds': 1.5,
                                 'communicationTimeoutSeconds': error.timeout,
                                 'killCalls': child.kill_calls, 'childReturnCode': child.returncode,
                                 'reaped': reaped, 'exception': type(error).__name__,
                                 'stdout': error.output.decode() if isinstance(error.output, bytes) else error.output,
                                 'stderr': error.stderr.decode() if isinstance(error.stderr, bytes) else error.stderr})
            self.assertEqual(child.kill_calls, 1)
            self.assertIsNotNone(child.returncode)
            self.assertNotEqual(child.returncode, 0)
            self.assertTrue(reaped)
            self.assertLess(elapsed, 1.5, 'waited for the child to exit naturally')
            self.assertEqual(error.output, '{"status":"saved"}\n')
            self.assertEqual(error.stderr, 'child waiting\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    outcome = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(RecoveryTimeoutTest))
    if args.report:
        args.report.write_text(json.dumps({'outcome': 'PASS' if outcome.wasSuccessful() else 'FAIL',
                                          'harnessSha256': hashlib.sha256(HARNESS.read_bytes()).hexdigest(),
                                          'testSha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                          'checks': OBSERVATIONS}, indent=2) + '\n')
    sys.exit(0 if outcome.wasSuccessful() else 1)
