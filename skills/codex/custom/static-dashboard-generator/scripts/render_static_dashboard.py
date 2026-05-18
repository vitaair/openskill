#!/usr/bin/env python3
"""Render file:// friendly static dashboards from JSON specs or DuckDB queries."""

from __future__ import annotations

import argparse
import html
import json
import subprocess
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
MARKDOWN_RENDERER = SKILL_DIR.parent / "markdown-html-embedder" / "scripts" / "render_markdown_fragment.mjs"

CSS = r"""
:root{--bg:#f5f7fa;--panel:#fff;--text:#172033;--muted:#657085;--line:#d9e1ec;--blue:#1f5fbf;--green:#237a42;--amber:#a15c00;--red:#ba2b20;--soft-blue:#eaf2ff;--soft-green:#eaf6ee;--soft-amber:#fff4df;--soft-red:#ffebe8;--shadow:0 12px 28px rgba(24,39,75,.08)}
.md-meta{padding:12px 18px;border-bottom:1px solid var(--line);background:#fff}.md-meta summary{cursor:pointer;font-weight:800;color:#344054}.md-meta-row{display:grid;grid-template-columns:150px 1fr;gap:10px;margin-top:8px;font-size:13px}.md-meta-value{display:inline-flex;margin:0 6px 6px 0;border-radius:999px;background:#eef2f7;padding:2px 8px;color:#344054;font-weight:700}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif;line-height:1.55}.page{max-width:1360px;margin:0 auto;padding:32px 24px 56px}.hero{display:grid;gap:22px;padding:22px 0 26px;border-bottom:1px solid var(--line)}h1,h2,h3{margin:0;letter-spacing:0}h1{font-size:clamp(30px,4vw,46px);line-height:1.12}h2{font-size:24px;margin:34px 0 14px}h3{font-size:17px}.subtitle{max-width:920px;margin:12px 0 0;color:var(--muted);font-size:15px}.summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;width:100%}.stat,.panel,.table-card,.note,.node,.diagram-card,.md-embed{background:var(--panel);border:1px solid var(--line);border-radius:8px;box-shadow:var(--shadow)}.stat{position:relative;display:grid;grid-template-columns:auto 1fr;grid-template-areas:"value label" "value hint";column-gap:14px;align-items:center;min-height:92px;padding:18px 20px;color:var(--text);text-decoration:none;overflow:hidden}.stat:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--blue)}.stat:hover{border-color:var(--blue);text-decoration:none;transform:translateY(-1px)}.stat strong{grid-area:value;display:block;min-width:58px;font-size:38px;line-height:1;color:#0f2f66}.stat span{grid-area:label;display:block;color:#344054;font-size:15px;font-weight:800}.stat span,.section-note,.panel p,.note p,.node span,.diagram-caption{color:var(--muted);font-size:13px}.stat span{color:#344054;font-size:15px}.stat em{grid-area:hint;display:block;margin-top:4px;color:var(--blue);font-size:12px;font-style:normal;font-weight:700}.toolbar{position:sticky;top:0;z-index:2;padding:14px 0;background:rgba(245,247,250,.94);backdrop-filter:blur(10px)}.search{width:100%;height:42px;border:1px solid var(--line);border-radius:8px;background:var(--panel);padding:0 14px;outline:none;color:var(--text);font-size:14px}.search:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(31,95,191,.12)}section{scroll-margin-top:76px}.table-card{overflow-x:auto}table{width:100%;min-width:840px;border-collapse:collapse}th,td{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;font-size:14px}th{background:#eef3f9;color:#344054;font-weight:800;white-space:nowrap}tr:last-child td{border-bottom:0}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}code{padding:1px 5px;border-radius:5px;background:#eef2f7;color:#243b64;font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace;font-size:.92em}.grid{display:grid;grid-template-columns:repeat(var(--cols,2),minmax(0,1fr));gap:16px}.panel{padding:18px}.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.chip,.badge{display:inline-flex;align-items:center;border-radius:999px;padding:3px 9px;font-size:12px;font-weight:700;white-space:nowrap}.chip{background:#eef2f7;color:#344054}.badge.ok{background:var(--soft-green);color:var(--green)}.badge.warn{background:var(--soft-amber);color:var(--amber)}.badge.high{background:var(--soft-red);color:var(--red)}.flow{display:grid;gap:12px}.flow-row{display:grid;grid-template-columns:repeat(var(--cols,3),minmax(0,1fr));gap:12px;align-items:stretch}.node{padding:12px;background:#fbfcff}.node b{display:block;margin-bottom:6px}.notes{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.note{padding:14px;border-left:4px solid var(--amber)}.note.high{border-left-color:var(--red)}.note.low{border-left-color:var(--green)}.diagram-card{overflow:hidden}.diagram-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;padding:16px 18px;border-bottom:1px solid var(--line);background:#fbfcff}.diagram-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.diagram-actions a{display:inline-flex;align-items:center;min-height:32px;border:1px solid var(--line);border-radius:8px;background:#fff;padding:4px 10px;font-size:13px;font-weight:700}.diagram-preview{padding:16px 18px;background:#fff}.diagram-preview img,.diagram-preview object{display:block;width:100%;max-height:620px;border:1px solid var(--line);border-radius:8px;background:#fff}.diagram-empty{padding:18px;color:var(--muted);font-size:13px}.md-embed{overflow:hidden}.md-embed-head{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:14px 18px;border-bottom:1px solid var(--line);background:#fbfcff}.md-toc{padding:12px 18px;border-bottom:1px solid var(--line);background:#fff}.md-toc strong{display:block;margin-bottom:6px}.md-toc ul{display:flex;flex-wrap:wrap;gap:6px 14px;margin:0;padding:0;list-style:none}.md-toc a{font-size:13px;font-weight:700}.md-toc-l2{margin-left:10px}.md-toc-l3{margin-left:20px}.md-body{padding:18px}.md-body h1,.md-body h2,.md-body h3,.md-body h4{margin:18px 0 10px}.md-body p,.md-body ul,.md-body ol{font-size:14px}.md-body pre{overflow:auto;border:1px solid var(--line);border-radius:8px;background:#101828;color:#f5f7fa;padding:12px}.md-body pre code{background:transparent;color:inherit;padding:0}.md-body table{margin:12px 0}.hidden{display:none}@media(max-width:1100px){.summary{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:900px){.grid,.notes,.flow-row{grid-template-columns:1fr}.summary{grid-template-columns:1fr}.page{padding:22px 14px 42px}.diagram-head,.md-embed-head{display:block}.diagram-actions{justify-content:flex-start;margin-top:12px}}
"""


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def cell(value: Any) -> str:
    if isinstance(value, dict):
        label = esc(value.get("label", value.get("text", "")))
        href = esc(value.get("href", ""))
        title = esc(value.get("title", ""))
        title_attr = f" title='{title}'" if title else ""
        if href:
            return f"<a href='{href}'{title_attr}>{label}</a>"
        return label
    text = esc(value)
    if text.startswith("http://") or text.startswith("https://"):
        return f"<a href='{text}'>{text}</a>"
    if "." in text and ("dmss." in text or "dwd." in text or "dim." in text or "ods." in text):
        return f"<code>{text}</code>"
    return text.replace("\n", "<br>")


