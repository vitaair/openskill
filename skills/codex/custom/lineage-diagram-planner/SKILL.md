---
name: lineage-diagram-planner
description: >
  Use when planning, generating, reviewing, or refining lineage, topology,
  dependency, data-flow, metric-to-result-table, or SQL procedure diagrams.
  Produces readable draw.io/SVG-oriented briefs with lanes, nodes, edges,
  layout rules, and validation checks for diagrams embedded in HTML reports,
  documents, or presentations.
metadata:
  short-description: Readable lineage and topology diagram planning
---

# Lineage Diagram Planner

Use this skill when the task is primarily about a dependency or lineage diagram, especially when prior graphs have overlapping nodes, tangled arrows, missing target tables, or unclear business-to-data mapping.

## Core Rule

Choose the diagram type before drawing. A single diagram should answer one primary question.

| Question | Diagram Type | Primary Nodes |
|---|---|---|
| Which scripts/tables produce what? | SQL 血缘关系图 | upstream, procedure, target table, metric |
| Which procedure depends on which procedure? | SQL 存储过程依赖拓扑图 | stored procedures |
| Which result table serves each metric? | 需求指标结果表血缘图 | business metrics and result tables |
| Which metric analyses are already visualized and what should be added? | 指标图形化分析覆盖图 | metric analysis blocks |
| How should metric logic be explained beyond lineage? | 指标补充分析图组 |口径、覆盖、风险、时间、脚本链路 |
| What is the execution or processing path? | 加工链路图 | stages or cards |

If the user needs multiple questions answered, create multiple diagrams instead of forcing one crowded graph.

## Workflow

1. Extract entities and classify them:
   - upstream/source table
   - intermediate table
   - stored procedure/script
   - result/target table
   - metric/indicator
   - push/detail/gap item
2. Decide the visual contract:
   - lane/table lineage for auditability
   - topology graph for procedure dependencies
   - metric-to-result graph for business traceability
   - cards or simple stages for processing summaries
3. Build a compact graph spec:
   - nodes: stable id, label, type, lane, optional subtitle
   - edges: source, target, meaning, solid/dashed
   - layout: canvas size, lane count, lane dimensions, ordering
4. Generate or edit `.drawio`/SVG artifacts.
5. Validate:
   - no node overlap
   - no title-to-node crowding
   - important arrows are readable
   - every expected entity is represented
   - XML/SVG parses

## Diagram Rules

### SQL 血缘关系图

Use when auditing `source -> procedure -> target table -> metric`.

- Prefer lanes or table-like rows.
- Include target result tables explicitly.
- Keep arrows mostly left-to-right.
- If many shared upstreams exist, group them in a lane instead of drawing every repeated source edge.

### SQL 存储过程依赖拓扑图

Use when the most important question is procedure dependency order.

- Procedure names are the primary labels.
- Target/result table names are secondary labels inside procedure nodes.
- Do not merge distinct procedures just to save space.
- Keep all paired drug/equipment procedures separate unless the user explicitly asks for merged abstraction.
- Use lanes such as source, core procedure, direct downstream, derived/aggregation, and gap/manual items.
- Increase canvas/lane height before shrinking labels.
- Keep lane heights consistent, based on the tallest lane.
- If lane titles are too close to nodes, move nodes down.
- Do not include production notes such as “加宽泳道” or “调整布局” inside the diagram.

### 需求指标结果表血缘图

Use when the user asks which result table a requirement metric comes from.

- Start from every metric/indicator in the requirement.
- Link each metric to concrete result table(s).
- Keep physical result tables separate.
- Use a dashed edge when coverage is partial, reused from risk-detail data, or requires confirmation.
- Keep common upstream tables as context only; do not show them as final metric result tables unless the requirement directly reads from them.

### 指标图形化分析覆盖图

Use when reviewing whether metric-related content has enough diagrams.

- Scope it to metrics only. Do not include feature/workflow topics such as online feedback, role permissions, push notification flows, or page management unless the user explicitly broadens the scope.
- Show what already exists, such as metric list, metric-to-result lineage, and threshold table.
- Show what has been or should be supplemented, such as:
  - 指标口径拆解图
  - 指标覆盖状态图
  - 指标风险判定流程图
  - 指标时间窗口图
  - 指标到脚本执行链路图
- If the supplementary diagrams have been created, label them as already supplemented rather than “建议补充”.

### 指标补充分析图组

Use when the user agrees that suggested metric diagrams should be added.

- Prefer one readable SVG “图组” with five clearly separated panels instead of five oversized separate diagrams, unless the user asks for separate files.
- Recommended panels:
  - 口径拆解: rate metrics split into numerator/denominator; duration metrics split into shipped/unshipped rules.
  - 覆盖状态: one node per core metric, with covered/partial/uncovered status based on result-table implementation.
  - 风险判定: rate-class thresholds and duration-class thresholds flowing to low/mid/high risk.
  - 时间窗口: natural-year monthly accumulation, daily T-1 refresh, and report retention.
  - 指标到脚本链路: metric group -> result table -> generation procedure -> shared order middle table.
- Keep drug and equipment/reagent physical tables or scripts separate when they are separate implementation artifacts.
- Use dashed edges for shared upstream support or partial/reused coverage.

### Processing Cards

When the content is a short pipeline summary rather than a true dependency graph, use cards instead of arrows:

- one card per processing stage
- 2-3 short tags per card
- no long prose inside cards
- put detailed dependencies in a table or graph elsewhere

## Validation Checklist

- The diagram answers one clear question.
- Counts match the source facts: 12 procedures means 12 procedure nodes, 7 attachments means 7 rows/cards, etc.
- No required target/result table is missing.
- Nodes do not overlap and lane title spacing is comfortable.
- Arrows do not obscure labels; split into separate diagrams if needed.
- Dashed/solid edge meanings are explained in the caption or legend.
- Generated `.svg`/`.drawio` parses as XML.
