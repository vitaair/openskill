# Next AI Draw.io 写作索引

更新时间：2026-05-12
来源项目：`<LOCAL_SKILL_WORKSPACE>/next-ai-draw-io`
抽象对象：`next-ai-draw-io` 的图表写作模型，不是应用运行手册

## 1. 这个 Skill 解决什么

把自然语言需求写成 AI 能稳定生成 draw.io 图表的内容，包括：

- 图表提示词
- 图表布局方案
- draw.io `mxCell` XML 片段
- 现有图表的 ID 级编辑指令
- 图标库选择说明
- 视觉校验和改进反馈
- 从图片、PDF、文本复刻图表的写作规范

## 2. 来自 next-ai-draw-io 的核心抽象

### D-001：先写布局计划

- 状态：active
- 触发场景：创建任何新图
- 内容：先用 2-3 句话说明布局方向、分区、节点密度和连线策略，再生成图表内容。
- 使用方式：不要直接堆节点；先决定左到右、上到下、泳道、网格、中心辐射或分层架构。

### D-002：生成模式和编辑模式分离

- 状态：active
- 触发场景：用户要新建图或修改旧图
- 内容：新图或大改用完整生成；小改用 ID 级操作。
- 使用方式：新建写 `mxCell`；修改写 `add/update/delete`，并引用当前图里的 cell ID。

### D-003：只写 mxCell 片段

- 状态：active
- 触发场景：为 next-ai-draw-io 或类似工具写 XML
- 内容：默认只输出 `mxCell` 元素。外层 wrapper 和 root cells 由工具补。
- 使用方式：除非明确要求 `.drawio` 文件，否则不要写 `<mxfile>`、`<mxGraphModel>`、`<root>`。

### D-004：视口和布局约束

- 状态：active
- 触发场景：任何图表
- 内容：所有元素保持在 x `0-800`、y `0-600` 的单页视口内。容器最大宽约 700，高约 550。
- 使用方式：从 x=40、y=40 左右开始；大图采用纵向堆叠、网格或分区，不横向铺太远。

### D-005：连线是图表质量的关键

- 状态：active
- 触发场景：有边、箭头、依赖、流向
- 内容：每条边应规划出口、入口和绕行点，避免穿过无关形状。
- 使用方式：边样式包含 `exitX`、`exitY`、`entryX`、`entryY`；复杂路径使用 `mxPoint` waypoints。

### D-006：图标库不猜

- 状态：active
- 触发场景：AWS、Azure、GCP、Kubernetes、BPMN、Material Design 等图
- 内容：写作时先声明需要查询或使用的 shape library。
- 使用方式：可用库包括 `aws4`、`azure2`、`gcp2`、`kubernetes`、`flowchart`、`bpmn`、`material_design`、`webicons` 等。

### D-007：视觉校验反馈要可执行

- 状态：active
- 触发场景：图表有遮挡、交叉、越界、层级不清、标签不可读
- 内容：反馈必须指出问题类型、位置、影响和修复建议。
- 使用方式：不要只说“不好看”；写“节点 A 到 C 的连线穿过 B，改为从 A 底部出线，经 y=360 绕行到 C 左侧”。

## 3. 图表类型写法

### 流程图

- 优先布局：上到下或左到右。
- 重点：开始/结束、判断分支、异常路径、回路。
- 写作要求：判断节点用菱形或明确标注；分支边标注条件。

### 架构图

- 优先布局：用户/客户端、入口层、服务层、数据层、外部依赖。
- 重点：边界、协议、数据流、同步/异步。
- 写作要求：容器表示系统边界，连接线标注请求、事件、数据。

### 云架构图

- 优先布局：区域/账号/VPC/子网/服务组。
- 重点：云厂商图标、网络边界、安全边界、托管服务。
- 写作要求：先声明 shape library，如 AWS 用 `aws4`。

### 时序/交互图

- 优先布局：参与者横向排列，时间纵向向下。
- 重点：请求、响应、异步事件、失败分支。
- 写作要求：避免线穿过生命线标签；消息边标清动作。

### 实体/领域模型

- 优先布局：核心实体居中，关系按聚合或依赖分区。
- 重点：实体、属性、关系、基数、约束。
- 写作要求：关系边标注 `1:N`、`belongs to`、`creates` 等。

### 文档/图片复刻

- 优先布局：保持原图方向、层级、线型和相对位置。
- 重点：形状、标签、颜色、线条曲直、容器边界。
- 写作要求：先描述观察结果，再写复刻方案。

## 4. XML 写作规则

### Shape

```xml
<mxCell id="2" value="Label" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

### Edge

```xml
<mxCell id="3" style="edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.5;entryX=0;entryY=0.5;endArrow=classic;html=1;" edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### Edge With Waypoints

```xml
<mxCell id="edge-1" style="edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.5;entryX=0;entryY=0.5;endArrow=classic;html=1;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="360" y="120"/>
      <mxPoint x="360" y="260"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## 5. 编辑操作写作规则

用于现有图表的小改：

```json
{
  "operations": [
    {
      "operation": "update",
      "cell_id": "service-api",
      "new_xml": "<mxCell id=\"service-api\" value=\"API Service\" style=\"rounded=1;whiteSpace=wrap;html=1;\" vertex=\"1\" parent=\"1\"><mxGeometry x=\"280\" y=\"160\" width=\"140\" height=\"60\" as=\"geometry\"/></mxCell>"
    }
  ]
}
```

要求：

- `update` 和 `add` 必须提供完整 `mxCell`。
- `delete` 只需要 `cell_id`。
- 不知道 ID 时，先要求读取当前 XML。
- JSON 字符串场景中，`new_xml` 内部引号需要转义。

## 6. 输出选择

用户要“帮我写提示词”：输出自然语言 prompt。

用户要“帮我设计图”：输出图表 brief。

用户要“直接给 XML”：输出 `mxCell` 片段。

用户要“修改这张图”：输出 edit operations。

用户要“检查这张图”：输出 validation feedback。

用户要“做成工具规则”：输出 agent/system prompt。

