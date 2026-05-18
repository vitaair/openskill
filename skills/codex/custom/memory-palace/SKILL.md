---
name: memory-palace
description: Use when creating, updating, migrating, auditing, or reading long-term Markdown memory for a project, agent, workflow, or multi-agent collaboration. Applies the AI/Agent memory palace method with nine zones, memory cards, lifecycle states, source/index separation, project onboarding, and continuation notes.
---

# 记忆宫殿

Use this skill when a user asks to record lasting project knowledge, build a reusable project memory, continue work across sessions, migrate project notes, audit existing notes, or design an Agent-friendly index.

## Fast Path

1. Read the workspace skill index if present: `skill-index.md`.
2. Read this skill index: `ai-memory-index.md`.
3. For a target project, install lightweight entrypoints, create or update project memory, then register the project in the index.

For another project, install entrypoints:

```bash
<LOCAL_SKILL_WORKSPACE>/记忆宫殿SKILL/scripts/install-agent-entrypoints.sh /path/to/project
```

Then create a project memory file, usually `AI_MEMORY.md`, using the nine zones:

- 入口：identity, goal, phase, success criteria
- 门厅：global rules, user preferences, constraints
- 地图：documents, paths, entrypoints, datasets, APIs
- 展厅：domain concepts, entities, terms, business rules
- 工坊：repeatable workflows, commands, verification steps
- 档案室：decisions, tradeoffs, architecture records
- 警示墙：risks, traps, fragile assumptions
- 工作台：current task state, blockers, next actions
- 出口：handoff, next-start instructions, unresolved questions

## Write Rules

- Record only information with future value: goals, constraints, decisions, rules, preferences, facts, workflows, risks, open questions.
- Preserve the source layer separately from the index layer. Do not turn uncertain summaries into facts.
- Every memory card should include status, zone, tags, trigger scenario, content, usage, source, and update date.
- Use lifecycle states: `active`, `draft`, `deprecated`, `superseded`, `archived`.
- When old and new memory conflict, keep both long enough to record replacement reason, date, and source.
- Prefer incremental edits. Avoid rewriting the whole memory unless migration is the explicit task.

## Read Rules

- For continuation work, read in this order: index, project memory entry, exit zone, workbench, warning wall, relevant map/workshop/archive sections.
- If context is tight, use L0-L3 reading:
  - L0: index and next-start hints
  - L1: active task and warnings
  - L2: relevant workflows and decisions
  - L3: source materials, books, diagrams, external references

## References

- Full method: `ai-agent-memory-palace.md`
- Template: `ai-memory-template.md`
- Example: `ai-memory-example-project.md`
- Index: `ai-memory-index.md`
- Diagrams: `diagrams/memory-palace-diagrams.md` and `diagrams/memory-palace-architecture.drawio`
- Workspace skill registry: `<LOCAL_SKILL_WORKSPACE>/skill-index.md`

Keep this skill independent. External projects should be referenced by path or URL, not copied into this skill.
