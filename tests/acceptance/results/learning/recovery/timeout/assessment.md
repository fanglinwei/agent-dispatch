# 恢复脚本超时处理验收

审查发现 `invoke()` 的 `communicate(timeout=20)` 抛出异常后，`Popen` 上下文退出仍会无限等待子进程。现于超时分支终止直接子进程，再次通信以回收进程和收集剩余输出，将完整输出附回原 `TimeoutExpired` 后重新抛出。超时路径不进入 JSON 成功结果处理。

主代理在隔离临时目录实际运行 `python3 -B tests/acceptance/test_recovery_timeout.py --report <报告路径>`。该标准库测试调用真实 `invoke()`，仅替换子进程工作内容并将通信超时缩至 0.05 秒：真实 Python 子进程先输出 `{"status":"saved"}` 和错误诊断、写就绪标记，再睡眠 2 秒。就绪后才开始通信，防止只验证了尚未启动的进程。POSIX 下额外通过 `waitpid` 确认子进程已回收。

| 实际运行 | 结果 | 调用耗时 | kill 次数 | 子进程退出码 | 输出与失败 |
| --- | --- | --- | --- | --- | --- |
| 修改前，同一测试 | FAIL，测试退出 1 | 2.042 秒 | 0 | 0，自行结束 | 传播超时但等待自然退出；kill 断言失败 |
| 修改后，同一测试 | PASS，测试退出 0 | 0.079 秒 | 1 | -9 | 两路输出完整保留，继续抛出 TimeoutExpired |

原始结果见 `red.json`、`green.json`，两者测试源码指纹相同。`prior-recovery-harness.py` 保留修复前脚本以核对 RED 指纹；GREEN 指纹对应当前脚本。测试要求调用少于 1.5 秒且进程非零退出并被回收。看似成功的 JSON 不会使调用成功。生产超时仍为 20 秒；缩短时间仅用于本回归。

随后在新的空临时目录实际运行 `python3 -B tests/acceptance/recovery-harness.py <空临时目录> <results/learning/fixes 的绝对路径>`，三组可写恢复、三组只读接手、五组两步归档故障恢复及 NFC 路径拒绝全部通过，包括 22 次恢复/重试进程调用。实际结果导出至上级 `replay.json`，各场景完整快照与前轮逐字相同，只有本轮时间、进程 ID 与脚本指纹更新；没有仅改哈希代替执行。上级 `probes.json` 仍为重新执行的十四组探针结果。

`prior-replay.json` 保存本轮前完整总清单，`prior-recovery-replay.json` 与 `prior-recovery-assessment.md` 保存前轮恢复记录。新增 Node 离线断言核对 RED/GREEN、源码指纹、终止、回收、耗时、诊断与异常；`npm test` 仍不启动 Python 或模型。

本轮由主代理执行与核对，没有新独立审查或模型调用。修改范围为验收工具、回归与说明；生产 Skill、保存函数及角色配置未改。全部写入隔离测试目录，授权仍为模拟；没有 Git 写操作。这验证直接子进程的超时清理，不扩展为后代进程树、断电、生产运行或跨文件事务保证。
