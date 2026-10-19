# 文档方案

读取 fixture 的现有五岗、AGENTS.md、最新目标与实际事实。既有团队完整复用，角色和 Skill 绑定不改。
共享写入仅由主代理完成：docs/implementation.md 为具体实施设计，docs/README.md 为单一状态入口；旧材料保留。
产品负责 R1～R6 流程与范围；UI 使用 visual-layout 定义组件与状态；前端定义 Vue/TS、接口适配及失败恢复；QA 规划容量、错误、重复提交与验收证据；审查岗位编写缺陷检查方法，不执行代码审查，不因 defect-evidence 缺失阻断文档。五岗各供稿并对整合版实际复核。
当前为文档设计检查，不执行应用、支付或数据操作。每岗独占 contributions/<role>.md 与 reviews/<role>.md，其余只读；共享契约由主代理先统一，再检查岗位之间的生产与消费关系。
专业复核通过也保持 DRAFT，模拟内容确认后才可修改 docs/README.md 和 AGENTS.md 中的实施入口。

模拟用户：我确认以上文件方案，允许在此隔离工作区编写与专业复核；尚未确认最终内容。
