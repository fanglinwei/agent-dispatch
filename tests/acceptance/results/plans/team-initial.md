# 首次团队配置方案（待批准方案，尚未写入配置）

本方案针对空项目 `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/team-project`。下文项目相对路径均以该绝对根为基准。这里提交的是完整可审阅方案；本次行为测试不等待批准、不写入项目配置，实际配置文件均由主代理在完整方案获得明确批准后生成。模拟用户尚未批准；fixture 中“可以在看到完整方案后批准”不构成预先授权。

## 已确认目标与本阶段完成标准

面向社区居民交付四期活动周刊，每周一期 Markdown，每期三篇，共十二篇。每期包括活动摘要、报名须知、来源清单与下期计划；以社区提供的已授权活动资料为依据，语气友好清晰，便于手机阅读。主代理负责统筹。

本阶段只完成必要岗位与协作、Skill 使用和项目学习配置。完成标准是：岗位来源固定且许可完整；一个成果有一个主责；周刊所有组成有责任覆盖；项目入口、角色 TOML、学习协议和空记忆结构完整且相互引用正确；格式校验与正文保真检查有证据，原生加载状态如实报告。周刊创作、实施文档、发布和 Git 写操作均没有在本阶段获得授权。本次配置获批也不自动启动这些工作。

`grill-me` 按已给定场景不可用。本轮采用 agent-dispatch 的 `references/interview.md` 分轮方法；目标、受众、工作、载体、风格、交付程度和边界均已明确，没有需要重复提问的分工决定。本文中的文件名、稳定标识及检查安排属于待批准的代理建议，不冒充用户原话。

## 岗位方案与来源

新增且只新增 **Content Creator**。保留上游原名、原 description 和完整专业正文，用于每期选题与篇目安排、三篇内容的撰写编辑、活动摘要和报名须知、来源清单、下期计划与 Markdown 阅读质量。上游正文实际包含内容策略、长文内容、品牌语气、平台适配等能力，足以覆盖本需求。主代理保留目标与排期裁决、材料与授权边界核对、最终整合、关键事实证据复核和完成判断，故不增加统筹岗。

上游固定为 `agency-agents` 提交 `652b2692f8d8ec2b1f1a38e559073e287dfdc469`，采用文件 `marketing/marketing-content-creator.md`：

- 固定来源链接：<https://github.com/msitarzewski/agency-agents/blob/652b2692f8d8ec2b1f1a38e559073e287dfdc469/marketing/marketing-content-creator.md>
- 本次读取副本：`/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/acceptance/fixtures/team/upstream/marketing/marketing-content-creator.md`。
- SHA-256：`26ddce44f057068a3935c13d53becd3c57385fb47fcdcfdd891b80269070b3d5`，与 `source.json` 一致。
- 保留的 description：`Expert content strategist and creator for multi-platform campaigns. Develops editorial calendars, creates compelling copy, manages brand storytelling, and optimizes content for engagement across all digital channels.`

已读取另一候选 **Legal Compliance Checker**，其职责涉及跨法域合规、法律风险、政策与法规框架；当前任务是基于社区已授权资料制作小型活动周刊，未出现需单设该岗的具体交付责任，因此不集成。若后续资料引出真实授权争议或需法律判断，由主代理核对受影响任务并正式调整配置，不能因上游候选存在就扩充岗位。

本模拟项目没有已有岗位或定制。已检查可见用户级 TOML 的 `name`，未见 `Content Creator`；当前宿主公开的内置/注册角色名也未见同名。该检查不等于目标项目新角色已被宿主加载；后者留待实际配置后的只读列出或新会话核对。

## 精确拟变更清单

以下五个文件均由主代理独占写入，本次执行者不创建它们：

