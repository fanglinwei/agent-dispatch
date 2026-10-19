# 隔离保存函数实施报告

状态：本次分配的保存函数与直接验证已完成。职责限于 `run/save-memory.py`、`run/save-report.md` 和 `run/save-check/`；未修改输入样本、真实源码、代理配置或共享记忆，未执行 Git 写操作或委派。真实候选准备、来源与确认状态、唯一主代理身份以及最终调用仍由主代理负责。

## 实际依据

运行依据为本次派发及当前源码协议，而不是样本中保留的旧入口。结束前已重新读取加入“获准保存时按需创建必要父目录，创建前后检查边界/链接”的最新正文。

| 来源 | SHA-256 |
| --- | --- |
| `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/skills/agent-dispatch/assets/learning-protocol.md`（协议版本 1，12296 字节） | `c9b61e36ddad5585d8bea0fee56cc3993a00b9cbaa6ab53f2dd0652936302f84` |
| 同 Skill 的 `references/project-learning.md`（6662 字节） | `82256e724aef28400e56aa35339cb573f80350c0f011dfc389a55d5700be6866` |
| `input/project/AGENTS.md` | `d902cc2bbd36535b7ddd3713e09df750bd2469bd0d838ec0217cfa6a1580c386` |
| `input/project/.codex/agent-memory/protocol.md` | `7216bda008f36429dea8d6552b3653420d3a25acb3338706889b6d2f1cd5d5d5` |
| `input/project/.codex/agent-memory/content-creator.md`（revision 1） | `24affc55b1b1149aa6996fefdb8cd0c638a4f2b9b43bb009b67de0e7ffe06019` |
| `input/project/.codex/agent-memory/legal-compliance-checker.md`（revision 0） | `f89665e155ce848f45afaf6730ca00c33c484ed802e5fcde4ca519ad9ce18d05` |

样本协议缺少当前安全保存段，样本入口尚未列精确 `.pending` 授权；它们是历史学习样本，未据此扩权或更新。本函数以主代理传入、本次确已获准的 `allowed_paths` 为边界，不自行从旧入口推导暂存权限。没有读取其他代理报告。

## 接口与实际行为

唯一对外操作：`save_memory(root, target_rel, candidate_bytes, expected_sha256, allowed_paths)`。Python 标准库实现，无 CLI、增量合并引擎、锁或后台任务，模块导入不执行文件系统写操作。

- `candidate_bytes` 必须是完整 UTF-8 字节。支持当前 Markdown 首个 `json` 围栏记录及等义的完整 JSON 对象；只支持 `format_version: 1`。验证顶层数组、非负整数修订、条目必需字段、来源定位/版本或哈希、回执结构、重复/冲突回执及记录内的条目引用。真实来源、确认权限、增量原始哈希与候选合并是否正确不由结构检查代替。
- `expected_sha256=None` 精确表示调用方确认目标原本不存在；否则必须等于实际旧目标完整原始字节的 SHA-256。旧目标先读取并验证完整结构；未知格式或损坏的旧目标返回 `unknown`，不会覆盖。已有目标的不同候选必须保持 `role_key`，并提高 revision；完全相同字节返回 `unchanged`，不创建暂存或归档目录。
- `allowed_paths` 为项目相对路径字符串集合或 frozenset，必须同时包含原样的 `target_rel` 和 `target_rel + '.pending'`。拒绝绝对路径、空段、`.`、`..`、反斜杠、大小写/Unicode 规范化别名、文件/目录前缀冲突；检查获准路径现存组件及硬链接。根目录本身先规范为实际目录；根内路径组件的符号链接全部保守拒绝，包括安全指向根内的链接，暂存链接不跟随。
- 候选、旧目标、精确授权和路径预检通过后，才按需创建该目标必需的父目录，并在创建前后检查路径。以 `O_CREAT | O_EXCL`（宿主有时加 `O_NOFOLLOW`）独占新建 `.pending`。完整写入、flush、宿主支持时 fsync、关闭、整体回读并解析，与完整候选逐字节及完整 JSON 内容核对。
- 原有 `.pending` 不覆盖、不提交、不删除，返回待恢复状态。新产生的暂存在失败时保留供主代理核对；本函数不自动恢复、清理或派发暂存内容。
- 替换前再次读取目标，核对旧完整字节和 revision，首次创建则核对仍不存在；发生变化即停止并保留暂存。再次检查暂存后，仅使用同目录 `os.replace` 原子替换；不会原地截断旧目标、先删后移或自动回滚新版本。
- 替换后整体回读，要求完整候选字节、完整记录、修订和回执相同，随后尝试同步父目录。遇到替换/回读/同步异常会再观察当前目标，完整候选确实已在目标中则报告 `saved` 并保留同步缺口；不能核对则 `unknown`。普通失败且旧目标保持原样为 `pending`。

