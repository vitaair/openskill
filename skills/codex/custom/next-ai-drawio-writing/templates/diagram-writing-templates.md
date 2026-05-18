# Diagram Writing Templates

## Natural-Language Prompt

```markdown
Create a [diagram type] about [topic].

Audience: [who will read it]
Goal: [what the diagram must explain]
Layout: [left-to-right / top-to-bottom / swimlanes / layered architecture / radial]
Elements: [nodes, actors, systems, entities]
Relationships: [flows, dependencies, ownership, timing]
Style: [minimal / professional / sketch / cloud architecture / animated connectors]
Constraints: keep everything in one viewport, avoid overlapping edges, label important edges.
```

## Diagram Brief

```markdown
## Diagram Goal

[One sentence.]

## Layout Plan

[2-3 sentences about zones, flow direction, grouping, and edge routing.]

## Elements

- id:
  label:
  type:
  position:
  size:
  parent:

## Connections

- from:
  to:
  label:
  route:

## Visual Constraints

- Viewport: x 0-800, y 0-600.
- No shape overlap.
- No edge crosses unrelated shapes.
- Use waypoints for obstacle avoidance.
```

## mxCell Fragment Request

```markdown
Generate only draw.io mxCell elements.

Do not include mxfile, diagram, mxGraphModel, root, or root cells id="0"/id="1".
Use unique IDs starting from "2" or meaningful stable IDs.
Set parent="1" for top-level shapes.
Every vertex must include mxGeometry.
Every edge must include source, target, parent="1", edge="1", and natural exit/entry points.
Keep all elements within x 0-800 and y 0-600.
```

## Edit Operation Request

```markdown
Modify the existing diagram using ID-based operations.

Current target cells:
- [cell_id]: [current role]

Required changes:
- [add/update/delete] [cell_id]: [exact change]

Return operations only. For add/update, include the complete replacement mxCell.
```

## Validation Feedback

```markdown
Diagram validation issues:

- [critical/warning] [issue type]: [where it appears and why it matters]

Suggested fixes:

- [specific layout or XML-level fix]
```

