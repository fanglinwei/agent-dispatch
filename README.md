# Agent Dispatch

当前版本 **v1.1.0**：新增项目独立的岗位学习、执行中纠错与后续任务复用，并完善协作复核和安全保存约定。完整变更见[更新记录](CHANGELOG.md)。

面向各类项目的团队配置与实施文档工具。插件名为 `agent-dispatch`，包含两个显式调用的 Skill：

| Skill | 工作内容 |
| --- | --- |
| `agent-dispatch` | 需求访谈、交付目标、从 agency-agents 选岗、后续增岗、职责交接与任务 Skill 使用规则。 |
| `agent-dispatch-doc` | 核对已有团队，组织各岗位编写、复核和维护新的实施文档，经用户确认后作为实施依据。 |

文档 Skill 不自行增岗，也不要求另一个 Skill 同时安装。团队缺失或需要重分职责时，先完成团队配置；已有合适团队可直接使用文档 Skill。两者均不自动启动项目开发、发布或 Git 写操作。

源码与安装结构参考 [Ponytail v5.3.2，提交 16352ac](https://github.com/DietrichGebert/ponytail/tree/16352ac229eb08a9598dcae48fe9f2b342567d86)：`skills/` 是唯一技能源目录，`.codex-plugin/plugin.json` 声明插件，`.agents/plugins/marketplace.json` 提供 Codex 安装入口。插件与独立安装复用相同技能内容；本工具按用户要求显式调用，不需要自动注入或生命周期 hooks。

## 安装

安装方式与 Ponytail 保持一致：Codex 插件使用原生 marketplace 命令，独立 Skill 使用标准 Skills CLI。插件方式需要支持 `codex plugin` 的 Codex CLI；Skills CLI 方式需要 Node.js/npm。两种方式使用同一份 `skills/` 内容，选择一种启用，避免重复入口。

**Codex 插件方式**：通过 GitHub 仓库提供的 marketplace 安装：

```sh
codex plugin marketplace add fanglinwei/agent-dispatch
codex plugin add agent-dispatch@agent-dispatch
```

**独立 Skill 方式**：使用 Ponytail 同样采用的标准 [Skills CLI](https://github.com/vercel-labs/skills)。以下命令安装两个用户级技能；可只保留一个 `--skill` 以单装：

```sh
npx skills add fanglinwei/agent-dispatch --skill agent-dispatch --skill agent-dispatch-doc --agent codex --global
```

Skills CLI 当前将 Codex 用户级技能安装到 `~/.agents/skills`。项目岗位输出与原生加载按 Codex 规则核对，其他宿主未验证。

从独立 Skill 切换为插件时，先核对 `CODEX_HOME/skills`（默认 `~/.codex/skills`）、`~/.agents/skills` 及自己的其他安装位置，把同名技能备份到技能目录之外并停用。从插件切换为独立 Skill 时，先执行 `codex plugin remove agent-dispatch@agent-dispatch`。备份与恢复自行保留原路径，原生命令和 Skills CLI 不包含本工具的自动迁移或回滚流程。

安装完成后重启 Codex 或新开会话。原生安装状态可用以下命令核对：

```sh
codex plugin list --marketplace agent-dispatch --json
```

插件安装、启用、技能被会话加载以及项目岗位配置是不同状态。技能内容的显式策略在各自 `agents/openai.yaml` 中；不靠插件安装自动运行它们。

## 使用

独立安装时显式调用：

```text
$agent-dispatch 根据当前项目目标配置团队与职责，检查已有岗位和适用技能。
$agent-dispatch-doc 由当前项目团队编写新的实施文档，经我确认后作为实施依据。
```

插件方式在技能选择器中选择对应入口，宿主可能显示 `agent-dispatch:agent-dispatch` 和 `agent-dispatch:agent-dispatch-doc` 等限定名称；以新会话实际注册名称为准。用户也可明确要求使用插件内对应 Skill。

团队配置尽量保留上游原岗，以项目职责和精确任务分工减少重叠。岗位 Skill 绑定按任务触发，例如浏览器页面设计使用已确认的 `frontend-design`，实际代码审查使用 `code-review`；可用性、依赖和权限均现场核对。工具不捆绑这些外部技能，`grill-me` 缺失时使用内置访谈方法继续。

文档要求各岗位实际参与、共享文件唯一写入者、输入输出与交接清晰。深度参考三国霸业的产品、规则、技术、UI/美术、实施与验收体系，适配不同项目，不固定六份文件。旧文档仅供背景核实，新文档先为草案，经专业复核与用户内容确认后才替换实施入口。

团队配置现在同时建立项目独立的岗位学习：`AGENTS.md` 记录稳定岗位标识与路径，角色保留完整专业正文并追加读取指引，`.codex/agent-memory/protocol.md` 保存项目内运行约定，`<role-key>.md` 保存该岗记忆。归档有实际需要时才创建。已有等效结构优先沿用；旧项目在下次显式配置时补齐，保留模型、定制与已有经验。

配置前核对协议、记忆、归档和暂存路径不冲突。默认布局的新岗位避开 `protocol` 保留名，已有稳定标识通过实际路径映射保留。保存记忆及归档时，在已获准的同目录 `<目标路径>.pending` 独占暂存完整结果，验证后原子替换并回读；不原地覆盖唯一有效记录。暂存路径也需精确授权，旧授权仅含目标时保持待保存。此流程保护单写者下的进程中断，不承诺所有文件系统的断电或硬件故障恢复。

角色在任务开始时读取相关记忆，执行中失败或收到纠正时立即核实、修正和验证，结束时简短复盘；重复错误、明显知识缺口或职责冲突在已触发任务内深入处理。没有新增认识就不写记忆。角色提交增量，主代理在当前授权内串行合并、去重并整体回读；下一任务的新上下文从项目入口读取并复用。草案、未验证推断与环境/权限缺口分别处理，记忆不能改变正式职责或授予新权限。

这套学习通过项目文件与任务交接执行，不修改模型权重、不启用后台服务或 hooks。首版以同一工作区一个主代理维护为前提，不提供多主并发锁，也不保证恢复尚未交接的上下文。只读任务默认仅返回待保存增量；有适用于本次任务的明确保存例外才写精确路径。原任务完成、学习保存及条目是否有效分别报告，学习不重置两轮返工或扩张任务。配置阶段不试运行项目任务，宿主加载与实际学习闭环需要分别验证。

协作规则按变更风险区分 `light / standard / high` 检查强度，分别说明结果验证和专业复核；记录结论、证据版本与缺口，只复核修订影响的范围。同一验收单元默认最多两轮合并返工，未解决阻塞交主代理裁决，非阻塞建议不扩大返工。实施文档还检查上下游契约，未来环境缺失与当前文档检查分别记载。这些方法参考 [squad-skills](https://github.com/danh121097/squad-skills)，仍遵守本工具的显式调用、配置/文档边界及原有授权规则，不增加固定角色或模型默认值。

## 维护与验证

每个 Skill 的引用资源都包含在自身目录中，可独立分发。插件通过 `.codex-plugin/plugin.json` 声明这两个目录；marketplace 通过 `.agents/plugins/marketplace.json` 从 GitHub `main` 分支提供插件。分发新版本时更新插件版本并通过原生安装流程核对结果；固定版本源码见 [Releases](https://github.com/fanglinwei/agent-dispatch/releases)。

变更后核对插件与 marketplace 的 JSON、两个技能的必需文件、自包含引用和显式调用策略，再通过原生安装状态及实际技能列表确认入口。技能行为需要另行用实际项目或隔离情景核对，语法校验不能证明团队或项目已交付。

测试脚本与 Ponytail 一致，使用 `tests/*.test.js`、Node.js 原生 `node:test` 和 `node:assert/strict`，通过 `npm test` 运行，无第三方测试依赖：

```sh
npm test
```

测试覆盖包与插件的版本一致、marketplace 与技能导出的对应关系、分别独立安装两个技能后的本地引用，以及两个 Skill 的必需元数据、名称和 `allow_implicit_invocation: false`；学习断言还核对实际稿件、来源哈希、保存回执、新上下文身份、无增量时字节不变、旧角色迁移与改名、只读项目完整树及边界情景证据。元数据检查限定本仓库的固定 YAML 布局和 JSON 兼容引号字符串；调整布局时需同步测试，并用 Codex 原生加载核实，不把它当成通用 YAML 解析器。

[隔离行为验收](tests/acceptance/README.md)提供首次选岗、实际增岗、保留定制、重复调用、全团队文档供稿/复核、内容确认及学习闭环的可重放项目。`npm test` 离线检查保存的真实岗位、文档与定向复核证据，并拒绝与当前技能、输入或产物不符的记录；它不自动调用模型。修改技能后重跑受影响流程，仍适用的历史专业证据保留原身份、时间和来源版本，不冒充本次新调用。原有中断与归档情景使用预置状态验证决策；路径与安全保存修复另以独立代理实际产出的代码，在隔离子进程中检验替换前/后的进程中断。后续恢复验收由新进程接手真实残留，检查恢复、重试去重、只读及已有归档的两步提交故障；这些存储实验不外推为新模型上下文自主恢复、断电、多主并发或跨文件事务保障。文档专业质量由岗位及主代理实际复核，单次学习样本不证明长期效果。验收中的用户确认均明确标为模拟，不表示真实用户已批准项目实施内容。

岗位来源为 [agency-agents](https://github.com/msitarzewski/agency-agents)；技能内容不预置其岗位正文，使用时固定来源版本并保留对应许可。测试目录包含选定岗位的固定原件、完整许可与隔离产物，仅用于验收，不作为用户项目的默认团队。插件结构与安装参见 [OpenAI 插件文档](https://developers.openai.com/plugins/build/plugins)。

## 许可

本项目原创内容使用 [MIT 许可证](LICENSE)，版权所有 © 2026 fanglinwei。测试中引用的 agency-agents 岗位及衍生产物保留各自的上游 MIT 许可证与署名。
