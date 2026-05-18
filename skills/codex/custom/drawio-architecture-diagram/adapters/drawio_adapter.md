# DrawIO Adapter

外部能力：

- `<LOCAL_SKILL_WORKSPACE>/NextAIDrawIO写作SKILL/SKILL.md`
- `<SOFTWARE_COPYRIGHT_WORKSPACE>/软著申请材料/00_通用说明/00_软著图生成规范_next_ai_drawio.md`
- `references/diagram_references_index.md`

## 边界

- 只调用或引用外部图写作能力。
- 不复制 `NextAIDrawIO写作SKILL` 全文。
- 不复制 `next-ai-draw-io` 项目源码。
- 软著 engine 只负责生成软著场景的图需求、图清单、章节嵌入和产物校验。
- 本地 GitHub 参考库只作为模板和图形语言参考，不作为项目事实来源，不直接继承示例业务名称。

## 输入

| 输入 | 来源 |
|---|---|
| 项目类型识别报告 | `00_材料说明/项目类型识别报告.md` |
| 功能事实表 | `00_材料说明/功能事实表.md` |
| 材料策略报告 | `00_材料说明/材料策略报告.md` |
| 设计说明模板 | `templates/design/README.md` |
| Skill 流程状态 spec | `status/drawio-specs/engine_phase_gate.drawio_spec.json` |
| 项目流程状态 spec | `status/drawio-specs/<项目slug>.drawio_spec.json` |

## 输出

| 产物 | 目标路径 |
|---|---|
| 图需求说明 | `<项目根目录>/00_材料说明/图示生成计划.md` |
| drawio 源文件 | `<项目根目录>/03_截图/drawio/DRWxx_图名.drawio` |
| PNG 导出图 | `<项目根目录>/03_截图/DRWxx_图名.png` |
| SVG 导出图 | `<项目根目录>/03_截图/DRWxx_图名.svg` |
| cells 源片段 | `<项目根目录>/03_截图/drawio/diagram-source/DRWxx_图名.cells.xml` |
| Skill 流程图 spec | `status/drawio-specs/engine_phase_gate.drawio_spec.json` |
| 项目状态图 spec | `status/drawio-specs/<项目slug>.drawio_spec.json` |

## 图清单

| 图号 | 图名 | 适用章节 | 必要性 |
|---|---|---|---|
| DRW01 | 软件结构图 | 总体设计 | 必备 |
| DRW02 | 核心业务流程图 | 功能流程 | 必备 |
| DRW03 | 逻辑框图 | 逻辑设计 | 设计说明必备 |
| DRW04 | 接口/模块映射图 | 接口设计 | T1/T7 推荐 |
| DRW05 | 算法流程图 | 算法说明 | T3 必备 |
| DRW06 | 设备采集流程图 | 运行设计 | T6 必备 |

## 验收

- 有 `.drawio` 源文件。
- 有 PNG 或 SVG 导出图。
- MD/Word/PDF 中嵌入图片，不嵌入 Mermaid 代码。
- 图中模块名称与正文和源码口径一致。
- 图名、图号、章节引用一致。
- 平台总体架构图按参考库和项目已有架构图做版式复刻：分区清晰、大模块尺寸一致、子功能独立成框、底部支撑层独立分隔。

## 本地参考库

已本地化以下 draw.io 架构图参考库：

| 参考库 | 路径 | 主要用途 |
|---|---|---|
| drawio 官方示例/模板 | `vendor/diagram-references/drawio-diagrams` | 模板、UML、数据流、信息图和架构类布局参考 |
| drawio 官方图形库 | `vendor/diagram-references/drawio-libs` | 图标库、形状库、模板库 |
| C4 draw.io 模板 | `vendor/diagram-references/c4-draw.io` | 软件系统架构语义、系统/容器/组件边界 |
| ADF diagrams.net 元素 | `vendor/diagram-references/adf-diagramsnet` | 架构分解、层、环境和运行边界 |

详细索引见 `references/diagram_references_index.md`。

## HTML + DuckDB 看板集成

状态看板不直接承担正式图绘制。集成链路为：

```text
DuckDB
  -> status_dashboard.py export-*-drawio-spec
  -> drawio spec JSON
  -> NextAIDrawIO写作SKILL
  -> .drawio
  -> PNG/SVG
  -> HTML 看板链接或嵌入
```

命令：

```bash
00_实验重构/softcopy-materials-engine/.venv_engine/bin/python \
  00_实验重构/softcopy-materials-engine/scripts/status_dashboard.py render-all \
  --project-root "<项目根目录>"
```

该命令会同时生成：

- `status/engine_flow.html`
- `status/projects/<项目slug>.html`
- `status/drawio-specs/engine_phase_gate.drawio_spec.json`
- `status/drawio-specs/<项目slug>.drawio_spec.json`
