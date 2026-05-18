---
name: markdown-html-embedder
description: >
  Use when Markdown files need to be embedded into static HTML dashboards,
  reports, docs, or review pages. Converts local .md files into file:// friendly
  sanitized HTML fragments with heading anchors, table rendering, code blocks,
  local link rewriting, and optional table of contents. Designed to pair with
  static-dashboard-generator markdown sections.
metadata:
  short-description: Embed local Markdown into static HTML
---

# Markdown HTML Embedder

Use this skill when the user wants Markdown content mounted into an HTML page, especially attachment documents, requirement notes, README-style files, Hugging Face-style model/dataset cards, or generated Markdown reports.

## Core Rule

Compile Markdown at generation time. Do not rely on browser-side `fetch(file://...)` to load `.md` files, because local browser security policies often block it.

Preferred pipeline:

```text
local .md files -> markdown-it render -> HTML fragment -> static dashboard section
```

For Hugging Face-style cards, treat the source as:

```text
README.md -> optional YAML frontmatter metadata -> Markdown body -> rendered card with outline/TOC
```

The YAML frontmatter should not be shown as raw Markdown. Parse it into a metadata block, similar to how Hugging Face model cards use README metadata for repo discovery and display context.

## Bundled Renderer

Use `scripts/render_markdown_fragment.mjs`.

It uses the local clone of `markdown-it` at:

```text
../vendor/markdown-it
```

The project was cloned from:

```text
https://github.com/markdown-it/markdown-it
```

Basic usage:

```bash
node scripts/render_markdown_fragment.mjs \
  --input /path/to/source.md \
  --output-dir /path/to/html-output-dir \
  --title "附件1 原文"
```

The script writes the rendered fragment to stdout unless `--output` is provided.

## Static Dashboard Pairing

When `$static-dashboard-generator` is available, add Markdown sections like:

```json
{
  "title": "附件1 原文",
  "type": "markdown",
  "source": "附件1-中选产品供应保障监测.md",
  "toc": true,
  "frontmatter": "summary"
}
```

The dashboard renderer should compile the Markdown into the final HTML during generation.

## Rendering Rules

- Use `markdown-it` with raw HTML disabled by default.
- Generate heading anchors for in-page navigation.
- Generate a compact table of contents for level 1-3 headings unless disabled.
- Parse top-level `---` YAML frontmatter and render it as a metadata block by default.
- Rewrite relative links and images from the Markdown source location to the HTML output location.
- Keep source links visible so reviewers can open the original `.md`.
- Preserve code fences and tables.
- For untrusted Markdown that allows raw HTML, pair with DOMPurify or keep `html: false`.

## Validation

Minimum checks:

```bash
node scripts/render_markdown_fragment.mjs --input sample.md --output-dir .
node --check scripts/render_markdown_fragment.mjs
```

For dashboard integration, verify:

- the final HTML contains `class="md-embed"`;
- the source `.md` link exists;
- headings received ids;
- no browser-side Markdown fetch is required;
- local relative links point to existing files when practical.
