# Draw.io 架构图参考库索引

更新时间：2026-05-14

本目录用于 SR-10 图示节点的本地参考。外部仓库只作为模板、图形语言和布局规则参考，不作为当前项目事实来源，不直接复制到提交材料中。

## 本地参考库

| 参考库 | 本地路径 | 上游来源 | 用途 | SR-10 适用方式 |
|---|---|---|---|---|
| drawio 官方示例/模板 | `vendor/diagram-references/drawio-diagrams` | `https://github.com/jgraph/drawio-diagrams` | 官方 `.drawio`/XML 示例、UML、数据流、信息图和架构类模板 | 参考页面结构、分组、箭头、标题区和图例做法 |
| drawio 官方图形库 | `vendor/diagram-references/drawio-libs` | `https://github.com/jgraph/drawio-libs` | diagrams.net 图形库、图标库、模板库 | 参考图形库和可复用图元，不强依赖在线导入 |
| C4 draw.io 模板 | `vendor/diagram-references/c4-draw.io` | `https://github.com/kaminzo/c4-draw.io` | C4 Model 语义、系统/容器/组件关系 | 用于软件系统架构、模块边界和关系命名，不直接套大数据平台总图 |
| ADF diagrams.net 元素 | `vendor/diagram-references/adf-diagramsnet` | `https://github.com/architecture-decomposition-framework/adf-diagramsnet` | ADF 架构分解元素和运行/设计视图库 | 用于规范化“层、环境、运行边界、依赖关系”的表达 |
| NextAIDrawIO 写作 Skill | `<LOCAL_SKILL_WORKSPACE>/NextAIDrawIO写作SKILL` | 本地 Skill | 图需求 brief、图片复刻 brief、mxCell 写作和视觉校验 | 作为生成规则，不复制 Skill 内容 |
| GitDiagram | `vendor/github-references/gitdiagram` | `https://github.com/ahmedkhaleel2004/gitdiagram` | 仓库结构到交互式架构图的生成流程 | 参考“仓库扫描 -> 结构化图模型 -> 校验 -> 渲染”的流程，不采用 Mermaid 正式输出 |
| OpenGithubs 项目索引 | `vendor/github-references/OpenGithubs`、`vendor/github-references/weekly`、`vendor/github-references/github-weekly-rank` | `https://github.com/OpenGithubs` | 开源项目发现、榜单和项目索引 | 作为外部参考项目清单来源，不作为图模板或项目事实来源 |

## SR-10 使用规则

1. 先判断图类型：平台总体架构、软件结构图、UML 活动图、逻辑框图、数据流向图、接口/模块映射图。
2. 若项目已有总体架构图或平台基础架构图，优先走“图片复刻 brief”：复刻版式、分区和层级，不复刻无关文字。
3. 若没有已有架构图，再从本地参考库选择模板风格：
   - 平台总图：优先参考 `drawio-diagrams` 的 infographic/layout 类模板和 ADF 的分区表达。
   - 软件系统架构：优先参考 C4 语义，明确系统、容器、组件和关系。
   - 流程图：优先参考 UML activity diagram 模板。
4. 软著正式图必须保留 `.drawio + SVG + PNG` 三类产物。
5. 图中模块名称必须来自项目事实、源码、截图、系统说明书或用户确认，不得从参考库继承示例业务名。

## 大数据平台总体架构复刻模板

用于医药大数据、数据治理、数据资产、主数据管理等平台型项目。

固定布局：

- 左侧：数据源栏，包含内部数据源、外部数据源，每类下方用小框表达来源。
- 中间：平台总体架构大框，顶部为管控/管理能力条。
- 中间主区：数据接入、数据处理、大数据治理中心、数据服务、数据分析等大模块必须尺寸一致或视觉权重一致。
- 子功能：数据导入、接口采集、文件采集、库表采集等必须使用独立小框，不得仅用换行文字堆叠。
- 右侧：数据应用栏，列出业务应用或分析应用。
- 底部：统一支撑/统一治理/统一权限/统一安全横向支撑条，可用箭头条或分隔条。

硬性约束：

- 平台总图不是业务流程图，平台内部能力区不使用连续流程箭头串联。
- 箭头只表达输入、输出或关键依赖，不表达“先后步骤”。
- 大模块同层级尺寸要统一；子功能框尺寸要统一。
- 分区框、底层支撑区和功能模块要有明显层级差异。
