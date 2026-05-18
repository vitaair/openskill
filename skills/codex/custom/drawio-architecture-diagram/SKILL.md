---
name: drawio-architecture-diagram
description: >
  Generate, refine, audit, and export professional architecture diagrams with draw.io as the
  single source of truth. Use for platform architecture, system architecture, data architecture,
  technical architecture, application architecture, function architecture, and big-data platform
  architecture diagrams that need .drawio plus consistent SVG/PNG outputs, visual design review,
  template reuse, and NextAIDrawIO-style mxCell/layout discipline.
metadata:
  short-description: Draw.io architecture diagram generation and export
---

# DrawIO 架构图生成 Skill

Use this skill when the user asks to create, optimize, audit, or export architecture diagrams, especially when the output must include `.drawio`, SVG, and PNG.

This skill is independent from the soft-copyright material skill. Other skills may call it, but should not copy its implementation.

## Core Rule

`.drawio` is the only formal diagram source.

The final SVG/PNG must be exported from `.drawio` by draw.io, preferably through the local background draw.io copy created by `scripts/drawio_architecture_engine.py`. Do not maintain long-term independent `.drawio`, SVG, and PNG renderers.

## When To Use

- Platform architecture diagrams
- System architecture diagrams
- Data architecture diagrams
- Technical architecture diagrams
- Application architecture diagrams
- Function architecture diagrams
- Big-data platform architecture diagrams
- Architecture diagram visual design review
- `.drawio` to SVG/PNG consistency fixes
- Template extraction from a manually adjusted architecture diagram

Do not use this skill for ordinary operation-manual screenshots or text-only software documentation.

## Workflow

1. Identify the diagram type and audience.
2. Pick a template from `templates/diagrams/architecture/`.
3. Replace template facts with project facts. Never invent modules, databases, interfaces, or products.
4. Generate or edit `.drawio` with stable IDs and explicit coordinates.
5. Export SVG/PNG from `.drawio` using draw.io.
6. Run visual review:
   - layer names are clear
   - same level uses same font size
   - background colors distinguish levels
   - labels are not over-framed
   - arrows express correct ownership and direction
   - text is centered and not clipped
7. Return the `.drawio`, SVG, PNG paths and any residual review notes.

## Style Rules

- Same-level text must use the same font size.
- Different layers should be separated by background color or bands, not random decoration.
- Layer titles should not be framed like functional buttons unless they are actual nodes.
- Concrete functions use white filled boxes with consistent borders.
- Input/output arrows must express the owning layer, not an accidental nearby module.
- Do not let line labels overlap lines or nodes.
- For architecture diagrams, prefer layered/area layout over process-flow chains.

## Scripts

Template regeneration:

```bash
python3 scripts/generate_architecture_templates.py
```

General engine functions live in:

```bash
scripts/drawio_architecture_engine.py
```

The engine creates a background draw.io copy under `.cache/drawio-background/draw.io.app` when possible. This avoids changing `/Applications/draw.io.app`.

## References

- `references/diagram_references_index.md`: local draw.io reference project index.
- `references/github_reference_assessment.md`: evaluation of cloned reference projects.
- `adapters/drawio_adapter.md`: draw.io generation adapter notes.
- External writing-method skill: `<LOCAL_SKILL_WORKSPACE>/NextAIDrawIO写作SKILL`

