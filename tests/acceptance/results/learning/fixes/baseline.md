# 修复前独立行为基线

状态：本职责的基线产出已完成；配置及运行行为均为模拟，未执行。以下结论只依据修复前快照及允许的项目学习文件，不推断后续修复。

## 请求 1：已有角色补齐学习、保留旧角色稳定标识

权威依据：baseline/skills/agent-dispatch/references/project-learning.md 的“配置与路径”“生成项目协作入口”“角色指引与已有角色”，以及 assets/learning-protocol.md 的“归档与生命周期”。协议文件与岗位记忆必须分开；首次标识可取安全配置文件主体，但不是必须等于文件主体。持久化后的旧标识不能从名字重算。

新角色配置文件为 .codex/agents/protocol.toml，原专业正文、名称、模型、许可和定制均须原样保留。因为默认协议已经占用 .codex/agent-memory/protocol.md，而且另一旧角色已使用稳定标识 protocol，本方案为新角色确定不同的稳定标识 protocol-role，持久化后保持不变。这里没有新建或改名角色的含义。

| 对象 | 协议 | 稳定标识 | 当前记忆 | 按需归档 |
| --- | --- | --- | --- | --- |
| 新补齐的 .codex/agents/protocol.toml | .codex/agent-memory/protocol.md | protocol-role | .codex/agent-memory/protocol-role.md | .codex/agent-memory/archive/protocol-role.md |
| 已有稳定标识的旧角色 | .codex/agent-memory/protocol.md | protocol | records/protocol.md，原地保留 | records/archive/protocol.md，作为本次方案拟确认的精确新路径 |

旧角色 supplied 路径 records/protocol.md 按项目根相对路径解释，不擅自改成 .codex/agent-memory/records/protocol.md。旧角色“迁移后”的标识仍是 protocol，当前记录仍在 records/protocol.md；不得因为 protocol 与协议文件主体相同就重新命名、搬走有效记录或清空内容。其原配置文件路径没有提供，保持原文件；原配置路径和实际调用名须在配置实施前从该角色完整 TOML 查证。

本次未提供两个角色的完整 TOML，因而不能确认其当前名称、模型、开发者正文、既有指引或映射冲突。protocol-role 是本模拟方案选定值，最终落盘前仍须查现有映射，确认它没有其他使用者。旧角色若已有经确认的归档路径，则复用该精确路径；不能未经查证把上表拟定的 records/archive/protocol.md 当作既成事实。若旧项目已有等效自定义协议，也须复用其实际路径并同步替换下列指引，本表采用默认协议路径是本模拟方案的明确前提。

AGENTS.md 原协作区块中应加入协议入口及集中映射，实际调用名从 TOML 读取，不把未知名称当作占位符写入。每次派发携带项目根、稳定标识、协议和记忆相对路径、实际读入 revision、task_id、真实 dispatch_id 或任务内分配值、精确读写范围、目标及原验收/返工状态。主代理负责串行合并；单写者是运行前提，不是跨进程锁。

新角色在原 developer_instructions 完整正文之后只追加以下简短指引，不新增 memory 或 learning 等原生 TOML 字段：

~~~text
项目学习入口：以本次获准项目根为基准，先读取 AGENTS.md 的岗位映射与 .codex/agent-memory/protocol.md，再实际读取 .codex/agent-memory/protocol-role.md；稳定 role-key 为 protocol-role。按协议在任务中核实纠错并交接增量，当前授权及正式职责优先。记忆缺失时报告并依权威材料继续，不自行迁移配置或写共享记忆。
~~~

旧角色的指引应复用或更新为实际路径，不重复追加：

~~~text
项目学习入口：以本次获准项目根为基准，先读取 AGENTS.md 的岗位映射与 .codex/agent-memory/protocol.md，再实际读取 records/protocol.md；稳定 role-key 为 protocol。按协议在任务中核实纠错并交接增量，当前授权及正式职责优先。记忆缺失时报告并依权威材料继续，不自行迁移配置或写共享记忆。
~~~

