# Static Dashboard Patterns

## Compact Schema

Top level:

- `title`: page title.
- `subtitle`: short context.
- `summary`: array of `{label, value, href?, hint?}`. Use `href` to jump to detail sections.
- `sections`: array of section blocks.

Section common fields:

- `id`: optional anchor target for summary cards or cross-page navigation.
- `title`: section title.
- `type`: `table`, `cards`, `flow`, `notes`, `diagram`, or `markdown`.

Linked table cell:

```json
{"label": "p_x.sql", "href": "p_x.sql", "title": "optional tooltip"}
```

Use linked cells for real files such as SQL scripts, attachment Markdown files, source documents, draw.io files, SVG previews, or exported reports.

Table section:

```json
{
  "id": "sql-scripts",
  "title": "脚本清单",
  "type": "table",
  "columns": ["脚本", "目标表", "上游"],
  "rows": [[{"label": "p_x.sql", "href": "p_x.sql"}, "dmss.t", "dwd.source"]]
}
```

Cards section:

```json
{
  "title": "附件模块",
  "type": "cards",
  "columns": 3,
  "cards": [
    {"title": "附件4", "body": "配送企业综合得分", "tags": ["st_dmss_dis_evaluation_m"]}
  ]
}
```

Flow section:

```json
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
}
```

Notes section:

```json
{
  "title": "风险点",
  "type": "notes",
  "notes": [
    {"title": "调度缺口", "body": "未发现统一编排。", "severity": "high"}
  ]
}
```

Diagram section:

```json
{
  "title": "脚本依赖节点图",
  "type": "diagram",
  "drawio": "脚本依赖节点图.drawio",
  "spec": "脚本依赖节点图.drawio_spec.json",
  "svg": "脚本依赖节点图.svg",
  "png": "脚本依赖节点图.png",
  "caption": "由 next-ai-drawio-writing 生成。"
}
```

Only `drawio` or `spec` is required in practice. `svg` and `png` are optional preview exports. When no preview is available, the HTML renderer shows clean artifact links and a note.

Markdown section:

```json
{
  "title": "附件1 原文",
  "type": "markdown",
  "source": "附件1-中选产品供应保障监测.md",
  "toc": true,
  "frontmatter": "summary"
}
```

Markdown sections are compiled at render time through `$markdown-html-embedder` when available. This avoids browser-side `file://` fetches.

## Design Patterns

- Analysis pages: summary stats, search, mapping table, dependency matrix, risks.
- Count-driven review pages: clickable summary cards, each backed by a detail section and linked source files.
- Metric catalogs: module cards, formula blocks, threshold tables.
- Workflow pages: flow rows, status legend, details sections.
- Review pages: conclusion cards, issue table,整改 notes.
- Diagram-backed pages: pair a matrix/table with a `diagram` section; use `$lineage-diagram-planner` for graph design when available.
- Markdown-backed pages: use `markdown` sections for source documents that reviewers need to read in-place.

## Data Extraction Pattern

For SQL dependency pages:

1. Extract procedure name.
2. Extract target tables from `insert into`, `truncate table`, and procedure names.
3. Extract upstream tables from `from` and `join`.
4. Classify temp tables as internal dependencies.
5. Create rows with `script`, `procedure`, `target_table`, `upstream`, `notes`.
6. For a visual dependency graph, create a lineage brief:
   - zones: source tables, intermediate tables, result tables, push/detail tables
   - nodes: scripts and key source/target tables
   - edges: upstream -> script/result relationships
   - layout: left-to-right or top-to-bottom, single viewport
7. Use `$lineage-diagram-planner` when available for layout rules; then use `next-ai-drawio-writing` or SVG editing for the artifact and add a `diagram` section to the page spec.

For requirement + attachment + SQL pages, include the following auditable structure:

1. Summary cards:
   - `核心指标` -> `#core-metrics`
   - `附件模块` -> `#attachment-modules`
   - `SQL脚本` -> `#sql-scripts`
   - `结果表` -> `#result-tables`
2. Detail sections:
   - `核心监测指标清单`: one row per metric.
   - `附件模块清单`: one row per attachment; link attachment number to the actual attachment file.
   - `SQL 脚本清单`: one row per `.sql` file; link script filename to the actual file.
   - `结果表清单`: one row per target table; link source script to the actual file.
3. Secondary analysis sections:
   - requirement-to-script mapping.
   - full SQL dependency matrix.
   - risks and gaps.

Count rule: if a summary card says `12`, the linked section must visibly contain 12 corresponding rows. Do not use prose-only counts.

Link rule: the detail row should point to the most specific available file. If an attachment has its own Markdown file, link to it. If not, link to the containing source document or mark待确认.

For SQL topology and metric-to-result-table lineage diagrams, use `$lineage-diagram-planner` when available. The static dashboard spec should only carry the resulting artifact links and a caption that explains solid/dashed edges or partial coverage.

For requirement mapping pages:

1. Split requirements into numbered clauses.
2. Normalize indicator/function names.
3. Match to attachments by keywords and target tables.
4. Match attachments to scripts by target table or procedure name.
5. Mark status: covered, partial, gap.

## DuckDB Tables Worth Reusing

Generic tables:

```sql
create table if not exists source_files (
  path varchar primary key,
  kind varchar,
  modified_at timestamp
);

create table if not exists extracted_facts (
  fact_id varchar primary key,
  source_path varchar,
  fact_type varchar,
  name varchar,
  payload json
);

create table if not exists page_sections (
  page_id varchar,
  section_order integer,
  section_type varchar,
  title varchar,
  payload json
);
```

SQL analysis tables:

```sql
create table if not exists sql_scripts (
  script_path varchar primary key,
  procedure_name varchar,
  target_tables varchar,
  upstream_tables varchar,
  temp_tables varchar,
  notes varchar
);
```

Requirement mapping tables:

```sql
create table if not exists requirement_mapping (
  req_id varchar,
  req_name varchar,
  attachment varchar,
  script_path varchar,
  target_table varchar,
  coverage varchar,
  notes varchar
);
```