def render_table(section: dict[str, Any]) -> str:
    columns = section.get("columns", [])
    rows = section.get("rows", [])
    head = "".join(f"<th>{esc(col)}</th>" for col in columns)
    body = []
    for row in rows:
        body.append("<tr>" + "".join(f"<td>{cell(value)}</td>" for value in row) + "</tr>")
    return f"<div class='table-card'><table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"


def render_cards(section: dict[str, Any]) -> str:
    cards = []
    for card in section.get("cards", []):
        tags = "".join(f"<span class='chip'>{esc(tag)}</span>" for tag in card.get("tags", []))
        cards.append(
            "<article class='panel'>"
            f"<h3>{esc(card.get('title'))}</h3>"
            f"<p>{esc(card.get('body'))}</p>"
            f"<div class='chips'>{tags}</div>"
            "</article>"
        )
    columns = max(1, min(int(section.get("columns", 2)), 4))
    return f"<div class='grid' style='--cols:{columns}'>{''.join(cards)}</div>"


def render_flow(section: dict[str, Any]) -> str:
    rendered_rows = []
    for row in section.get("rows", []):
        nodes = []
        for node in row:
            nodes.append(
                "<div class='node'>"
                f"<b>{esc(node.get('title'))}</b>"
                f"<span>{esc(node.get('body')).replace(chr(10), '<br>')}</span>"
                "</div>"
            )
        rendered_rows.append(f"<div class='flow-row' style='--cols:{max(len(nodes),1)}'>{''.join(nodes)}</div>")
    return f"<div class='flow'>{''.join(rendered_rows)}</div>"


