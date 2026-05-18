# json-render Index

This file is the shared source for the `json-render` skill and its cross-tool entrypoints.

## Capability Summary

`json-render` is a generative UI architecture. The model does not emit arbitrary app code. It emits a JSON spec constrained by a catalog. The app validates and renders that spec through a registry of known components and actions.

```text
User prompt
  -> catalog.prompt()
  -> AI outputs JSON spec or JSON Patch stream
  -> spec validation / patch application
  -> renderer + registry
  -> native UI/output
```

## Mental Model

The catalog is the contract with the model. The registry is the contract with the runtime.

- Catalog answers: "What may the AI use?"
- Registry answers: "How does this app render and execute it?"
- Spec answers: "What UI instance should exist right now?"

## Standard Workflow

1. Select renderer and platform.
2. Define allowed components and actions.
3. Write Zod prop schemas and descriptions that guide generation.
4. Create registry implementations.
5. Generate a prompt from the catalog.
6. Stream or parse the generated spec.
7. Render with providers for state, actions, visibility, and validation.
8. Validate edge cases and real prompts.

## Spec Shape

The React-style flat spec normally looks like:

```json
{
  "root": "card-1",
  "elements": {
    "card-1": {
      "type": "Card",
      "props": { "title": "Hello" },
      "children": ["button-1"]
    },
    "button-1": {
      "type": "Button",
      "props": { "label": "Click me" },
      "children": []
    }
  },
  "state": {}
}
```

## Dynamic UI Features

- `$state`: read a JSON Pointer path from state.
- `$bindState`: read and write a state path through a component value prop.
- `$bindItem`: bind a field of the current repeated item.
- `$item`: read a field from a repeated item.
- `$index`: read the repeated item index.
- `$cond`: choose a value based on a visibility condition.
- `$template`: interpolate state or item values into a string.
- `$computed`: call a host-registered function.
- `visible`: show or hide elements using state/item/index conditions.
- `repeat`: render children once per item in a state array.
- `watch`: trigger actions when state paths change.

## Action Model

Events live on the element `on` field:

```json
{
  "type": "Button",
  "props": { "label": "Save" },
  "on": {
    "press": {
      "action": "saveRecord",
      "params": { "id": { "$state": "/record/id" } }
    }
  },
  "children": []
}
```

Built-in React schema actions include `setState`, `pushState`, `removeState`, and `validateForm`.

## Renderer Targets

- React: `@json-render/react`
- shadcn UI: `@json-render/shadcn`
- Vue: `@json-render/vue`
- Svelte: `@json-render/svelte`
- Solid: `@json-render/solid`
- React Native: `@json-render/react-native`
- Next.js apps: `@json-render/next`
- PDF: `@json-render/react-pdf`
- image/SVG/PNG: `@json-render/image`
- video: `@json-render/remotion`
- email: `@json-render/react-email`
- terminal UI: `@json-render/ink`
- 3D scenes: `@json-render/react-three-fiber`

## Common Use Cases

### AI dashboards

Generate metrics, charts, tables, filters, and widget layouts. Use typed business actions for data fetches or mutations.

### Chat with rich UI

Let an assistant call tools, then render interactive cards/charts/tables inline in the conversation.

### Low-code builders

Use prompts or structured edits to generate app screens, landing pages, forms, and dashboards from a controlled component system.

### Dynamic forms

Use `$bindState`, validation checks, `watch`, conditional visibility, and computed values for interactive forms.

### Enterprise guardrails

Expose only approved components and safe actions. The model composes UI but cannot execute arbitrary code.

### Multi-output generation

Render the same catalog/spec pattern to web, mobile, PDF, image, video, email, or terminal targets.

## Implementation Checklist

- Catalog includes only components the app can render.
- Every component has clear descriptions and strict prop schemas.
- Actions are named, described, typed, and implemented safely.
- Registry covers every catalog component.
- Spec child references are complete.
- Repeated data uses `state` plus `repeat`.
- Form components use `$bindState` or `$bindItem`.
- Streaming route handles JSON Patch lines.
- Renderer is wrapped with the required providers.
- Tests cover generation, refinement, invalid specs, and action behavior.

## Local Source Map

Repository:

`<LOCAL_SKILL_WORKSPACE>/json-render`

Read these when implementing:

- `README.md`: package overview and quick starts
- `apps/web/app/(main)/docs/quick-start/page.mdx`: end-to-end React flow
- `apps/web/app/(main)/docs/renderers/page.mdx`: renderer targets
- `packages/core/src/schema.ts`: schema/catalog definitions
- `packages/core/src/prompt.ts`: prompt builder
- `packages/core/src/types.ts`: spec, element, state, patch types
- `packages/core/src/props.ts`: dynamic prop expressions
- `packages/core/src/actions.ts`: action bindings
- `packages/core/src/validation.ts`: validation checks
- `packages/react/src/schema.ts`: React schema and default rules
- `packages/react/src/renderer.tsx`: runtime renderer
- `packages/react/src/hooks.ts`: streaming and helper hooks
- `examples/no-ai`: static specs, forms, validation, computed values
- `examples/dashboard`: AI-generated persisted dashboard widgets
- `examples/chat`: tool-using chat with inline rendered specs
- `examples/next-website-builder`: generated Next.js app/pages pattern

