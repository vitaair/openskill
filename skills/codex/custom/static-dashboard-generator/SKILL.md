---
name: static-dashboard-generator
description: >
  Use when generating reusable static HTML dashboards, report pages, mapping tables,
  dependency views, metric catalogs, or review pages from structured data such as
  Markdown extracts, SQL analysis, CSV/JSON, or DuckDB query results. Produces file://
  friendly HTML without requiring a web server. Supports clickable summary-to-detail
  navigation, detail-to-source-file links, and embedding draw.io/SVG diagrams.
metadata:
  short-description: DuckDB/JSON driven static HTML dashboards
---

# Static Dashboard Generator

Use this skill when a task needs a reusable static page rather than a one-off hand-written HTML file. It is especially useful for:

- requirement-to-script mapping pages
- SQL/script dependency analysis
- metric catalogs and口径清单
- workflow/status dashboards
- draw.io/SVG-backed dependency or architecture diagram sections
- clickable summary dashboards where counts drill into detail tables
- review and整改报告 pages
- DuckDB-backed static reports

## Core Rule

Prefer this pipeline:

```text
source files -> structured facts -> optional DuckDB -> JSON page spec -> static HTML
```

Do not hide important data only in prose. Put facts into tables, cards, flow rows, or notes so the page can be reviewed and regenerated.

For analysis dashboards, every top-level count must be auditable:

```text
summary count -> detail section -> source file / script / artifact
```

If a count says there are 7 attachments, 12 scripts, 12 result tables, or 9 metrics, the page must include a corresponding detail section with exactly those rows, and rows should link to real local files when such files exist.

For a multi-page report set, avoid copying the same dense content into every page. Use one complete dashboard plus focused topic pages:

```text
index -> complete dashboard -> focused metric page / focused implementation-dependency page
```

Keep shared context, generation notes, and page responsibilities in the index. Keep the full raw/detail content in the complete dashboard. Topic pages should only keep the analysis needed for their topic.

## When To Use DuckDB

Use DuckDB when:

- the page is derived from many files or repeated scans
- the user asks whether data is stored/queryable
- data needs grouping, filtering, joins, or repeatable refresh
- the page may be regenerated later

Skip DuckDB when:

- the page is small and source data is already a simple JSON/list
- the user only needs a quick static artifact
- no database runtime is available and a plain JSON spec is enough

## Workflow

1. Discover source files with `rg --files` and inspect likely inputs.
2. Extract structured facts: entities, fields, formulas, dependencies, statuses, risks.
3. If repeatability matters, create or update a DuckDB file near the output, usually `status/static_dashboard.duckdb`.
4. For dependency graphs, process flows, architecture diagrams, or entity maps, use `$lineage-diagram-planner` when available to choose the right graph type and create a compact layout plan, then invoke `next-ai-drawio-writing` or edit SVG/draw.io artifacts.
5. Build a JSON page spec with title, clickable summary stats, sections, tables, cards, flows, notes, and optional diagrams.
6. Render HTML using `scripts/render_static_dashboard.py` when the built-in blocks are enough.
7. For custom visuals, edit generated HTML directly or add a small custom renderer, keeping it file:// friendly.
8. Verify:
   - HTML file exists.
   - Key entities, counts, anchors, and file links are present with `rg`.
   - If a script was used, run `python -m py_compile`.
   - If the user has a browser open or asks for visual check, open the page in Browser and inspect.

## Multi-Page Report Sets

When the user asks for several static pages around the same source material, assign each page a clear responsibility and prevent content drift:

- `1-*索引.html`: entry page only. Include page cards, global rules, generation metadata, and where each topic lives.
- `2-*总看板.html`: complete dashboard. It may include all tables, diagrams, markdown originals, gaps, and common notes.
- `3-*指标*.html`: metric topic page. Keep metric list, metric thresholds, metric lineage, metric analysis diagrams. Do not repeat attachment markdown, SQL script tables, or implementation dependency matrices unless the user explicitly asks.
- `4-*依赖*.html`: implementation/dependency topic page. Keep attachments, scripts, result tables, dependency matrix, SQL lineage/topology, and processing chain. Do not repeat metric-only analysis or threshold explanations unless they are necessary for dependency review.

