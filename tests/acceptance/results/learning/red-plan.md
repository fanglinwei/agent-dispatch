# 四期社区活动周刊：首次团队配置方案

状态：方案已完成，供检查与批准；未写入任何项目配置，未开始内容创作。该方案按旧版 `agent-dispatch` 运行至展示完整方案的阶段。此次有界执行只负责方案，所有配置写入由主代理完成。

## 已确认目标与范围

面向社区居民连续交付四期活动周刊，每周一期，每期一份 Markdown，包含三篇活动内容，以及活动摘要、报名须知、来源清单和下期计划。以社区提供的已授权活动资料为事实依据，语气友好清晰，适合手机阅读。主代理承担统筹，不另设统筹岗位。

本阶段只配置完成内容工作的必要岗位与协作规则。后续内容创作、项目实施文档、发布及 Git 写操作均不在本阶段执行范围。项目为空，没有需要保留的现有岗位、旧文档或自定义 Skill；用户已确认项目类型、内容、工具、风格与交付程度。

`grill-me` 不可用，采用 `references/interview.md` 的替代访谈方法核对已有决定。现有信息足以确定本次选岗和责任边界，无需重复提问。首期日期、具体活动资料和活动内容属于后续创作任务输入，不阻断本次团队配置，不擅自编造。

## 岗位选择与来源

只新增一个项目岗位 `Content Creator`，复用上游原岗位名、description 和完整专业正文。其内容策略、文案创作、叙事一致性、长文及平台适配能力足以承担本次社区周刊。项目协作规则将工作范围收窄为授权资料内的四期 Markdown 周刊，不将上游营销增长指标作为本项目验收标准，不赋予分发或外部操作权限。

| 项目 | 拟配置 |
| --- | --- |
| 原岗位名及项目调用名 | `Content Creator` |
| 固定来源 | `agency-agents`，提交 `652b2692f8d8ec2b1f1a38e559073e287dfdc469` |
| 上游文件 | `marketing/marketing-content-creator.md` |
| 固定提交链接 | https://github.com/msitarzewski/agency-agents/blob/652b2692f8d8ec2b1f1a38e559073e287dfdc469/marketing/marketing-content-creator.md |
| 已读本地副本 | `baseline/tests/acceptance/fixtures/team/upstream/marketing/marketing-content-creator.md` |
| 主责 | 每期三篇活动内容的编写与修订、报名信息表达、来源清单、下期计划、手机阅读体验自查 |
| 调用条件 | 后续明确授权编写或修订某期周刊，并已提供该期授权资料和精确写入范围时 |
| 交接对象 | 主代理，负责事实与来源对应验证、专业质量复核、最终裁决与交付判断 |
| 默认维护 | 已交付周刊中的内容修订；仅获得每次派发明确列出的文件权限 |

已读取候选 `Legal Compliance Checker` 原文；本次需求没有新增法律解释、隐私政策、报名数据处理或跨司法辖区合规工作，且内容来源已确认为社区提供的授权资料，因此不纳入初始团队。不创建自定义替代岗位，不另设统筹或检查岗位。日后出现影响原分工的新任务时，再检查现有团队的实际缺口并提出增补。

项目为空，未见项目级名称冲突。可见用户级岗位与宿主列出的内置角色均未包含 `Content Creator`，当前可见范围内名称可用；原生加载后的实际注册结果仍须另行核对。

## 精确写入清单

任务材料未给出待配置空项目的绝对根路径，以下路径全部严格相对于后续获准配置的同一个项目根；不把测试夹具目录或本报告所在目录当作项目根。主代理在写入前应将这些精确相对路径绑定至实际目标根，不增加其他文件。

| 精确项目相对路径 | 操作与内容 |
| --- | --- |
| `.codex/agents/content-creator.toml` | 新建一个岗位文件。三个非空字符串字段为 `name`、`description`、`developer_instructions`；保留上游名称、原始描述和 Markdown frontmatter 之后的完整正文。 |
| `.codex/agents/LICENSE.agency-agents` | 原样复制固定快照 `upstream/LICENSE` 的完整 MIT 许可及版权声明。许可位置及来源写入角色 TOML 注释。 |
| `AGENTS.md` | 新建一个集中协作区块，写入下面的项目目标、岗位分工、Skill 使用、派发、授权和验收约定。若写入时出现已有文件，则保留完整内容，只在已有等效协作区块中合并，不覆盖。 |

