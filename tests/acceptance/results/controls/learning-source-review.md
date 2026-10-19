# 项目角色学习实现独立关键复核

状态：**PARTIAL（派发范围的独立只读源码复核已完成；最终全局证据清单仍由主代理收束）**。未发现仍未解决的高优先级问题。确认的一项中优先级测试维护问题已由主代理修复，并通过本审查者的定向复核。本报告不代替主代理的最终集成、整体验收或完成判断。

本次改动将学习协议随团队配置复制到目标项目，固定岗位身份与记忆映射，角色交接增量，主代理在当前授权内串行合并并回读。两个 Skill 保持显式入口，普通任务不依赖另一个 Skill 的安装目录。复核使用 `code-review deep`、`ponytail-review` 与 `karpathy-guidelines`，只比较本次新增影响，保留任务开始前已有改动。

## 范围、基准与覆盖

- 仓库：`/Users/fun/Documents/ChatGPT/Skill/agent-dispatch`。
- 权威设计：`docs/plans/2026-10-19-project-role-learning-design.md`。比较基准：`/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline`。使用目录差异与逐文件 diff；未把 Git 中早于快照的文档/验收变更计入本次发现。
- 完整阅读本次新增三个 assets、`references/project-learning.md`、两个 `SKILL.md` 及各自项目参考、README、新增学习 fixtures、`tests/learning.test.js` 与 `tests/acceptance.test.js` 的新增逻辑。关联读取验收说明与 `tests/package.test.js` 的 Finder 元数据过滤差异。
- 读取真实 repair/reuse 报告、原始增量、revision 1 记忆、主代理合并记录、13 类原始边界情景及实际响应/复核记录；另核对新增旧项目迁移及改名快照与测试。单用户临时工作区、单主代理串行维护是本次判断的负载前提。

| 影响路径 | 已核对的行为与边界 |
| --- | --- |
| 配置入口 → 项目协议/映射 → 角色指引 | 完整方案先确认精确路径及日常合并授权；稳定 key 不随显示名重算；原专业正文和定制保留；已有等效结构按真实路径适配。 |
| 任务读取 → 纠错 → 增量 | Q3 触发与原返工计数保留；缺失/未知格式如实返回；未验证推断、已确认决定、环境与权限不足分别处理；角色不写共享记忆。 |
| 主代理合并 → 持久化 → 后续复用 | 当前权限优先、单写者、版本重读、原始字节指纹、同 ID 冲突、完整结果和整体回读均有明确步骤；真实保存正文与增量一致，后续新上下文报告实际读取并使用条目。 |
| 中断、归档、来源失效 | 不凭回执判成功；历史合法修订可证明旧保存；先核对归档再移除当前副本；只处理失效条目。当前证据属于预置状态的恢复决策核对。 |
| 迁移、改名与独立安装 | 旧角色迁移保持模型、正文与定制；改名快照保留原 key 和记忆路径；两个 Skill 的全部 14 个本地 Markdown 引用均存在且留在各自目录内。 |
| 只读、职责与结束条件 | 一般维护许可不覆盖本次只读；精确例外只作用于指定路径；记忆不转移正式职责，不重置两轮返工，不隐式迁移旧项目。 |

## 中 / 应当修复

1. **全新完整重放被误要求历史复用字段（已修复）**

   位置：`tests/acceptance.test.js:43`，当前修复为第 43–46 行的条件检查；需求依据为 `tests/acceptance/README.md:9` 至第 16 行的全新重放流程，以及第 21 行仅对定向复用历史证据增加来源保留要求。

   触发及证据：构造一个全新完整 replay，其版本、当前 Skill/fixture/output 哈希全部匹配，`nativeTomlParse=PASS`、`scope=isolated-simulated-user`，且没有复用历史调用，所以不含 `priorSkills` / `revalidation`。直接通过 Node VM 和内存 `fs` 调用真实测试文件的第一个测试回调，原实现只因无这两个字段而以 `retain prior provenance when reusing unaffected evidence` 失败。复现命令为 `node - <<'JS'` 的内联隔离脚本，完整执行退出 **0**；未修改测试文件、项目产物或证据。此问题会迫使维护者为合法的全新重放伪造无关历史信息，或使整个测试入口失败。

   最小建议：仅在任一历史字段存在时要求两者配对，并核对对应报告存在。主代理已实施该建议。本审查者重新执行真实回调的同一内存验证，四种结果为：全新完整 replay 接受；只有 `priorSkills` 拒绝；只有 `revalidation` 拒绝；两字段配对接受。定向复核完整退出 **0**，无未解决事项。该验证是回调逻辑验证，不冒称真实模型重放。

## 实际验证

- `node --check /Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/learning.test.js`，退出 **0**；`node --check /Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/acceptance.test.js`，退出 **0**。
- Python 只读内联断言，退出 **0**：保存的唯一条目与原始增量 `changes[0].entry` 全对象一致；回执的 ID、原始增量 SHA-256、结果修订和条目标识一致；revision 0 恢复线索完整；四个来源/产物哈希与实际文件相同；repair/reuse 的活动名、原始编号与项目约定结果一致；复制到项目的协议与源模板逐字一致。
- 同一 Python 检查重新计算只读项目完整树，八个文件均等于保存的 before/after 哈希；两个 Skill 共 14 个本地 Markdown 引用存在且未越出各自安装目录。该检查未创建隔离安装副本，也未宣称宿主已原生加载。
- `node --test /Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/learning.test.js /Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/acceptance.test.js`，本次执行退出 **1**：10 项中 9 项通过。唯一失败为 `acceptance.test.js:36` 的当前 Skill 清单核对；执行时全局 `results/replay.json` 仍保留旧清单，主代理已说明正在汇总保存。新增学习三项、首次配置、增岗、保留定制、幂等、历史文档证据及确认门槛等其余九项均通过。此执行不是完整成功，不能据其报告全套测试通过；不将进行中的证据汇总另列为源码缺陷。

## 未确认项与残余限制

最终全局 replay 清单与全套测试应由主代理在证据保存完成后核对，本报告没有将其进行中状态改写为 PASS。原五岗文档供稿/复核为保留身份、时间和原 Skill 哈希后的历史复用；本次没有重新调用全部五岗。

中断、归档、多实例/冲突、拆分替换与单写者等边界主要验证真实代理读取预置输入后的判断；不证明真实崩溃恢复、实际归档全过程或多主并发锁。已检查旧项目迁移/改名快照保留性，未额外调用改名岗位验证宿主加载。通用委派读取角色正文与新上下文复用，仍不等同于原生岗位注册成功或长期效果改善。这些限制已由协议/验收材料相应说明，未发现需要额外扩大实现的依据。

本审查者只写本报告，未修改源码、测试、配置、项目学习记录或 Git 状态；未递归委派。源码复核结论：在上述覆盖范围内，无仍待修复的已确认问题；最终集成验收状态由主代理裁决。

## 复核时的当前源码指纹

- `skills/agent-dispatch/assets/learning-protocol.md`：`7216bda008f36429dea8d6552b3653420d3a25acb3338706889b6d2f1cd5d5d5`
- `skills/agent-dispatch/references/project-learning.md`：`3957cdc9209f76f593bab027829d1e9ee8c8ca236318bbe6fc7d155211380ffb`
- `tests/learning.test.js`：`f20ef4d8913f5ce23278abe11c4f5fdfd85ceac8b652e6ebb7950f1b4f03638e`
- `tests/acceptance.test.js`：`a2221d6dd84282c4f39147ae65bfb82c18ebd88c3773bef0f81626f11a09f95c`