结果字典含 `status`、`learning_status`、`reason`、`phase`、`committed`、原样目标/暂存路径、候选/实际 SHA-256 与修订（已读到时）、`pending_retained`、`sync.file`、`sync.directory` 和不含材料正文的 `issues`。

| status | 含义 |
| --- | --- |
| `saved` / 已保存 | 目标整体回读与已验证完整候选一致。仍应检查 `sync` / `issues` 中的同步缺口；不代表条目已获真实确认或证据为真。 |
| `unchanged` / 无增量 | 目标字节已完全相同，没有发生写入。 |
| `pending` / 待保存 | 本次保存没有完成替换；可能缺权限、候选不合格、陈旧版本、待恢复暂存或保存失败。它不是“所有历史/归档均未包含某增量”的恢复结论。 |
| `unknown` / 状态未知 | 目标当前完整性或提交结果无法核对，`committed` 为 null；主代理须先恢复/协调，不能按未保存重放。 |

## 直接验证

命令（工作目录为本任务隔离根）：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 run/save-check/check_save.py
```

最终执行退出状态 **0**：**20 个用例全部通过**。覆盖正常替换、无额外侧文件、首次归档创建及零增量、缺暂存授权、不合格候选不建归档目录、目标存在/不存在前提、陈旧哈希、旧暂存/暂存链接保留、逃逸与大小写/前缀/硬链接别名、父目录链接、未知格式、只有回执缺条目、写后替换前陈旧目标、文件 fsync 失败、替换调用失败、替换前中断、提交后回复失败、目录 fsync 失败，以及替换后损坏目标返回 unknown。

实际 `content-creator` revision 1 记录用于测试：在测试独占目录组装完整 revision 2，保存并整体回读，再用同一函数首次保存完整归档；原输入字节保持一致。普通测试数据及故障残留全部位于 `run/save-check/`。

独立的只读导入审计命令使用 `PYTHONDONTWRITEBYTECODE=1 python3 -` 执行 importlib 加载，并以 `sys.addaudithook` 检查写打开、mkdir、remove、rename、rmdir、chmod、link、symlink 事件，退出 **0**，结果 `import_mutations: []`。`inspect.signature` 精确为 `(root, target_rel, candidate_bytes, expected_sha256, allowed_paths)`。

最终函数 SHA-256：`8f2c11dc0bfdbaa780b0531e833ed46e317b16919fb585a68cf36b840bd44a06`；测试脚本 SHA-256：`63063e58841e2b05bacca7b5618c7eda6217bc88b041b82c995698bd4277de5f`。

## 保证边界与交回事项

保证范围是已确认单写者、宿主支持同目录原子替换条件下的一次保存；字节/修订复查不能充当跨进程锁，也未防御外部恶意进程在路径检查与系统调用之间替换目录、链接或文件。没有实际 SIGKILL、断电、硬件损坏或所有文件系统的恢复试验；中断验证通过 Python 异常注入，原子性依赖宿主 `os.replace` 语义。同步不支持或失败会如实返回，不保证断电恢复；新建祖先目录没有逐级持久化保证。

新暂存和首次目标权限为 0600，新建必要父目录为 0700；原文件的 ACL、扩展属性、时间、拥有者及权限元数据不复制。保存失败可能留下这次按需创建的必要空目录，以及应核对的 `.pending`；不自动清理。

历史/归档的真实性、完整保留、回执 result_revision 对应原合并结果、历史成功判定及来源/批准状态由主代理负责。本函数不扫描相关归档来判断增量是否曾保存，也不决定条目 active 状态。

归档迁移须由主代理先调用本函数提交并核对完整归档，再调用同一函数更新当前文件；它们不是跨文件事务。归档失败应保留当前完整副本，当前更新失败应保留已验证归档和当前旧版；本函数不会删除任何唯一副本。真实项目/共享记忆保存仍未执行，无本职责内剩余阻塞。