采用项目原生 `.codex/agents/` 目录格式，不为注册额外创建 `.codex/config.toml`，不增加未经证实的配置键。角色文件不写模型或 effort，后续选择遵守目标环境已有委派规则；省略这些字段不表示已验证实际模型。

拟写入的角色字段值：

```toml
# Upstream name: Content Creator
# Source: https://github.com/msitarzewski/agency-agents/blob/652b2692f8d8ec2b1f1a38e559073e287dfdc469/marketing/marketing-content-creator.md
# License: LICENSE.agency-agents
# Adaptation: 仅格式转换；保留完整专业正文；展示元数据不转换为配置项。
name = "Content Creator"
description = "Expert content strategist and creator for multi-platform campaigns. Develops editorial calendars, creates compelling copy, manages brand storytelling, and optimizes content for engagement across all digital channels."
developer_instructions = '''
[此处由主代理逐字置入已读取源文件 frontmatter 之后的完整专业正文，从 # Marketing Content Creator Agent 起至末尾，不使用此占位文字作为最终配置]
'''
```

上面的占位只为避免方案重复抄录源文件。它指定了唯一来源和完整转换边界；生成时必须替换为全文，再逐字核对。上游 `tools`、`color`、`emoji`、`vibe` 是源文件展示元数据，不成为 TOML 配置字段。无需改写岗位专业正文；项目特定边界集中维护在 `AGENTS.md`。

## 拟写入 AGENTS.md 的协作约定

以下内容为本方案的完整规则范围，主代理可使用单一标记区块 `<!-- agent-dispatch:start -->` 与 `<!-- agent-dispatch:end -->` 包裹，重复运行时更新同一区块。

1. **目标与完成标准。** 项目为四期面向社区居民的活动周刊；每周交付一期 Markdown，每期三篇活动内容，覆盖活动摘要、报名须知、来源清单和下期计划。基于社区提供的授权资料写作，表达友好清晰，采用短段落、清晰标题和便于手机阅读的列表。活动时间、地点、对象、名额、报名方式、截止时间等以该期资料为准；资料未载明的内容不编造，交回主代理澄清。每条活动事实与报名要求能对应至来源清单中的具体资料。

2. **岗位调用与默认维护。** 主代理在后续获准编写或修订周刊时，按需要调用已配置的 `Content Creator`。该岗位为周刊文字、报名须知表达、来源清单和下期计划的唯一内容主责；维护责任不授予整目录写权限。主代理保留统筹、范围与优先级判断、资料核对、成果集成、关键证据复核、最终裁决及完成声明。任何角色均不得自行递归委派、修改代理配置或由岗位原文推导额外权限。

3. **未来成果位置与单写入者。** 后续创作任务建议采用 `issues/issue-01.md`、`issues/issue-02.md`、`issues/issue-03.md`、`issues/issue-04.md` 作为四期成果的精确项目相对路径；这是待批准的日常路径约定，本次不创建目录或周刊文件。每一期内的三篇活动正文、报名须知、来源清单和下期计划统一由本期 `Content Creator` 写入同一文件，避免分割为多人同时改写的共享文件。主代理提供审核意见；修订交回原内容负责人。需要主代理最终编辑时，先结束该岗位的写入职责并核对当前内容版本，再由主代理接管，同一时刻保持唯一写入者。

4. **每次派发契约。** 派发必须包含本期编号和具体目标、授权资料的实际路径与版本或哈希、允许动作、精确只读和可写文件、适用规则与 Skill、三篇内容及四类栏目要求、验收标准、返回证据和未覆盖范围。未有明确创作授权时，不因岗位已配置而自动制作周刊。资料缺失仅阻断受影响内容，说明需补充的项目及恢复条件，继续其他独立且已获准的工作。不覆盖其他工作者的修改。

5. **日常工作与交接。** 接收并阅读本期资料后，`Content Creator` 依据授权资料编写或修订指定期号文件，自查三篇内容与栏目完整性、事实准确性、来源可追溯性、报名信息清晰度和手机阅读体验，再交回主代理。交接给出实际成果路径、文件内容哈希或能唯一定位未提交内容的版本、已用资料、已检查项、检查方法与结果、未覆盖项和待确认信息。采用对话或现有交接入口即可，不为此固定增加台账或额外项目文档。