Index cards and explanatory cards should share one visual style: same radius, border, shadow, title scale, padding, and responsive behavior. Use color only as a small category signal, such as a top border.

Place generation metadata near the page title, not only at the bottom:

```html
<div class="meta">
  <span>最后更新：YYYY-MM-DD</span>
  <span>static-dashboard-generator</span>
  <span>lineage-diagram-planner</span>
  <span>markdown-html-embedder</span>
</div>
```

## Page Spec

The bundled renderer accepts JSON:

```json
{
  "title": "需求与脚本依赖分析",
  "subtitle": "从需求、附件和 SQL 脚本抽取。",
  "summary": [
    {"label": "脚本", "value": "12", "href": "#sql-scripts", "hint": "查看脚本清单"},
    {"label": "结果表", "value": "10", "href": "#result-tables", "hint": "查看结果表清单"}
  ],
  "sections": [
    {
      "id": "sql-scripts",
      "title": "对应关系",
      "type": "table",
      "columns": ["需求", "脚本", "状态"],
      "rows": [
        ["4.1", {"label": "p_st_dmss_dis_evaluation_m.sql", "href": "p_st_dmss_dis_evaluation_m.sql"}, "已覆盖"]
      ]
    },
    {
      "title": "依赖链路",
      "type": "flow",
      "rows": [
        [
          {"title": "源表", "body": "dwd.wt_tm_order_m"},
          {"title": "中间层", "body": "dmss.wt_dmss_tm_order_m"},
          {"title": "结果表", "body": "st_dmss_*"}
        ]
      ]
    },
    {
      "title": "脚本依赖节点图",
      "type": "diagram",
      "drawio": "script-lineage.drawio",
      "spec": "script-lineage.drawio_spec.json",
      "caption": "由 next-ai-drawio-writing 生成 draw.io 图源。"
    }
  ]
}
```

Supported section types:

- `table`: columns + rows.
- `cards`: cards with title, body, tags.
- `flow`: rows of ordered nodes.
- `notes`: note items with title, body, severity.
- `diagram`: draw.io/spec links with optional SVG/PNG preview.
- `cards` can include optional `columns` for desktop layout control.
- `markdown`: embeds a local `.md` file rendered by `$markdown-html-embedder` when available.

See `references/static-dashboard-patterns.md` for the full compact schema and design rules.

### Navigation And Links

- Add `href` and `hint` to `summary` cards when a count has a detail section.
- Add `id` to the target section. Use stable ids such as `core-metrics`, `attachment-modules`, `sql-scripts`, and `result-tables`.
- A table cell can be a link object: `{"label": "p_x.sql", "href": "p_x.sql"}`.
- Use file-relative links when the HTML and linked files live together. Prefer linking to the real `.sql`, `.md`, `.drawio`, `.svg`, `.xlsx`, or source artifact rather than mentioning only a filename.
- If a source file does not exist, do not fake a link. Either point to the containing source document or mark the row as待确认.

### Required Detail Sections For Requirement/SQL Dashboards

When generating a requirement-to-script or SQL dependency dashboard, include these detail sections when applicable:

- `核心监测指标清单` (`id: core-metrics`): every metric/indicator in the requirement.
- `附件模块清单` (`id: attachment-modules`): one row per attachment/module, linked to attachment files when present.
- `SQL 脚本清单` (`id: sql-scripts`): one row per script, linked to actual `.sql` files.
- `结果表清单` (`id: result-tables`): one row per target/result table, with linked source script.
- Keep the fuller dependency matrix as an additional section when useful; it should not replace the concise linked script/result lists.

## Diagram Integration

This skill owns HTML embedding, not diagram design. When a section needs a real lineage/topology diagram, use `$lineage-diagram-planner` when available and keep this skill focused on attaching the artifact to the page.

