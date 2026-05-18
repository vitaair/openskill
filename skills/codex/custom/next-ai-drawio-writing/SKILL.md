---
name: next-ai-drawio-writing
description: Use when writing, refining, or auditing prompts and specifications for AI-generated draw.io diagrams based on the next-ai-draw-io project model: natural-language diagram creation, mxCell-only XML generation, ID-based diagram edits, shape library selection, layout planning, visual validation, and iterative improvement.
---

# Next AI Draw.io Writing

Use this skill when the task is to write or improve diagram-generation content: prompts, diagram briefs, draw.io XML instructions, mxCell snippets, edit operations, validation feedback, or agent instructions for creating diagrams.

This skill abstracts the **writing model** behind `next-ai-draw-io`. It does not require running the app.

## Fast Path

1. Read `next-ai-drawio-writing-index.md` to choose the correct writing mode.
2. Identify the diagram intent: flowchart, architecture, sequence/process, mind map, entity model, cloud diagram, UI/mockup, artistic sketch, or document/image replication.
3. Write a short layout plan before diagram content: direction, zones, grouping, and edge-routing strategy.
4. If generating draw.io XML, output only `mxCell` elements unless the caller explicitly asks for a full `.drawio` file.
5. Keep the diagram inside one viewport: x `0-800`, y `0-600`, compact groups, no page-break sprawl.
6. Avoid overlap: plan shape sizes, spacing, edge exit/entry points, and waypoints before writing cells.
7. For existing diagrams, prefer ID-based edit operations instead of regenerating the whole diagram.
8. For cloud/icon diagrams, first identify the needed shape library and do not guess icon syntax.

## Writing Modes

- **Diagram prompt**: Write a user-facing natural-language prompt for `next-ai-draw-io`.
- **Diagram brief**: Write a structured spec an agent can convert into draw.io.
- **mxCell XML**: Write draw.io `mxCell` elements only, with valid IDs, parents, geometry, and edge routing.
- **Edit operations**: Write ID-based add/update/delete operations for an existing diagram.
- **Validation feedback**: Write concise feedback that tells the diagram agent what to fix visually.
- **Replication brief**: Convert an image/PDF/text source into layout, shapes, labels, and style requirements.

## Hard Rules

- Do not include `<mxfile>`, `<diagram>`, `<mxGraphModel>`, or `<root>` when the target expects `mxCell` fragments.
- Do not include root cells `id="0"` or `id="1"` in fragment mode.
- Every cell must have a unique ID and a valid `parent`.
- Top-level shapes use `parent="1"`; children use their container ID.
- Every vertex needs `mxGeometry` with x, y, width, and height.
- Every edge should specify natural exit and entry points in style.
- Use waypoints when a direct edge would cross another shape.
- Do not write XML comments; draw.io strips them and they break edit patterns.
- Escape user-visible XML text: `&`, `<`, `>`, and quotes where needed.

## References

- Index and workflow: `next-ai-drawio-writing-index.md`
- Output templates: `templates/diagram-writing-templates.md`
- Source project path: `<LOCAL_SKILL_WORKSPACE>/next-ai-draw-io`
- Shape library docs in source project: `<LOCAL_SKILL_WORKSPACE>/next-ai-draw-io/docs/shape-libraries`