6. **风险与检查分工。** 单一主责、只改局部措辞且不改变活动事实、报名要求或共享约定的变更可为 `light`，一次针对性验证即可。每期完整周刊按 `standard`：内容负责人自查，主代理验证结果符合性并复核表达质量、事实与来源的对应，以及活动正文与报名须知之间的一致性。上述两种检查注明检查者和对象；同一会话的不同检查不称为独立岗位检查。出现敏感信息、授权范围变化或不可逆影响时，仅对受影响任务提高风险等级、明确边界和所需独立验证，不自动增岗或发起额外项目工作。必须独立检查而条件不足时，受影响部分标为 `PARTIAL`。

7. **结论与返工结束条件。** 结果验证用 `PASS / FAIL / NEEDS_ENVIRONMENT`，质量复核用 `APPROVE / CHANGES_REQUESTED / NEEDS_EVIDENCE`，分别记录在交接中。缺资料、缺环境或缺授权写明具体缺口及恢复条件，不能视为产品缺陷或通过。主代理将阻塞项合并交回原内容负责人修订，建议和风险提示单列；每期验收单元默认最多两轮合并返工，仍有阻塞则交主代理裁决或向用户提出选项，受影响部分保持未完成。修改后复核失效结论与相邻影响，保留仍有效证据。通过后的非阻塞建议由用户选择，出现新缺陷或新增需求才重开相应范围。

8. **集成与完成判断。** 主代理核对活动正文、报名信息和来源清单的对应关系，核对下期计划属于资料支持的计划或清楚标明待确认；各项自查不能替代这项整体核对。四期均完成且各期三篇和必要栏目通过检查，才可判断周刊目标完成。项目交付检查属于后续实际任务，本次只配置其方法。

9. **授权边界。** 岗位调度继续遵守现有委派、模型、工具和文件权限规则；配置不自动授予发布、外部通信、安装、修改第三方系统或 Git 写操作权限。本阶段不创作内容，不编写实施文档，不发布，不执行 Git 写操作。项目配置仅由获准主代理写入。

10. **后续文档交接。** 此次不新增需求、设计、进度或实施文档。若用户后续需要，交接已确认目标、本岗位定义、成果主责、Skill 规则与未决事项，并由用户显式调用 `agent-dispatch-doc`；未安装时仅说明名称和所需前置资料，不假设其可用，也不补做其任务。

## Skill 使用安排

岗位名本身不触发方法 Skill。本次已实际读取并用于方案的是指定的旧版 `agent-dispatch` 及其三个参考；当前没有项目指定或已安装的周刊创作专用 Skill，本方案不额外绑定不匹配的文档、代码或外部平台 Skill，不要求安装插件。

| 岗位或任务 | 触发条件 | Skill 与已核实位置 | 要求与不可用处理 |
| --- | --- | --- | --- |
| 主代理，首次团队配置 | 用户显式调用，当前已满足 | `agent-dispatch`；本次实际路径为 `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/skills/agent-dispatch/SKILL.md` | 本次必用且已用于方案；项目配置中记录采用宿主实际注册名或目标环境已核实入口，不把测试临时绝对路径复制为长期入口。将来仅在用户显式调用时使用。 |
| 主代理，需求访谈 | 影响目标或分工的决定尚未明确 | `grill-me` 不可用；本次已核实的替代方法为旧版 Skill 的 `references/interview.md` | 优先项缺失已说明，按其允许的备用分轮方法继续；本轮已有信息充分，未重复询问。 |
| `Content Creator`，Markdown 周刊创作与修订 | 后续明确授权对应任务且资料可用 | 无额外必用或推荐的专用 Skill；以已确认协作规则和实际授权资料为方法依据 | 可以按一般内容创作方法执行，不声称使用未安装技能。以后新增适用 Skill 时，先读取真实指令、核对依赖与定位方式，只更新受影响绑定并纳入确认范围。 |
| 主代理，各岗位委派 | 允许且确有独立产出的派发 | 目标环境已有模型选择/委派规则；此次已读取 `/Users/fun/.codex/skills/subagent-delegation/SKILL.md` | 遵守目标环境现有规则，不将本机绝对路径未经核对地复制进其他环境；每次派发带上本次适用的 Skill 和已核实定位方式。 |

未来若绑定必用 Skill 或必需依赖而不可用，只暂停依赖它的部分并标 `PARTIAL`，说明缺失和恢复条件；不擅自安装、替换或跳过。推荐项不可用则说明后采用一般方法。交付区分“可用”“已读取”“已用于任务”“执行受阻”，不把可见或启用当成已执行。