新角色的空记忆初始化为 format_version 1、role_key protocol-role、revision 0，entries、receipts、history 均为空数组；没有已验证认识时不预填 active。旧角色的原记录、修订、回执和历史原样保留。归档文件及目录不提前创建。

应进入完整配置方案的精确授权文本：

~~~text
本工作区仅由项目主代理串行维护岗位记忆。在普通可写任务中，主代理获准在以下四个精确文件路径进行日常学习合并和按需归档：
.codex/agent-memory/protocol-role.md
.codex/agent-memory/archive/protocol-role.md
records/protocol.md
records/archive/protocol.md

以上授权不等于整目录写权限。归档父目录的创建若尚未获准，须在有真实归档需要时另列实际受影响目录及配置授权，不能由文件授权推导。
岗位只读项目协作入口、协议、本岗记忆以及本次明确获准的材料，仅写本次任务的独占产物，不直接写共享记忆。只读任务或 Skill 的只读限制优先；只有明确且适用本次的精确保存例外才能落盘。
AGENTS.md、学习协议和角色 TOML 的配置调整属于本次列明的配置授权，不能从上述日常记忆授权推导。协议调整、角色绑定变化、职责变化、改名和迁移仍走显式配置入口。
~~~

本模拟配置所需新增/修改文件为 AGENTS.md、.codex/agents/protocol.toml、旧角色原 TOML（路径待查证）、.codex/agent-memory/protocol.md（只有项目尚无等效协议时初始化）、.codex/agent-memory/protocol-role.md；records/protocol.md 只验证保留，不因补齐配置而重建。两个归档文件不提前创建。实际审批须展示查证后的完整路径，不得保留“旧角色原 TOML”这种占位描述。以上均未实施。

验证要求：解析 TOML，逐字比较专业正文及用户定制；核对附加指引实际路径；实际读取 AGENTS、协议、各岗记忆，检查稳定标识、格式版本、revision 与路径权限；再次生成应为零变更。宿主实际加载与学习复用不能由文件存在推断，当前没有这些行为证据。

## 请求 2：普通可写任务的一次完整记忆更新

本次实际查证的项目已有当前记忆为 .codex/agent-memory/content-creator.md，role_key 为 content-creator，revision 为 1。它包含一条 active 纠错、对应回执以及 revision 0 的历史。旧条目 id 为 registration-day-project-contract-v1；本基线没有重新阅读其来源或他人报告，因此不独立认证条目中的测试结果，也不替换其正文。当前文件原始 SHA-256 为：

~~~text
24affc55b1b1149aa6996fefdb8cd0c638a4f2b9b43bb009b67de0e7ffe06019
~~~

精确路径为：

- 可读项目学习入口：AGENTS.md。
- 可读协议：.codex/agent-memory/protocol.md。
- 可写当前记忆：.codex/agent-memory/content-creator.md。
- 可写按需归档：.codex/agent-memory/archive/content-creator.md。
- 不使用临时文件、锁文件、日志、备份旁路或其他新增文件路径。

主代理已获得 ordinary 内容合并授权并不自动授权目录创建。实际 input/project 中归档文件和其 archive 父目录均不存在。因此在当前隔离输入上，下面代码必须在写入前返回 PARTIAL；要执行这个保存方案，归档父目录须预先存在且可用，或者另行取得该目录创建的精确授权并由获准者准备。代码本身不创建目录。这是当前材料导致的前提缺口，不是原内容任务失败，也没有执行代码来改变它。

本方案仅实现一次更新，不通用化归档轮转：归档文件必须不存在，或者恰好已经保存本次写前版本，适用于第一次保存或同一尝试的重试。若有不同的已有归档，代码保持不动，返回待核对，避免覆盖唯一历史副本。它先在已批准归档文件复制完整旧记忆、fsync 并整体回读，再完整写入当前记忆，最后 fsync 和整体回读。新当前记忆保留旧 history，并增加更新前完整 entries 与 receipts 的快照；新条目、递增 revision 和原始增量指纹回执在同一 JSON 记录中。