def render_notes(section: dict[str, Any]) -> str:
    notes = []
    for note in section.get("notes", []):
        sev = note.get("severity", "medium")
        cls = "high" if sev == "high" else "low" if sev == "low" else ""
        notes.append(
            f"<article class='note {cls}'>"
            f"<h3>{esc(note.get('title'))}</h3>"
            f"<p>{esc(note.get('body'))}</p>"
            "</article>"
        )
    return f"<div class='notes'>{''.join(notes)}</div>"


def render_link(path: str, label: str) -> str:
    if not path:
        return ""
    href = esc(path)
    return f"<a href='{href}'>{esc(label)}</a>"


def render_diagram(section: dict[str, Any]) -> str:
    drawio = section.get("drawio", "")
    spec = section.get("spec", "")
    svg = section.get("svg", "")
    png = section.get("png", "")
    caption = section.get("caption", "")
    actions = [
        render_link(drawio, "打开 .drawio"),
        render_link(spec, "查看 spec"),
        render_link(svg, "查看 SVG") if svg else "",
        render_link(png, "查看 PNG") if png else "",
    ]
    actions_html = "".join(action for action in actions if action)
    preview = ""
    if svg:
        preview = f"<div class='diagram-preview'><object data='{esc(svg)}' type='image/svg+xml'></object></div>"
    elif png:
        preview = f"<div class='diagram-preview'><img src='{esc(png)}' alt='{esc(section.get('title', 'diagram'))}'></div>"
    else:
        preview = "<div class='diagram-empty'>当前仅挂接 draw.io 图源和结构 spec；如需要页面内预览，可补充 SVG 或 PNG 导出路径。</div>"
    return (
        "<div class='diagram-card'>"
        "<div class='diagram-head'>"
        f"<div><h3>{esc(section.get('diagram_title', section.get('title', 'Diagram')))}</h3>"
        f"<p class='diagram-caption'>{esc(caption)}</p></div>"
        f"<div class='diagram-actions'>{actions_html}</div>"
        "</div>"
        f"{preview}"
        "</div>"
    )


