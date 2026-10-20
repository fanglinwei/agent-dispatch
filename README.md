# Agent Dispatch

Agent Dispatch 帮你在 Codex 中确认需求、配置专业岗位，并组织团队编写和复核实施文档。适用于软件、研究、内容、运营等项目，支持首次配置和后续增岗。

| Skill | 适用场景 | 交付内容 |
| --- | --- | --- |
| `agent-dispatch` | 新项目配置团队，或为已有团队补充职责 | 岗位配置、职责与协作规则、任务 Skill 使用要求、项目记忆。 |
| `agent-dispatch-doc` | 已有合适团队，需要制定或更新实施安排 | 各岗位编写和复核的实施文档，确认内容后供后续任务使用。 |

当前版本 **v1.2.0**：按需求选择访谈方法，支持领域术语和重要决策记录。变更见 [CHANGELOG](CHANGELOG.md)。

## 功能特点

- 从 [agency-agents](https://github.com/msitarzewski/agency-agents) 选择所需岗位，按职责确定团队规模。主代理先检查已有分工，增岗时保留原有模型、定制与经验。
- 需求访谈按场景选择 Skill：用 `grill-me` 追问功能与方案中的遗漏；需要澄清业务概念、核对现有实现并记录术语和决策时，用 `grill-with-docs`。切换时沿用已确认的答案。
- 为任务指定负责人和复核者，约定交接、Skill 使用与验收要求。主代理负责整合和最终判断。
- 各岗位提供专业内容，并复核整合后的文档。你确认草案内容后，团队才将其作为实施依据；后续按变更维护。
- 角色在执行中核实并纠正错误，向主代理交接有依据的新经验。主代理将经验保存在项目文件中，供后续任务读取。

请明确调用所需 Skill。开发、制作、发布及 Git 写操作需要后续任务的授权。

## 安装

选择一种安装方式，避免重复安装同名 Skill。

### Codex 插件

需要支持 `codex plugin` 的 Codex CLI：

```sh
codex plugin marketplace add fanglinwei/agent-dispatch
codex plugin add agent-dispatch@agent-dispatch
```

安装后新开会话，从技能选择器中选择对应入口。名称以会话显示为准，例如 `agent-dispatch:agent-dispatch` 和 `agent-dispatch:agent-dispatch-doc`。

### 独立 Skill

需要 Node.js/npm，通过 [Skills CLI](https://github.com/vercel-labs/skills) 安装：

```sh
npx skills add fanglinwei/agent-dispatch --skill agent-dispatch --skill agent-dispatch-doc --agent codex --global
```

单独安装时，保留所需的 `--skill` 参数。切换安装方式前，备份并停用旧入口。其他宿主尚未验证。

## 使用

在目标项目中打开 Codex。以下示例使用独立 Skill 名称；插件安装时从技能选择器选择对应入口。

新项目配置团队：

```text
$agent-dispatch 我要做一个面向独立开发者的反馈管理工具。先帮我确认需求，再配置合适的团队、职责和任务技能。
```

已有项目补充职责：

```text
$agent-dispatch 项目现在要接入支付。检查已有团队，补齐缺少的职责，保留现有配置。
```

由已有团队编写实施文档：

```text
$agent-dispatch-doc 根据已确认需求，由当前团队共同编写和复核实施文档，经我确认后作为实施依据。
```

主代理会先展示岗位或文档方案，列明范围、职责和写入路径，你确认后再写入。实施文档还需经过专业复核和你的内容确认；确认方案不等于接受尚未写出的文档。

## 职责与限制

两个 Skill 可单独安装。已有合适团队时，你可以使用 `agent-dispatch-doc`；需要选岗、增岗或调整职责时，先用 `agent-dispatch` 完成配置。文档 Skill 不负责更改团队分工。

本工具不捆绑 `grill-me`、`grill-with-docs` 等外部技能。主代理会核实入口与依赖；推荐能力缺失时，说明后采用内置分轮访谈。若你或项目要求某项能力必用且不可替代，主代理会将受影响部分标为 `PARTIAL`（尚未完成）。

使用 `grill-with-docs` 时，代理会在授权范围内维护术语表和符合条件的重要决策记录（ADR）。完整实施文档由 `agent-dispatch-doc` 组织团队编写。

项目记忆默认保存在 `.codex/agent-memory/`，主代理在 `AGENTS.md` 中记录岗位和记忆路径；项目已有等效结构时优先沿用。角色读取相关经验，主代理在授权范围内统一保存。这套记忆不修改模型权重，也不启动后台服务。记忆不增加写入权限，只读任务默认返回待保存内容。详见[项目岗位学习配置](skills/agent-dispatch/references/project-learning.md)。

## 维护与验证

`skills/` 存放技能源码。运行本地检查：

```sh
npm test
```

`npm test` 检查包结构、元数据、引用和已保存的行为验收证据，不调用模型。修改技能后，维护者还需重跑受影响的行为验收。方法与覆盖范围见[隔离行为验收](tests/acceptance/README.md)。

详细规则：[团队配置](skills/agent-dispatch/SKILL.md) · [需求访谈](skills/agent-dispatch/references/interview.md) · [团队文档](skills/agent-dispatch-doc/SKILL.md)。

## 来源与许可

主代理从 [agency-agents](https://github.com/msitarzewski/agency-agents) 选岗，采用时固定版本并保留许可。测试中的岗位样本仅供验收。

协作与验收方法参考 [squad-skills](https://github.com/danh121097/squad-skills)。

本项目使用 [MIT 许可证](LICENSE)。引用的上游材料保留各自许可与署名。
