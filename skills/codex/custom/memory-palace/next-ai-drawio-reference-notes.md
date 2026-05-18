# next-ai-draw-io 参考吸收笔记

更新时间：2026-05-12
参考项目：DayuanJiang/next-ai-draw-io
上游地址：https://github.com/DayuanJiang/next-ai-draw-io
吸收原则：学习可编辑图表生成流程；外部项目只引用或按需调用，不内嵌为本 SKILL 的代码副本。

## 1. 关键发现

### M-20260512-001：细节图表优先使用可编辑 draw.io XML

- 状态：active
- 区域：门厅
- 标签：#图表 #drawio #架构图 #流程图
- 触发场景：用户要求生成细节点流程图、架构图、系统图、云架构图、泳道图、ER 图或需要后续编辑的图表时
- 记忆内容：next-ai-draw-io 的核心价值是生成和编辑 draw.io XML，而不是输出静态图片。draw.io XML 可以继续在 draw.io/diagrams.net 中手工编辑、导出和迭代。
- 使用方式：本 SKILL 后续遇到复杂流程图或架构图时，优先产出可编辑图表方案；如果环境支持 draw.io/MCP，就优先使用 draw.io XML；如果只需要轻量说明，才使用 Mermaid。
- 来源：`README.md`、`lib/system-prompts.ts`
- 更新时间：2026-05-12

### M-20260512-002：图表生成前必须先规划布局

- 状态：active
- 区域：工坊
- 标签：#图表 #布局 #流程 #质量
- 触发场景：生成包含多个节点、容器、箭头或跨层关系的图表时
- 记忆内容：next-ai-draw-io 的 prompt 强调先用 2-3 句规划布局和结构，避免对象重叠、边穿过对象、元素超出页面。复杂图需要先确定方向、分层、分组、间距和连接规则。
- 使用方式：生成细节图表前，先写“图表意图、布局方向、分组/泳道、关键连接、校验点”，再生成图表。
- 来源：`lib/system-prompts.ts`
- 更新时间：2026-05-12

### M-20260512-003：新图和编辑图要用不同策略

- 状态：active
- 区域：工坊
- 标签：#图表 #编辑 #drawio #流程
- 触发场景：用户要求修改已有图、补充节点、调整标签、移动元素或重构图表时
- 记忆内容：next-ai-draw-io 区分新建图和编辑图。新建图可以整体生成；修改已有图应优先使用 ID 级操作更新、添加或删除具体 cell，避免重建导致用户手工修改丢失。
- 使用方式：如果已有图表，先读取当前 XML 或结构，再做小范围 ID 级修改；只有用户要求重做或结构完全变化时才整体重建。
- 来源：`packages/mcp-server/src/index.ts`、`packages/mcp-server/src/diagram-operations.ts`
- 更新时间：2026-05-12

### M-20260512-004：图表输出必须校验 XML 和视觉质量

- 状态：active
- 区域：警示墙
- 标签：#图表 #校验 #XML #风险
- 触发场景：生成 draw.io XML、修改图表或准备交付图表文件时
- 记忆内容：next-ai-draw-io 对 XML 做结构校验，包括重复 ID、标签闭合、实体转义、嵌套 mxCell、source/target 引用等；还支持视觉校验，检查重叠、遮挡、布局问题并重试修复。
- 使用方式：本 SKILL 的图表流程应加入“结构校验 + 视觉校验 + 修复记录”。不能只看 XML 是否生成，还要确认图能打开、能编辑、文字不重叠、箭头不穿过节点。
- 来源：`lib/diagram-validator.ts`、`lib/validation-schema.ts`、`packages/mcp-server/src/xml-validation.ts`
- 更新时间：2026-05-12

## 2. 可吸收设计

- 图表产物优先级：可编辑 draw.io XML > Mermaid > 静态图片。
- 新建图：先规划布局，再生成完整结构。
- 编辑图：先读取当前图，再用 ID 级 update/add/delete 操作。
- 云架构和专业图标：先查 shape library，不猜图标语法。
- 质量边界：单页视口、合理边距、节点不重叠、箭头绕障、连接点自然。
- 历史保护：每次 AI 编辑前保留上一个版本，方便回退。

## 3. 不直接照搬内容

- 不把 next-ai-draw-io 的 Next.js 应用作为本 SKILL 的运行依赖。
- 不要求所有图都用 draw.io；轻量文本说明、简单状态流仍可用 Mermaid。
- 不复制系统 prompt 全文，只吸收图表生成流程、校验规则和编辑策略。
- 不默认调用外部 AI provider；本 SKILL 只记录方法、引用地址和适用规则。

## 4. 本轮建议改进

- 在主规范增加“细节图表生成协议”。
- 在主规范增加“draw.io 与 Mermaid 的选择规则”。
- 在模板增加图表产物字段和图表质量检查。
- 在索引登记 next-ai-draw-io 参考仓库。