def render_markdown(section: dict[str, Any]) -> str:
    source = section.get("source", "")
    if not source:
        return "<div class='diagram-empty'>Markdown section is missing a source file.</div>"
    base_dir = Path(section.get("_base_dir", "."))
    output_dir = Path(section.get("_output_dir", "."))
    source_path = Path(source).expanduser()
    if not source_path.is_absolute():
        source_path = base_dir / source_path
    if not source_path.exists():
        return f"<div class='diagram-empty'>Markdown source not found: {esc(source)}</div>"
    if not MARKDOWN_RENDERER.exists():
        href = esc(str(source))
        return f"<div class='diagram-empty'>Markdown renderer is unavailable. <a href='{href}'>Open source Markdown</a>.</div>"
    cmd = [
        "node",
        str(MARKDOWN_RENDERER),
        "--input",
        str(source_path),
        "--output-dir",
        str(output_dir),
        "--title",
        str(section.get("markdown_title", section.get("title", source_path.name))),
        "--toc",
        "false" if section.get("toc") is False else "true",
        "--frontmatter",
        str(section.get("frontmatter", "summary")),
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        message = getattr(exc, "stderr", "") or str(exc)
        return f"<div class='diagram-empty'>Markdown render failed: {esc(message)}</div>"
    return result.stdout


def render_section(section: dict[str, Any]) -> str:
    section_type = section.get("type", "table")
    if section_type == "cards":
        body = render_cards(section)
    elif section_type == "flow":
        body = render_flow(section)
    elif section_type == "notes":
        body = render_notes(section)
    elif section_type == "diagram":
        body = render_diagram(section)
    elif section_type == "markdown":
        body = render_markdown(section)
    else:
        body = render_table(section)
    note = f"<p class='section-note'>{esc(section.get('note'))}</p>" if section.get("note") else ""
    section_id = esc(section.get("id", ""))
    id_attr = f" id='{section_id}'" if section_id else ""
    return f"<section{id_attr}><h2>{esc(section.get('title'))}</h2>{note}{body}</section>"


def render_page(spec: dict[str, Any]) -> str:
    summary_items = []
    for item in spec.get("summary", []):
        href = item.get("href", "")
        inner = (
            f"<strong>{esc(item.get('value'))}</strong>"
            f"<span>{esc(item.get('label'))}</span>"
            f"<em>{esc(item.get('hint', '查看明细'))}</em>"
        )
        if href:
            summary_items.append(f"<a class='stat' href='{esc(href)}'>{inner}</a>")
        else:
            summary_items.append(f"<div class='stat'>{inner}</div>")
    summary = "".join(summary_items)
    sections = "".join(render_section(section) for section in spec.get("sections", []))
    title = esc(spec.get("title", "Static Dashboard"))
    subtitle = esc(spec.get("subtitle", ""))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="page">
    <header class="hero">
      <div><h1>{title}</h1><p class="subtitle">{subtitle}</p></div>
      <div class="summary">{summary}</div>
    </header>
    <div class="toolbar"><input id="searchInput" class="search" type="search" placeholder="搜索页面内容..." aria-label="搜索"></div>
    {sections}
  </main>
  <script>
    const input = document.querySelector("#searchInput");
    const sections = document.querySelectorAll("section");
    input.addEventListener("input", () => {{
      const q = input.value.trim().toLowerCase();
      sections.forEach((section) => {{
        section.classList.toggle("hidden", q && !section.innerText.toLowerCase().includes(q));
      }});
    }});
  </script>
</body>
</html>
"""


def import_duckdb():
    try:
        import duckdb  # type: ignore
    except ImportError as exc:
        raise SystemExit("DuckDB is required for --db. Install duckdb or use --spec only.") from exc
    return duckdb


def spec_from_duckdb(db_path: Path, queries: list[str], title: str, subtitle: str) -> dict[str, Any]:
    duckdb = import_duckdb()
    con = duckdb.connect(str(db_path))
    sections = []
    for item in queries:
        if "=" in item:
            section_title, sql = item.split("=", 1)
        else:
            section_title, sql = "查询结果", item
        result = con.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = [list(row) for row in result.fetchall()]
        sections.append({"title": section_title, "type": "table", "columns": columns, "rows": rows})
    con.close()
    return {
        "title": title,
        "subtitle": subtitle or f"Source DuckDB: {db_path}",
        "summary": [{"label": "查询区块", "value": str(len(sections))}],
        "sections": sections,
    }


def list_tables(db_path: Path) -> None:
    duckdb = import_duckdb()
    con = duckdb.connect(str(db_path))
    rows = con.execute("show tables").fetchall()
    for (name,) in rows:
        print(name)
    con.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", help="JSON page spec.")
    parser.add_argument("--db", help="DuckDB database path.")
    parser.add_argument("--query", action="append", default=[], help="'Section title=select ...' DuckDB query. Repeatable.")
    parser.add_argument("--title", default="Static Dashboard")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--output", help="Output HTML path.")
    parser.add_argument("--list-tables", action="store_true")
    args = parser.parse_args()

    if args.db and args.list_tables:
        list_tables(Path(args.db).expanduser())
        return

    spec_base_dir = Path.cwd()
    if args.spec:
        spec_path = Path(args.spec).expanduser()
        spec_base_dir = spec_path.resolve().parent
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    elif args.db and args.query:
        spec = spec_from_duckdb(Path(args.db).expanduser(), args.query, args.title, args.subtitle)
    else:
        raise SystemExit("Provide --spec, or --db with at least one --query.")

    output = Path(args.output or "static_dashboard.html").expanduser()
    for section in spec.get("sections", []):
        section.setdefault("_base_dir", str(spec_base_dir))
        section.setdefault("_output_dir", str(output.resolve().parent))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_page(spec), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