| 精确路径 | 拟写入内容 |
| --- | --- |
| `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/team-project/AGENTS.md` | 一个集中项目协作区块：目标、调用条件、成果主责、派发契约、权限、Skill 规则、学习入口与稳定映射、检查与返工规则。配置时保留任何届时已存在的规则。 |
| `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/team-project/.codex/agents/marketing-content-creator.toml` | `name`、`description`、`developer_instructions` 三个非空字符串；完整专业正文之后追加本文所列短指引。注释记录固定来源、许可位置及真实适配。 |
| `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/team-project/.codex/agents/LICENSE.agency-agents` | 逐字保存同一固定快照的完整 MIT License 与 `Copyright (c) 2025 AgentLand Contributors`。 |
| `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/team-project/.codex/agent-memory/protocol.md` | 逐字复制本次实际读取的 `assets/learning-protocol.md`，形成项目自包含的协议，协议版本 1。 |
| `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/team-project/.codex/agent-memory/marketing-content-creator.md` | 按实际读取的 `assets/role-memory.md` 初始化空记忆，稳定标识替换为 `marketing-content-creator`，初始 revision 0。 |

预先约定但本次不创建的按需归档精确路径是 `/var/folders/f8/xps48s6x0y18qc9vrcm_b0d80000gn/T/agent-learning-vt_gjmvk/team-project/.codex/agent-memory/archive/marketing-content-creator.md`。没有归档需求不建空目录或文件。不创建 `.codex/config.toml`，不写入未经支持的 `memory`、`learning`、`skills` 等原生字段，不安装上游批量脚本。

角色 TOML 保留上游名称和描述；Markdown frontmatter 中的 tools、color、emoji、vibe 属于展示/来源元数据，不转为 Codex 原生配置。上游完整专业正文保留，营销增长等通用成功指标不替代本项目已确认的十二篇内容及来源可核对的验收要求，专业能力和外部操作也不构成执行授权。新角色省略模型和 effort，实际派发继续服从目标环境现有模型选择规则；省略字段不证明运行模型身份。本方案不检查或变更用户级模型设置。

拟追加在角色完整正文之后的短指引为：

> 项目规则入口：开始任务前读取获准项目根的 AGENTS.md，按本次任务触发条件遵守其中的 Skill 使用规则、正式分工和精确读写授权。
>
> 项目学习入口：以本次获准项目根为基准，先读取 AGENTS.md 的岗位映射与 .codex/agent-memory/protocol.md，再实际读取 .codex/agent-memory/marketing-content-creator.md；稳定 role-key 为 marketing-content-creator。按协议在任务中核实纠错并交接增量，当前授权及正式职责优先。记忆缺失时报告并依权威材料继续，不自行迁移配置或写共享记忆。

来源注释会明确写成“保留上游完整专业正文，追加项目规则与学习入口”，不声称只有格式转换。源正文和项目附加正文可分段定位核对。

## 日常协作、调用与成果主责

| 责任或成果 | 主责与调用条件 | 交接与边界 |
| --- | --- | --- |
| 项目目标、优先级与每期排期 | 主代理；后续用户授权具体周刊任务时组织 | 确定当期可用资料、三篇范围和任务级输出路径；材料不足只暂停受影响篇目或事实，不补造活动信息。 |
| 当期三篇正文及其四类组成 | Content Creator；明确授权当期策划、创作、修改或内容检查时调用 | 在获准独占产物中完成活动摘要、报名须知、来源清单及下期计划，标明资料来源与不确定点。主代理指定单一最终 Markdown 文件写入者；多人输入时只在各自独占位置返回意见或草稿。 |
| 结果符合性和最终内容质量 | 主代理；角色提交后核对 | 核对三篇与四类组成、活动时间地点/报名条件等关键事实与来源对应、友好语气、手机阅读性及范围边界；失败汇总交回 Content Creator 修复。该检查属于主代理复核，不冒充独立岗位检查。 |
| 配置文件、项目协作规则、学习记忆与整合 | 主代理唯一写入者 | 岗位代理只返回输入、产物和学习增量；职责/Skill/协议/角色配置的正式变更仍走显式配置流程。 |

不将上表中的默认维护责任解释为整目录写权限。当前阶段不预先创建周刊草稿、来源台账、进度文档或实施文档。后续每期任务开始时由主代理给出真实资料及精确读写路径；未分配的路径无默认写入权。配置可批准主代理按任务需要调用本岗，但仍受适用委派、Git、外部动作及每项工作的用户授权约束。

