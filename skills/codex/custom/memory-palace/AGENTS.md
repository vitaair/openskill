# AI Memory Palace Agent Instructions

This repository is the single source for the AI/Agent memory palace method.

When an agent needs long-term project memory, reusable notes, handoff records, migration notes, or an Agent-readable project index, use this method:

1. Read the workspace skill registry if present: `<LOCAL_SKILL_WORKSPACE>/skill-index.md`.
2. Read `SKILL.md` for the fast workflow.
3. Read `ai-memory-index.md` to find the full method, template, examples, diagrams, and references.
4. Use `ai-memory-template.md` when creating a project memory file.
5. Keep external projects as references by URL or path. Do not copy external repositories into this skill.

Core structure:

- 入口：identity, goal, phase, success criteria
- 门厅：global rules, preferences, constraints
- 地图：documents, paths, entrypoints, datasets, APIs
- 展厅：domain concepts, entities, terms, business rules
- 工坊：repeatable workflows, commands, verification steps
- 档案室：decisions, tradeoffs, architecture records
- 警示墙：risks, traps, fragile assumptions
- 工作台：current task state, blockers, next actions
- 出口：handoff, next-start instructions, unresolved questions

For other projects, add a small project-level `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or Cursor rule that points back to this directory instead of copying the full method.