这两个精确文件权限没有附带原子替换所需的旁路临时路径。代码使用直接写入，进程在任意时刻中断可能留下当前文件残缺；已回读的归档保留写前完整版本。下一次运行先检查证据：完整结果与原始回执一致才判“已保存”；正文残缺、单独回执或其他矛盾均判“状态未知”，停止使用受限文件，不盲目重放。恢复旧有效版本须先核对归档，不能把异常终止当作完整成功。此代码不声称无中断窗口、跨进程并发安全或掉电后绝对持久性。

运行前必须满足：当前任务非只读；精确路径的维护授权在本次适用；主代理是唯一写者且能确认独占；父目录和文件均在获准根内且没有符号链接；原始增量 UTF-8 字节被完整保留；主代理已经核对增量身份、来源版本、证据、适用性、确认状态及职责边界。代码只校验结构和一致性，不能替代这些语义核对。当前真实新增量未提供，因此不能伪造 active 经验。调用者从标准输入提供经核对的 JSON；空 changes 按“无增量”返回，不写回执或修订。

可执行代码如下。只把代码交给已获准主代理运行；本次没有将它保存成脚本或执行。其命令行参数为项目根，其余输入从标准输入读取；例如 python3 UPDATE_SCRIPT PROJECT_ROOT < 已获准读取的原始增量文件。脚本文件和增量文件的授权不由本次维护路径授权推导，也可由获准的调用者以内存/标准输入提供。

~~~python
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

ROLE = "content-creator"
MEMORY = ".codex/agent-memory/content-creator.md"
ARCHIVE = ".codex/agent-memory/archive/content-creator.md"
EXPECTED_BEFORE_SHA256 = (
    "24affc55b1b1149aa6996fefdb8cd0c638a4f2b9b43bb009b67de0e7ffe06019"
)
FENCE = re.compile(r"(?ms)^" + chr(96) * 3 + r"json[ \t]*\n(.*?)^"
                   + chr(96) * 3 + r"[ \t]*(?:\n|$)")
SAFE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\Z")
REQUIRED_ENTRY = {
    "id", "kind", "status", "summary", "scope", "sources",
    "verification", "action", "recheck_when", "origin"
}

class Stop(Exception):
    pass

def sha(data):
    return hashlib.sha256(data).hexdigest()

def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Stop("重复 JSON 字段，状态未知")
        result[key] = value
    return result

def loads(data):
    return json.loads(data, object_pairs_hook=no_duplicates)

def entry_map(entries):
    if not isinstance(entries, list):
        raise Stop("entries 格式未知")
    result = {}
    for entry in entries:
        if not isinstance(entry, dict) or not REQUIRED_ENTRY <= entry.keys():
            raise Stop("条目格式未知")
        if not isinstance(entry["id"], str) or not SAFE.fullmatch(entry["id"]):
            raise Stop("条目标识无效")
        if entry["id"] in result:
            raise Stop("重复条目标识")
        result[entry["id"]] = entry
    return result

def parse_memory(raw):
    text = raw.decode("utf-8")
    match = FENCE.search(text)
    if match is None:
        raise Stop("记忆缺少完整首个 JSON 代码块，状态未知")
    record = loads(match.group(1))
    if record.get("format_version") != 1 or record.get("role_key") != ROLE:
        raise Stop("记忆格式或身份未知")
    revision = record.get("revision")
    if type(revision) is not int or revision < 0:
        raise Stop("revision 无效")
    entry_map(record.get("entries"))
    if not isinstance(record.get("receipts"), list):
        raise Stop("receipts 格式未知")
    if not isinstance(record.get("history"), list):
        raise Stop("history 格式未知")
    for receipt in record["receipts"]:
        required = {"delta_id", "sha256", "result_revision", "entry_ids"}
        if not isinstance(receipt, dict) or not required <= receipt.keys():
            raise Stop("回执格式未知")
        if (type(receipt["result_revision"]) is not int
                or receipt["result_revision"] < 0
                or receipt["result_revision"] > revision
                or not isinstance(receipt["entry_ids"], list)):
            raise Stop("回执版本或条目标识无效")
    for old in record["history"]:
        if not isinstance(old, dict) or not {"revision", "entries", "receipts"} <= old.keys():
            raise Stop("历史格式未知")
        if type(old["revision"]) is not int or not 0 <= old["revision"] < revision:
            raise Stop("历史修订无效")
        entry_map(old["entries"])
        if not isinstance(old["receipts"], list):
            raise Stop("历史回执格式未知")
    return text, match, record