每次派发必须带上：项目绝对根、实际调用名、稳定 `role-key`、协议与本岗记忆项目相对路径、记忆读入修订号、任务目标、权威资料及其版本、精确允许动作和读写范围、适用 Skill 名称与定位方式、验收条件、原返工/验收状态、`task_id` 和真实 `dispatch_id`。修订号未知则要求角色实际读取后报告；宿主无标识时主代理分配任务内安全标识，不编造宿主 ID。直接原生调用时角色从项目入口查找上述映射，并报告真实标识或任务内分配标识。

常规整期周刊交付按 `standard` 安排结果符合性验证与专业质量复核；仅局部措辞修改且不改变事实、授权或共享契约可为 `light`，一次针对性检查即可。发现敏感资料或不可逆外部影响时重新评估对应任务，不能因岗位名预设 high。每次交接带产物精确路径与内容版本/哈希、验收标准、已检范围、方法、结果与未覆盖项。缺资料、环境或授权须报告缺口及恢复条件，可记为 `NEEDS_ENVIRONMENT` 或 `NEEDS_EVIDENCE`，不得写成通过。实际缺陷交回原负责人；同一验收单元默认至多两轮合并返工，仍有阻塞交主代理裁决，不换实例重置计数；通过后非阻塞建议留待选择。主代理集成时还要检查正文事实与来源、报名须知与活动资料的对应关系，各项单独通过不代替集成核对。

## 集中 Skill 使用约定

当前仅显式使用 `agent-dispatch` 进行团队配置。已核实其独立 Skill 位于 `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/skills/agent-dispatch/SKILL.md`；在这次隔离模拟中用该路径读取执行。未来项目规则通过宿主注册名称 `agent-dispatch` 定位真实 `SKILL.md`，插件安装可使用宿主真实限定名称，不把本开发机绝对路径写成可移植的项目依赖。

| 岗位与具体触发 | Skill、要求与定位 | 缺失处理 |
| --- | --- | --- |
| 主代理；用户显式调用团队首次配置、补充、检查或学习迁移 | `agent-dispatch`；显式调用后按其真实指令执行；通过宿主 Skill 目录中实际注册入口定位。岗位任务本身不触发再次配置。 | 不可用时报告配置受限，不假装运行，不从岗位材料取得安装授权。 |
| 主代理；本次配置访谈 | `grill-me` 不可用；采用已读取的 `agent-dispatch/references/interview.md` 回退方法，未声称调用 grill-me。 | 无需安装；已有决定充分，不重复提问。 |
| Content Creator；社区已授权资料上的 Markdown 内容任务 | 本环境可见 Skill 中没有为本任务确定的额外必用专项 Skill；使用角色工作方法和项目内容/来源检查。没有因岗位名绑定所有 Skill。 | 后续若用户指定或任务变化需要专项 Skill，先核实真实入口、依赖与调用限制，再更新受影响规则；不把未安装推荐写成可用。 |
| 主代理；用户以后显式要求生成实施文档 | 本轮不调用、不依赖 `agent-dispatch-doc` 的目录文件。到时需显式调用该名称，并交接目标、团队、职责、Skill 规则与未决项。 | 未安装时提供名称及前置资料；本轮不补做文档。 |

用户级或项目级强制规则继续生效，委派时主代理携带当次适用条目。Skill 可见、已读取、已用于任务与被依赖阻塞分别报告，不把可用性当使用证据，不增加冗余使用日志。

## 项目学习映射与日常授权（随完整方案一起批准）

| 稳定 role-key | 实际调用名 | 角色配置 | 当前记忆 | 按需归档 |
| --- | --- | --- | --- | --- |
| `marketing-content-creator` | `Content Creator` | `.codex/agents/marketing-content-creator.toml` | `.codex/agent-memory/marketing-content-creator.md` | `.codex/agent-memory/archive/marketing-content-creator.md` |

学习协议为 `.codex/agent-memory/protocol.md`，项目入口为 `AGENTS.md`。岗位开始任务前必须实际读取入口、协议与本岗相关记忆，报告读入修订和来源适用性；执行失败或收到纠正时立即核实问题与依据，在本次授权内纠正并做针对性验证；结束时简短复盘，将有效增量随交接返回。Q3 只有开始、失败/纠正、完成三个触发点，出现重复错误/知识缺口/职责冲突时深入处理受影响部分；不增加逐步、定时、后台学习触发器，不扩大扫描或返工范围。