## 验证安排与当前证据

方案批准且由主代理写入后，做与这三个配置文件直接相关的最小充分验证：

- 以 Python 3.11+ `tomllib` 或等效可靠解析器解析岗位 TOML，核对三字段均为非空字符串，名称为 `Content Creator` 且不冲突，没有无依据字段。
- 逐字比较 `developer_instructions` 与选定上游正文；核对 source、adaptation、license 注释，核对许可文件与快照完整一致。
- 比较写入前后精确文件差异，检查已有内容保留、目标全覆盖、唯一主责、来源追溯、技能规则及职责交接一致。空项目未初始化 Git 时用文件快照比较，不初始化 Git，也不执行 Git 写操作。
- 再检查同一方案，确保不会重复建立岗位、协作区块或许可副本。
- 宿主若有只读岗位列表，可核对实际注册名称；否则标注加载未验证，提示新会话或重启后核对。不得试派发来启动周刊创作。格式有效、已写入和原生已加载分别陈述。

当前已经完成：完整读取指定初始需求、旧版 Skill 和三个参考、两份候选岗位、来源清单及许可；读取可见用户级角色文件的名称；检查固定快照三份文件的 SHA-256。只读核验命令为 Python 标准库 `json`、`hashlib`、`pathlib` 和 `tomllib`，退出码 0。结果：

| 快照文件 | SHA-256 | 结果 |
| --- | --- | --- |
| `marketing/marketing-content-creator.md` | `26ddce44f057068a3935c13d53becd3c57385fb47fcdcfdd891b80269070b3d5` | 与 `source.json` 匹配 |
| `support/support-legal-compliance-checker.md` | `08d938c5666e41b3cf197c2f7b37070d7f39aca62b7147d157200eb6dbeeced6` | 与 `source.json` 匹配 |
| `LICENSE` | `9a45258434d5cedf0af73c9ad4771373701225038d246c49219026c33677f66f` | 与 `source.json` 匹配 |

未验证项：项目配置尚未生成，故未做生成后 TOML 解析、生成正文比对、项目文件差异或宿主加载检查；本地来源与所给清单一致，未另行联网验证提交。目标项目绝对根未提供，因此使用精确项目相对路径。当前没有周刊资料及日期，但它们不影响初始配置方案；实际创作阶段由对应派发提供。此方案完成不等于配置已写入，也不等于周刊或实施文档已完成。方案按本次职责交回主代理，不在本执行中等待或冒充用户批准。

## 实际读取文件路径

以下列出本次读取的文件；只列目录、但未读取的 `addition.md`、`repeat.md` 不列为已读。

1. `/Users/fun/.codex/skills/subagent-delegation/SKILL.md`
2. `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/skills/agent-dispatch/SKILL.md`
3. `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/skills/agent-dispatch/references/role-skills.md`
4. `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/skills/agent-dispatch/references/interview.md`
5. `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/skills/agent-dispatch/references/codex-project-agents.md`
6. `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/tests/acceptance/fixtures/team/initial.md`
7. `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/tests/acceptance/fixtures/team/source.json`
8. `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/tests/acceptance/fixtures/team/upstream/marketing/marketing-content-creator.md`
9. `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/tests/acceptance/fixtures/team/upstream/support/support-legal-compliance-checker.md`
10. `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/baseline/tests/acceptance/fixtures/team/upstream/LICENSE`
11. `/Users/fun/.codex/agents/design-ui-designer.toml`
12. `/Users/fun/.codex/agents/engineering-backend-architect.toml`
13. `/Users/fun/.codex/agents/engineering-devops-automator.toml`
14. `/Users/fun/.codex/agents/engineering-frontend-developer.toml`
15. `/Users/fun/.codex/agents/engineering-sre.toml`
16. `/Users/fun/.codex/agents/task-delegate.toml`
17. `/Users/fun/.codex/agents/task-execute.toml`
18. `/Users/fun/.codex/agents/task-review.toml`
19. `/Users/fun/.codex/agents/task-scan.toml`
20. `/Users/fun/.codex/agents/testing-api-tester.toml`

实际写入仅为本独占方案报告 `red-plan.md`；没有修改上述已读文件、项目配置、共享产出或 Git 状态。