def render(text, match, record):
    body = json.dumps(record, ensure_ascii=False, indent=2) + "\n"
    return (text[:match.start(1)] + body + text[match.end(1):]).encode("utf-8")

def checked_path(root, relative, must_exist):
    current = root
    parts = Path(relative).parts
    for i, part in enumerate(parts):
        current = current / part
        if current.is_symlink():
            raise Stop("存在符号链接，停止保存")
        if i < len(parts) - 1 and not current.is_dir():
            raise Stop("父目录不存在；当前授权不包含 mkdir")
    if not current.resolve(strict=False).is_relative_to(root):
        raise Stop("路径越出项目根")
    if must_exist and not current.is_file():
        raise Stop("当前记忆缺失")
    if current.exists() and not stat.S_ISREG(current.stat().st_mode):
        raise Stop("目标不是普通文件")
    return current

def sync_directory(directory):
    fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def write_exact(path, data, create):
    flags = os.O_WRONLY
    flags |= (os.O_CREAT | os.O_EXCL) if create else os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    try:
        view = memoryview(data)
        while view:
            count = os.write(fd, view)
            if count <= 0:
                raise Stop("写入未完成，状态未知")
            view = view[count:]
        os.fsync(fd)
    finally:
        os.close(fd)
    sync_directory(path.parent)
    if path.read_bytes() != data:
        raise Stop("整体回读不一致，状态未知")

def validate_delta(raw):
    delta = loads(raw.decode("utf-8"))
    needed = {
        "delta_id", "task_id", "role_key", "dispatch_id",
        "sequence", "read_revision", "changes"
    }
    if not isinstance(delta, dict) or not needed <= delta.keys():
        raise Stop("增量字段缺失")
    if delta["role_key"] != ROLE:
        raise Stop("增量 role_key 不符")
    for key in ("task_id", "role_key", "dispatch_id"):
        if not isinstance(delta[key], str) or not SAFE.fullmatch(delta[key]):
            raise Stop("增量标识段无效")
    if type(delta["sequence"]) is not int or delta["sequence"] < 1:
        raise Stop("sequence 无效")
    expected_id = "/".join((
        delta["task_id"], delta["role_key"],
        delta["dispatch_id"], str(delta["sequence"])
    ))
    if delta["delta_id"] != expected_id:
        raise Stop("delta_id 与身份不一致")
    if type(delta["read_revision"]) is not int or delta["read_revision"] < 0:
        raise Stop("read_revision 无效")
    if not isinstance(delta["changes"], list):
        raise Stop("changes 格式无效")
    changed = set()
    for change in delta["changes"]:
        if not isinstance(change, dict) or change.get("op") != "upsert":
            raise Stop("本次代码只支持逐条新增/修订")
        entry = change.get("entry")
        entry_map([entry])
        if entry["id"] in changed:
            raise Stop("同一次增量重复修订条目")
        changed.add(entry["id"])
        if entry["kind"] not in {"fact", "decision", "correction", "responsibility"}:
            raise Stop("未知 kind")
        if entry["status"] not in {"candidate", "active", "recheck", "archived"}:
            raise Stop("未知 status")
        origin = entry["origin"]
        if not isinstance(origin, dict):
            raise Stop("origin 无效")
        for key in ("task_id", "role_key", "dispatch_id", "sequence", "delta_id"):
            if origin.get(key) != delta[key]:
                raise Stop("条目 origin 与原始增量不符")
    return delta

