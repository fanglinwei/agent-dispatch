# 文档方案

输入：documents/ 下的已确认目标、事实、团队、技能与旧设计。
产出：documents/docs/implementation.md（新实施设计草案）和 documents/docs/README.md（草案索引），唯一写入者为主代理。保留旧文档和所有岗位文件；内容确认前不修改 AGENTS.md 实施入口。
五个岗位各自供稿至 contributions/<岗位名>.md 并复核整合版：product_owner 定义范围、流程、R1~R6需求；ui_owner 依 visual-layout 设计页面和状态；frontend_owner 定义 Vue 状态、API契约、错误恢复；delivery_qa 定义可执行用例与证据门槛；code_auditor 定义后续只读代码审查方法。本次不做实际代码审查或项目开发。
R1活动列表；R2详情；R3表单校验；R4容量满；R5报名结果；R6网络失败重试并保留输入。无本阶段构建/执行记录，不继承旧 React/失败清空/PASS。
各岗位具体工作含责任边界、输入/前置、设计/方法、输出/交接、依赖/顺序、完成条件、未知项。主代理集成后各岗复核，未决设计明确标建议；新内容均 DRAFT，专业复核不代替用户内容确认。后续模拟内容确认单独记录并在隔离副本测试升基线，不能外推到实际用户项目。