**精确权限：** 岗位只读上述项目入口、协议、本岗记忆及本次获准材料，只写每次派发分配的独占任务产物；不直接写共享记忆、归档或代理配置。完整方案获批后，主代理获得在普通可写任务中串行合并日常增量的持续授权，且仅限 `.codex/agent-memory/marketing-content-creator.md` 和按需 `.codex/agent-memory/archive/marketing-content-creator.md`。这不是修改协议、角色 TOML 或正式职责的日常授权。协议和角色配置变化仍需配置授权。

**当前只读优先：** 未来任务或适用 Skill 明确只读时，角色与主代理均仅返回待保存增量，不落盘记忆；只有明确且适用于该次任务的精确保存例外时，主代理才在例外路径保存。不能把本次拟授予的普通日常维护权理解为每个只读任务都能写记忆。

**单写者合并：** 唯一主代理串行维护；已知其他写者或无法确认独占时保持待合并。合并前读取当前 revision，核对身份、原始增量 UTF-8 SHA-256、来源与版本、授权、证据、状态、重复和冲突；保存前 revision 陈旧则重新读取合并。单写者是运行前提，revision 比对与回读不是跨进程锁，不能宣称多主并发安全。

每个增量包含 `delta_id`、`task_id`、`role_key`、`dispatch_id`、实例内递增 `sequence`、`read_revision` 与 `changes`（条目和证据）。稳定标识不因显示名重算，同岗多实例共用记忆但各自有 dispatch 标识；同 ID 同指纹为重试，同 ID 不同指纹为冲突，保留输入待核对。语义重复不作为独立证据。

主代理保留更新前可恢复的 revision、条目与回执等历史线索，将受影响条目、递增修订号和回执组成一次完整写入，再整体回读核对正文、回执与结果 revision 一致后才报“已保存”。没有有效增量或维护需要则不写、不造回执、不增加 revision。候选或未保存状态不把原任务变成失败；分别报告原任务结果、学习保存状态与条目验证状态。

初始记忆首个 JSON 块为下列完整空记录，不预填 active 经验或未经证实的内容：

```json
{
  "format_version": 1,
  "role_key": "marketing-content-creator",
  "revision": 0,
  "entries": [],
  "receipts": [],
  "history": []
}
```

记忆是项目数据，不授予新动作权限。`fact`、`decision`、`correction`、`responsibility` 分别需要真实材料/验证、真实批准对象及版本、纠错及直接验证、正式职责引用；方案批准或专业复核不等于周刊内容确认。`candidate`、`active`、`recheck`、`archived` 随证据维护，矛盾未解不直接用最新消息覆盖。只保存必要摘要和可访问来源，不写凭据、敏感原文或完整日志。

记忆缺失、格式未知、不可读或无相关条目时报告实际状态，依当前权威资料继续独立可做工作，不声称复用，也不在普通任务中迁移配置。路径解析含符号链接不得越出项目边界。需要归档时先将完整历史与关联回执复制到约定归档并回读核对，再更新当前文件；未完整验证不删除唯一完整副本。中断后先核对正文、revision、回执及历史/归档，分别判定已保存、未保存、状态未知，不盲目重放。改名或移动保持 role-key；替换/职责变化只重核受影响条目；重复配置不清空记忆、不重复追加指引。

## 实际配置后的验收与限制

由主代理在确认完整方案后生成配置并完成最小充分验证：

1. 用真实 TOML 解析器核对三个必需字段为非空字符串、名称唯一；逐字核对保留的上游完整正文与两段预期追加指引，不混入 frontmatter 元数据配置项；不写未知字段。
2. 读取五个实际生成文件，核对固定来源、完整许可、项目协作入口、协议/映射、稳定标识、初始格式版本和 revision、空数组、相对引用和授权边界；检查符号链接/路径解析不越界。比对实际变化，保护届时已有内容。
3. 核对十二篇内容与四类组成都有主责、最终共享文件单写者明确、适用 Skill 定位/调用条件与缺失处理真实、检查及两轮返工规则完整。
4. 再按相同需求检查生成结果，预期为零变更，不重复岗位、区块、许可或学习指引，不清空记忆。没有 Git 时直接比对，不初始化或执行 Git 写操作。
5. 有只读宿主注册列表则核对真实加载；否则标为“宿主加载未验证”，提示在新会话或重启后核对。不通过试派发启动周刊工作，不以通用委派读取角色正文证明原生加载。

