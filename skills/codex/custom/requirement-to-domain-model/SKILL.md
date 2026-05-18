---
name: requirement-to-domain-model
description: Convert raw requirement inputs such as service function lists, tables, meeting notes, and business descriptions into a validated domain model for enterprise app delivery. Use when starting a new project from `00-requirements-input/` and needing `01-domain-model/domain-model.json`, schema validation with JSON Schema/Ajv, and model change records.
---

# Requirement To Domain Model

## Purpose

Transform raw inputs into a structured domain model. Do not design UI or APIs in this step. Preserve traceability from source requirement rows to model objects.

## Inputs

Read from:

```text
00-requirements-input/
```

Typical files:

- `01-source-function-list.md`
- `02-source-notes.md`
- `03-source-attachments/`
- `04-change-log.md`
- `05-approval-record.md`

## Outputs

Create or update:

```text
01-domain-model/
  schema/
    domain-model.schema.json
  domain-model.json
  01-domain-model.md
  02-model-change-log.md
```

## Workflow

1. Parse raw function rows into structured service items.
2. Normalize business names while preserving original Chinese labels.
3. Extract roles, modules, services, features, notification templates, frequencies, states, and permissions.
4. Generate `domain-model.schema.json` if missing.
5. Generate `domain-model.json` that conforms to the schema.
6. Write `01-domain-model.md` as a readable explanation.
7. Update `02-model-change-log.md` when model content changes.
8. Validate with JSON Schema + Ajv when Node is available.

## Domain Model Fields

Use these core fields:

- `project`
- `targetUsers`
- `roles`
- `modules`
- `services`
- `features`
- `notifications`
- `states`
- `permissions`
- `sourceRefs`

For service function lists, map:

- 服务大类 → `category`
- 服务类型 → `type`
- 功能指标（细类） → `name`
- 指标口径说明（功能描述） → `desc`
- 发送频率 → `frequency`
- 备注 → `remark`
- 通知模板 → `template`

## Rules

- Do not hard-code UI page decisions here.
- Do not invent APIs here.
- Keep source traceability.
- Prefer explicit arrays over prose-only summaries.
- Ordinary Markdown files must use numeric prefixes.

## References

Read `references/01-domain-model-schema.md` when creating the schema.
