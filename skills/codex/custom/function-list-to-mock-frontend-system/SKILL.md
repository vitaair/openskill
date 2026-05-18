---
name: function-list-to-mock-frontend-system
description: End-to-end enterprise workflow that turns a raw service/function list into OpenAPI contracts, mock interface data, an independent mock-server, and a runnable Taro H5 frontend, with feature-to-frontend traceability, startup checks, and mobile UI fidelity gates. Use when a new project starts from `00-requirements-input/` and needs a mock-data frontend rather than backend code.
---

# Function List To Mock Frontend System

## Purpose

Orchestrate the full delivery chain from raw function list to runnable mock-data frontend.

The default scope stops at:

```text
03-contracts + 04-mock-server + 05-frontend + 06-verification
```

Backend code generation is optional and must not block this skill.

This is a controller skill. It coordinates the lower-level skills:

1. `requirement-to-domain-model`
2. `domain-model-to-product-blueprint`
3. `openapi-contract-and-mock-server`
4. `taro-h5-app-builder`
5. `verification-runner`
6. `ui-design-fidelity-reviewer`

Use this skill when the expected result is not only documents, but a working H5 frontend that calls an independent mock-server through HTTP.

## Required Inputs

```text
00-requirements-input/
```

At minimum:

```text
00-requirements-input/01-source-function-list.md
```

Optional but recommended:

```text
00-requirements-input/02-source-notes.md
00-requirements-input/03-source-attachments/
00-requirements-input/04-change-log.md
00-requirements-input/05-approval-record.md
```

## Required Outputs

```text
01-domain-model/
02-product-blueprint/
03-contracts/
04-mock-server/
05-frontend/mobile-h5-app/
06-verification/
```

Required traceability and verification files:

```text
02-product-blueprint/06-feature-frontend-traceability.md
02-product-blueprint/07-mobile-ui-reference.md
02-product-blueprint/diagrams/*.drawio
02-product-blueprint/diagrams/*.svg
06-verification/reports/01-h5-mock-verification.json
06-verification/reports/02-feature-frontend-coverage.json
06-verification/reports/03-mobile-ui-fidelity.json
06-verification/reports/04-diagram-verification.json
06-verification/reports/05-platform-independence.json
```

## Workflow

### 01. Requirements To Domain Model

Run `requirement-to-domain-model`.

Gate:

- `01-domain-model/domain-model.json` exists.
- `01-domain-model/schema/domain-model.schema.json` exists.
- Domain model validates with Ajv.
- Every source row has a stable feature id and source reference.

Do not proceed if the domain model is invalid.

### 02. Domain Model To Product Blueprint

Run `domain-model-to-product-blueprint`.

Gate:

- Page map exists.
- User flow exists.
- State flow exists.
- Permission matrix exists.
- Component rules exist.
- Every feature has a page/category placement.

### 03. Contracts And Mock Server

Run `openapi-contract-and-mock-server`.

Gate:

- `03-contracts/openapi.yaml` parses as OpenAPI.
- Examples exist for core APIs.
- `04-mock-server` starts independently from the frontend dev server.
- Mock APIs are real HTTP endpoints, not Vite/Taro middleware.

Required baseline APIs:

- `GET /api/health`
- `GET /api/dashboard`
- `GET /api/todos`
- `POST /api/todos/{id}/complete`
- `GET /api/messages`
- `POST /api/messages/{id}/read`
- `GET /api/services`
- `GET /api/profile-stats`

### 04. Feature To Frontend Traceability

Generate:

```text
02-product-blueprint/06-feature-frontend-traceability.md
```

Gate:

- Every function-list feature appears in the traceability table.
- Every feature maps to:
  - frontend page or entry
  - API endpoint
  - current realization form
  - coverage status
- Missing count must be `0`.

Run:

```bash
npm run verify:feature-coverage
```

### 05. Mobile UI Reference

Run `ui-design-fidelity-reviewer`.

Generate or update:

```text
02-product-blueprint/07-mobile-ui-reference.md
```

Rules:

- If a target UI image/design exists, record it as `targetImage: <path>`.
- If no target UI exists, create a draft design screenshot and keep `status: draft`.
- The reference must declare `ownerRole: ui-design-fidelity-reviewer`.
- The reference must declare `reviewMethod: manual-screenshot-review` or `reviewMethod: visual-diff`.
- Only after user approval may the file be changed to `status: confirmed`.
- Without `status: confirmed`, mobile UI fidelity must fail.

Do not claim UI completion when the reference is not confirmed.

### 06. Taro H5 Frontend

Run `taro-h5-app-builder`.

Gate:

- H5 app builds successfully.
- H5 app starts on `0.0.0.0`, so both localhost and LAN access work.
- Pages call `src/api` only.
- Pages do not import mock JSON directly.
- API base URL works for both:
  - `http://127.0.0.1:4173`
  - `http://<local-ip>:4173`

Mobile UI gate:

- Do not shrink a PC page and call it mobile.
- Bottom navigation must have visible, non-empty icons.
- No red overlay, blank icon, hidden fake element, or large meaningless blank area.
- Real screenshot evidence must exist.

### 07. Verification

Run `verification-runner`.

Required command:

```bash
npm run system:check
```

The system gate must include:

- mock-server health
- H5 startup
- localhost browser validation
- LAN browser validation
- real HTTP API calls
- feature coverage validation
- mobile UI fidelity validation
- detailed skill flow/architecture diagram generation
- draw.io diagram structure validation
- platform independence validation: `YJXZS-STD-PLATFORM-INDEPENDENCE-001`

If `npm run system:check` fails, report the failure honestly and do not mark the stage complete.

### 08. Detailed Diagrams

Generate detailed flowcharts and architecture diagrams by following the `next-ai-draw-io` pattern.

Required outputs:

```text
02-product-blueprint/diagrams/01-skill-end-to-end-flow.drawio
02-product-blueprint/diagrams/01-skill-end-to-end-flow.svg
02-product-blueprint/diagrams/02-skill-architecture.drawio
02-product-blueprint/diagrams/02-skill-architecture.svg
02-product-blueprint/diagrams/03-stage-gate-map.drawio
02-product-blueprint/diagrams/03-stage-gate-map.svg
02-product-blueprint/diagrams/diagram-source/*.cells.xml
```

Rules:

- Generate draw.io-compatible `mxCell` elements and wrap them into `.drawio` files.
- Use stable cell ids so future edits can update/add/delete cells by id.
- Keep diagrams in a single readable viewport.
- Use explicit orthogonal edge styles with source and target ids.
- Do not draw vague concept bubbles. Every node must correspond to a stage, skill, directory, artifact, or verification gate.
- Output SVG previews alongside editable `.drawio` files.

Gate:

```bash
npm run verify:diagrams
```

The diagram gate must check:

- files exist
- XML wrapper exists
- ids are unique
- edge source/target ids exist
- required stages and labels appear

### Optional. Java Backend Skeleton

Do not generate backend code by default.

Only run `java-backend-skeleton-builder` when the user explicitly asks for backend code or backend integration preparation.

The mock frontend workflow is complete without:

```text
07-backend-skeleton-java/
```

## Completion Definition

The project is not complete when files are generated.

The project is not complete when build passes.

The project is not complete when ports are listening.

Completion requires:

- domain model valid
- contracts valid
- mock-server running
- H5 running
- frontend calls mock-server through HTTP
- function list maps to frontend one by one
- mobile UI has confirmed reference and fidelity gate passes
- `npm run system:check` passes

Completion does not require Java backend code.

## Reporting Format

Use this format after each stage:

```text
阶段：
产出：
验证：
结果：
问题：
下一步：
```

## Anti-Fake Rules

- Do not use hidden DOM text to pass checks.
- Do not use empty images or placeholders as successful icons.
- Do not count elements as visual success unless they visibly render.
- Do not report UI fidelity as passed without a confirmed target UI reference.
- Do not report localhost success as LAN success.
- Do not report mock data frontend success if pages import mock JSON directly.