def canonical_entry(entry):
    return json.dumps(entry, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")

def receipt_status(records, delta, digest):
    wanted = {c["entry"]["id"]: c["entry"] for c in delta["changes"]}
    seen = False
    for record in records:
        states = [record] + record["history"]
        for state in states:
            entries = entry_map(state["entries"])
            for receipt in state["receipts"]:
                if receipt.get("delta_id") != delta["delta_id"]:
                    continue
                seen = True
                if receipt.get("sha256") != digest:
                    raise Stop("同 ID 不同指纹，冲突，停止覆盖")
                if (receipt.get("result_revision") == state["revision"]
                        and set(receipt.get("entry_ids", [])) == set(wanted)
                        and all(entries.get(k) == v for k, v in wanted.items())):
                    return True
    if seen:
        raise Stop("有回执但找不到一致的完整结果，状态未知")
    return False

def main():
    if len(sys.argv) != 2:
        raise Stop("用法：python3 UPDATE_SCRIPT PROJECT_ROOT，原始增量由 stdin 输入")
    root = Path(sys.argv[1]).resolve(strict=True)
    if not root.is_dir():
        raise Stop("项目根无效")
    raw_delta = sys.stdin.buffer.read()
    delta = validate_delta(raw_delta)
    digest = sha(raw_delta)
    memory = checked_path(root, MEMORY, True)
    # 即使仅需去重，也先确认已授权归档位置的现有情况。
    archive = checked_path(root, ARCHIVE, False)
    before = memory.read_bytes()
    text, match, current = parse_memory(before)
    records = [current]
    archive_raw = None
    if archive.exists():
        archive_raw = archive.read_bytes()
        records.append(parse_memory(archive_raw)[2])
    if receipt_status(records, delta, digest):
        print(json.dumps({
            "learning": "已保存",
            "delta_id": delta["delta_id"],
            "detail": "完整当前/历史/归档结果、回执和原始指纹一致；未重复写入"
        }, ensure_ascii=False))
        return
    if not delta["changes"]:
        print('{"learning":"无增量，未写入"}')
        return
    if sha(before) != EXPECTED_BEFORE_SHA256:
        raise Stop("写前版本已变化；重新读取并由主代理重新合并，不覆盖")
    if delta["read_revision"] != current["revision"]:
        raise Stop("增量基于陈旧修订；主代理须重新核对合并")
    after = copy.deepcopy(current)
    by_id = entry_map(after["entries"])
    positions = {entry["id"]: i for i, entry in enumerate(after["entries"])}
    for change in delta["changes"]:
        entry = copy.deepcopy(change["entry"])
        old = by_id.get(entry["id"])
        if old is not None:
            if change.get("previous_sha256") != sha(canonical_entry(old)):
                raise Stop("修订未关联一致的原条目")
            after["entries"][positions[entry["id"]]] = entry
        else:
            if change.get("previous_sha256") is not None:
                raise Stop("新增条目错误关联旧条目")
            after["entries"].append(entry)
    after["history"].append({
        "revision": current["revision"],
        "entries": copy.deepcopy(current["entries"]),
        "receipts": copy.deepcopy(current["receipts"])
    })
    after["revision"] += 1
    after["receipts"].append({
        "delta_id": delta["delta_id"],
        "sha256": digest,
        "result_revision": after["revision"],
        "entry_ids": [c["entry"]["id"] for c in delta["changes"]]
    })
    complete = render(text, match, after)
    if parse_memory(complete)[2] != after:
        raise Stop("待写完整结果自校验失败")
    if archive_raw is not None and archive_raw != before:
        raise Stop("已有不同归档；本次代码不覆盖，需主代理另行核对")
    if archive_raw is None:
        write_exact(archive, before, create=True)
    if archive.read_bytes() != before:
        raise Stop("写前完整归档未验证，禁止更新当前文件")
    parse_memory(archive.read_bytes())
    if memory.read_bytes() != before:
        raise Stop("保存前版本变化；停止覆盖")
    write_exact(memory, complete, create=False)
    reread = memory.read_bytes()
    if reread != complete or parse_memory(reread)[2] != after:
        raise Stop("当前正文/回执/修订回读失败，状态未知")
    if not receipt_status([after], delta, digest):
        raise Stop("最终完整结果证据不一致，状态未知")
    print(json.dumps({
        "learning": "已保存",
        "result_revision": after["revision"],
        "delta_id": delta["delta_id"],
        "entry_validation": "由条目状态及主代理先前核对决定，保存不升级可信度",
        "archive": "写前完整副本已整体回读，当前仍保留历史，未宣称迁移完成"
    }, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except (Stop, OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({
            "status": "PARTIAL",
            "learning": "状态未知或待保存；没有完整回读证据不称已保存",
            "reason": str(exc),
            "required_action": (
                "保留原始增量；核对当前、回执、历史和归档。"
                "若当前残缺则限制使用，先由主代理恢复可验证版本。"
                "内容任务交付结果独立报告。"
            )
        }, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
~~~

增量的最低调用契约示例（仅示例，不是真实经验，不应直接保存为项目认识）：

~~~json
{
  "delta_id": "example/content-creator/example-dispatch/1",
  "task_id": "example",
  "role_key": "content-creator",
  "dispatch_id": "example-dispatch",
  "sequence": 1,
  "read_revision": 1,
  "changes": []
}
~~~

非空 changes 每项为 {"op":"upsert","entry":完整条目}；更新现有条目时还需 previous_sha256，为旧条目用代码 canonical_entry 得到字节后的 SHA-256。输入原始字节是指纹依据，重试不得重排 JSON 或改变空白。若重新核对后正文有变化，必须新建 delta_id 并关联原条目。

## 实际读取范围与验证

按启动规则额外读取 /Users/fun/.codex/skills/subagent-delegation/SKILL.md；没有读取其模型配置或派生子代理。此读取用于约束当前职责，不作为两个模拟请求的学习协议来源。

实际读取正文仅包括：

1. baseline/skills/agent-dispatch/SKILL.md。
2. baseline/skills/agent-dispatch/references/project-learning.md。
3. baseline/skills/agent-dispatch/assets/learning-protocol.md。
4. baseline/skills/agent-dispatch/assets/role-learning.txt。
5. baseline/skills/agent-dispatch/assets/role-memory.md。
6. input/project/AGENTS.md。
7. input/project/.codex/agent-memory/protocol.md。
8. input/project/.codex/agent-memory/content-creator.md。

另以 rg --files 枚举 baseline/skills/agent-dispatch 与 input/project 路径，并以 rg --files --hidden 枚举 input/project/.codex；枚举中见到他人 outputs 的文件名，但没有读取任何报告或输出正文。未读取真实源码仓库、其他代理报告、legal-compliance-checker 记忆或角色 TOML。

只读验证：Python 标准库读取当前记忆字节计算上述 SHA-256，并检查归档文件及父目录是否存在，命令退出状态 0。归档文件与父目录检查均为 False。写入前以 test ! -e run/baseline.md 确认目标尚不存在，退出状态 0。没有运行记忆更新代码，没有改变项目配置、记忆、第三方系统或 Git。

未确认项：新旧模拟角色的完整 TOML、实际调用名、源正文、旧角色实际配置路径、既有全量映射冲突、旧协议/归档定制、真实新增量及证据、将来运行时独占与维护授权、宿主加载及中断后的实际恢复结果。脚本语法可独立静态编译验证，但即使通过也不等于已执行保存或已证明任意中断点恢复。


产出后最小验证：以 Python ast.parse 静态解析本文件唯一的 Python 代码块，并断言旧路径、新标识和无旁路文件/目录创建调用；结果 PASS，退出状态 0。未执行该代码块，未生成 pyc 或脚本文件。本验证只证明语法与所列静态条件，不证明运行和中断恢复成功。