1. Decide the diagram type and layout with `$lineage-diagram-planner` or an equivalent lineage planning pass.
2. Use `next-ai-drawio-writing` to produce `.drawio` or `mxCell` content when draw.io output is needed.
3. Save the graph artifact next to the HTML output, usually as `<page-topic>.drawio`.
4. Save a compact `<page-topic>.drawio_spec.json` with layout plan, nodes, edges, and notes.
5. Add a `diagram` section to the page spec.

```json
{
  "title": "依赖节点图",
  "type": "diagram",
  "drawio": "依赖节点图.drawio",
  "spec": "依赖节点图.drawio_spec.json",
  "svg": "依赖节点图.svg",
  "caption": "源表、中间表、结果表和推送明细依赖关系。"
}
```

`svg` and `png` are optional. If present, the renderer embeds a preview. If absent, it renders clean links to the draw.io source and spec.

For requirement + SQL dashboards, the common useful diagram set is:

- **SQL 血缘关系图**: `upstream -> procedure -> target table -> metric` for auditability.
- **SQL 存储过程依赖拓扑图**: procedure-to-procedure dependencies, with target tables as subtitles.
- **需求指标结果表血缘图**: business metric to concrete result table mapping.
- **指标图形化分析覆盖图**: checks which metric-related analyses are already visualized.
- **指标补充分析图组**: covers metric口径拆解、覆盖状态、风险判定、时间窗口、指标到脚本链路. Keep feature/workflow items such as online feedback, role permissions, and push notification flows out of this metric-only diagram unless the user broadens the scope.

Keep the detailed layout, lane, edge, and overlap rules in `$lineage-diagram-planner`; this skill only references the produced `.drawio`, `.svg`, `.png`, and spec files.

## Markdown Integration

This skill can embed local Markdown files as generated HTML sections. Use `$markdown-html-embedder` when available.

```json
{
  "title": "附件1 原文",
  "type": "markdown",
  "source": "附件1-中选产品供应保障监测.md",
  "toc": true,
  "frontmatter": "summary"
}
```

The renderer compiles Markdown during HTML generation. Do not rely on browser-side `fetch(file://...)` for Markdown includes.

## Renderer

Run from this skill directory:

```bash
python scripts/render_static_dashboard.py \
  --spec /path/to/page_spec.json \
  --output /path/to/output.html
```

DuckDB table sections can be added without writing JSON rows:

```bash
python scripts/render_static_dashboard.py \
  --db /path/to/static_dashboard.duckdb \
  --query "脚本清单=select script, target_table, upstream from script_deps" \
  --output /path/to/output.html \
  --title "脚本依赖分析"
```

Multiple `--query` arguments are allowed.

## Design Rules

- Build the actual review page first, not a landing page.
- Keep pages dense but readable: table-first for analysis, cards only for grouped summaries.
- Put summary cards in a full-width row under the title. They should look like navigation, not tiny side stats.
- Summary cards should be clickable when they represent a count with a detail table.
- Use restrained colors; avoid one-hue pages and decorative backgrounds.
- Use native `details/summary`, buttons, search input, and simple JavaScript only.
- Ensure text wraps cleanly in tables and cards.
- Use file-relative links only when the output and linked files move together; otherwise use absolute local paths in final replies.
- Do not require a dev server for the generated page.

## Validation

Minimum validation:

```bash
python -m py_compile scripts/render_static_dashboard.py
rg -n "expected keyword|expected table|expected script" /path/to/output.html
rg -n "href='#sql-scripts'|id='sql-scripts'|href='expected.sql'" /path/to/output.html
```

For count-driven dashboards, verify:

- summary counts match detail row counts.
- every summary `href` has a matching section `id`.
- linked files exist in the output directory, or the row clearly marks the source as unavailable/待确认.
- diagrams parse as XML/SVG when generated:

```bash
python - <<'PY'
import xml.etree.ElementTree as ET
for f in ["diagram.svg", "diagram.drawio"]:
    ET.parse(f)
    print(f, "ok")
PY
```

For DuckDB-backed pages, also verify the database:

```bash
python scripts/render_static_dashboard.py --db /path/to/db.duckdb --list-tables
```