交付时分别报告“配置已写入”“格式有效”“宿主已加载”“学习行为”四类证据。当前仅方案完成，五个配置文件均未由本执行者写入，因而不能声称这些验证已通过。学习文件存在也不能证明纠错、持久化或新上下文复用已经发生；学习闭环须留到获准任务或隔离验收中证明。

## 本执行者已读取路径与实际核验

本次只读材料：

- `/Users/fun/.codex/skills/subagent-delegation/SKILL.md`（启动规则；没有派生代理或检查用户级模型）。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/skills/agent-dispatch/SKILL.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/skills/agent-dispatch/references/project-learning.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/skills/agent-dispatch/references/role-skills.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/skills/agent-dispatch/references/interview.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/skills/agent-dispatch/references/codex-project-agents.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/skills/agent-dispatch/assets/learning-protocol.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/skills/agent-dispatch/assets/role-memory.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/acceptance/fixtures/team/initial.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/acceptance/fixtures/team/source.json`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/acceptance/fixtures/team/upstream/marketing/marketing-content-creator.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/acceptance/fixtures/team/upstream/support/support-legal-compliance-checker.md`。
- `/Users/fun/Documents/ChatGPT/Skill/agent-dispatch/tests/acceptance/fixtures/team/upstream/LICENSE`。

只为角色重名检查以 `tomllib` 解析了以下可见用户级文件的 name 字段，没有使用其中正文作为项目需求，也没有改动：`/Users/fun/.codex/agents/design-ui-designer.toml`、`engineering-backend-architect.toml`、`engineering-devops-automator.toml`、`engineering-frontend-developer.toml`、`engineering-sre.toml`、`task-delegate.toml`、`task-execute.toml`、`task-review.toml`、`task-scan.toml`、`testing-api-tester.toml`（后九项均位于同一 `/Users/fun/.codex/agents/` 目录）。`/Users/fun/.agents/agents` 不存在，目录列举命令因此退出 1；该位置没有可读岗位，不影响已确认范围内的方案。

读取命令为 `cat`、`rg --files` 和只读 `ls`；来源校验使用 Python `hashlib.sha256` 比对 `source.json` 的三项文件，三项一致：内容岗 `26ddce44f057068a3935c13d53becd3c57385fb47fcdcfdd891b80269070b3d5`、合规岗 `08d938c5666e41b3cf197c2f7b37070d7f39aca62b7147d157200eb6dbeeced6`、许可 `9a45258434d5cedf0af73c9ad4771373701225038d246c49219026c33677f66f`，该 Python 命令退出 0。所有命令显式使用 `workdir: '/'`、`shell: '/bin/sh'`、`login: false`。

来源版本可信度限于本地副本与给定 source.json 一致；没有联网核验远端提交。目标项目为空及 grill-me 不可用取自模拟前提，不扩展扫描来重新证明。未读取 acceptance 预期、实现或其他 fixture，不猜测测试结果。没有生成配置、周刊、实施文档或归档，没有运行发布、Git 写操作或任何项目实际工作。唯一写入产物为本方案报告。

## 主代理采纳与模拟用户确认
为延续本验收既有配置命名，实际文件及稳定标识采用 content-creator，读取指引采用当前 assets/role-learning.txt 渲染值；其他范围沿用上述方案。模拟用户：已看到这份完整方案与命名调整，批准 AGENTS.md、.codex/agents/content-creator.toml、.codex/agents/LICENSE.agency-agents、.codex/agent-memory/protocol.md、.codex/agent-memory/content-creator.md，并批准主代理在普通可写任务维护本岗记忆及按需 archive/content-creator.md。此批准只适用于隔离模拟项目。
