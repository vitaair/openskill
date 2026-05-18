# Markdown Embed Patterns

## Dashboard Section

```json
{
  "title": "附件原文",
  "type": "markdown",
  "source": "附件1-中选产品供应保障监测.md",
  "toc": true,
  "frontmatter": "summary"
}
```

## Hugging Face-Style Card Pattern

Hugging Face model and dataset cards are commonly stored as `README.md` files with optional YAML metadata at the top followed by Markdown prose. Mirror that pattern for local static pages:

```markdown
---
license: apache-2.0
tags:
- monitor
- lineage
---

# Card Title

Markdown body...
```

Rendering behavior:

- strip the YAML block from the body;
- show metadata as a compact metadata panel;
- generate a heading-based table of contents;
- keep a source `.md` link visible.

## Multi-Document Pattern

Use one section per document when reviewers need independent source links:

```json
[
  {"title": "附件1 原文", "type": "markdown", "source": "附件1.md"},
  {"title": "附件2 原文", "type": "markdown", "source": "附件2.md"}
]
```

Use a table of links instead when there are many long documents and only navigation is needed.

## File Link Rules

- If the Markdown source and HTML output are in the same directory, keep links relative.
- If the Markdown source is elsewhere, rewrite relative links based on source dir -> output dir.
- Keep external `http://` and `https://` links untouched and add safe external link attributes.
- Keep anchor links untouched.

## Safety Defaults

- Raw HTML in Markdown should be disabled unless the source is trusted and the user explicitly needs it.
- Do not execute scripts from Markdown.
- Do not inject remote CDN dependencies into file:// pages unless the user asks for web-hosted output.
