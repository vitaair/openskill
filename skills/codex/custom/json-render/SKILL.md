---
name: json-render
description: "Use when designing, implementing, reviewing, or explaining json-render style generative UI: catalog-constrained components, AI-generated JSON specs, streaming JSON Patch UI, state/actions/validation, and multi-renderer output for React, Vue, Svelte, Solid, React Native, PDF, image, video, email, terminal, or Next.js apps."
---

# json-render

Use this skill when the task involves building or analyzing a `json-render` style system: AI produces a constrained JSON spec, and the host app renders it through a known component registry instead of letting the model write arbitrary UI code.

## Fast Path

1. Read `json-render-index.md` for the full capability model and source map.
2. Identify the target output: React UI, shadcn UI, Vue, Svelte, Solid, React Native, Next.js app, PDF, image, video, email, terminal UI, or code export.
3. Define the catalog first: allowed components, Zod prop schemas, descriptions, slots, actions, and sample data expectations.
4. Define the registry second: map every catalog component to a real implementation and every action to a safe handler.
5. Generate or accept specs only inside that catalog. Prefer flat specs with `root`, `elements`, and optional `state`.
6. For AI generation, use `catalog.prompt()` plus explicit rules and stream JSON Patch lines when progressive rendering matters.
7. Wrap renderers with state, visibility, action, and validation providers when interactivity is required.
8. Validate specs and test with realistic prompts, missing-child cases, state binding, actions, and streaming/refinement flows.

## Core Concepts

- **Catalog**: the guardrail. It declares what the model is allowed to use.
- **Registry**: the runtime mapping. It turns catalog names into real components/actions.
- **Spec**: the generated JSON UI tree. It should be data, not executable code.
- **State**: top-level `state` plus JSON Pointer paths for dynamic UI.
- **Dynamic props**: `$state`, `$bindState`, `$bindItem`, `$cond`, `$template`, `$computed`.
- **Actions**: event bindings such as `on.press`, plus built-ins like `setState`, `pushState`, `removeState`, `validateForm`.
- **Streaming**: JSON Patch / JSONL updates let the UI appear progressively.

## When To Use

- AI dashboard/widget generation
- Chat messages with rich interactive UI
- Low-code or no-code page builders
- Dynamic forms with validation and cascading fields
- Controlled enterprise AI interfaces
- Multi-platform rendering from one constrained UI model
- Exporting generated UI to project-specific code

## Guardrails

- Do not let AI invent components outside the catalog.
- Do not put events or visibility inside `props`; they belong on the element.
- Do not use `statePath` as a generic component prop for two-way binding; use `$bindState` on the natural value prop.
- Ensure every child key exists in `elements`.
- Use realistic sample data when a UI displays records, products, posts, metrics, or other data.
- Prefer repeat scopes for arrays instead of hardcoding one element per item.
- Keep actions named and typed; map them to safe host functions.

## Source Project

Local source checkout:

`<LOCAL_SKILL_WORKSPACE>/json-render`

Useful source files:

- `README.md`
- `packages/core/src/schema.ts`
- `packages/core/src/prompt.ts`
- `packages/core/src/types.ts`
- `packages/core/src/props.ts`
- `packages/core/src/actions.ts`
- `packages/react/src/schema.ts`
- `packages/react/src/renderer.tsx`
- `packages/react/src/hooks.ts`
- `examples/dashboard`
- `examples/chat`
- `examples/no-ai`
- `examples/next-website-builder`

