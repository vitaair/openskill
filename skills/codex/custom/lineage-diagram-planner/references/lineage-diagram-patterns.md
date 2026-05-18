# Lineage Diagram Patterns

## Compact Graph Spec

Use this shape when planning a diagram:

```json
{
  "title": "SQL 存储过程依赖拓扑图",
  "type": "procedure-topology",
  "canvas": {"width": 1680, "height": 1020},
  "lanes": [
    {"id": "source", "label": "源表与公共中间层", "x": 40, "y": 120, "width": 300, "height": 760},
    {"id": "core", "label": "核心过程", "x": 370, "y": 120, "width": 360, "height": 760}
  ],
  "nodes": [
    {"id": "p_order", "label": "p_wt_dmss_tm_order_m", "subtitle": "dmss.wt_dmss_tm_order_m", "lane": "core"}
  ],
  "edges": [
    {"from": "p_order", "to": "p_general_list", "style": "solid", "label": "reads target table"}
  ],
  "legend": [
    {"style": "solid", "meaning": "已覆盖"},
    {"style": "dashed", "meaning": "部分覆盖/待确认"}
  ]
}
```

## Layout Defaults

- Canvas width: 1400-1800 for dense local report diagrams.
- Lane height: use the maximum lane content height and apply it to all lanes.
- Node spacing: at least 28 px vertical gap and 40 px horizontal gap.
- Lane title gap: at least 48 px between title baseline and first node top.
- Node labels: primary label first, target/result table as subtitle.
- Avoid negative letter spacing and tiny fonts; expand the canvas instead.

## Edge Patterns

- Solid edge: confirmed dependency or confirmed result table support.
- Dashed edge: partial coverage, risk-only table, inferred dependency, or pending confirmation.
- Curved edge: acceptable for topology graphs, but keep it away from labels.
- Orthogonal edge: preferable for lane/table lineage where auditability matters.
- Shared upstream: use a grouped upstream node rather than repeating many parallel edges.

## Anti-Patterns

- Combining multiple business questions into one graph.
- Showing result tables as primary nodes in a procedure-topology graph.
- Hiding target tables entirely in SQL lineage.
- Merging drug/equipment procedure pairs when table-level auditability matters.
- Writing layout instructions or editing notes inside the diagram.
- Using a dense force graph when a lane/table layout would be easier to read.

