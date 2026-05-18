---
name: openapi-contract-and-mock-server
description: Generate OpenAPI contracts and independent mock servers from domain models and product blueprints. Use when creating `03-contracts/` and `04-mock-server/` with OpenAPI, Prism contract mock, Fastify TypeScript project mock, scenarios, errors, latency, and permission states.
---

# OpenAPI Contract And Mock Server

## Purpose

Produce the API contract and a real HTTP mock-server. Front-end apps must call this mock-server instead of reading local mock data.

## Inputs

```text
01-domain-model/domain-model.json
02-product-blueprint/
```

## Outputs

```text
03-contracts/
  openapi.yaml
  01-api-review.md
  02-api-version.md
  03-compatibility-report.md
  examples/

04-mock-server/
  package.json
  src/
    server.ts
    routes/
    data/
    scenarios/
    errors/
    latency/
    permissions/
```

## Technology

- OpenAPI for contracts.
- Prism for contract mock.
- Fastify + TypeScript for project mock behavior.
- openapi-diff for compatibility checks.

## Standard APIs

For YJXZS-like products, start with:

- `GET /api/dashboard`
- `GET /api/todos`
- `GET /api/messages`
- `GET /api/services`
- `GET /api/profile-stats`
- `POST /api/todos/{id}/complete`
- `POST /api/messages/{id}/read`

## Mock Server Requirements

Fastify mock-server must support:

- Scenario data
- Error codes
- Response latency
- Permission states
- POST state mutation
- JSON data files

## Rules

- `openapi.yaml` is the source of truth.
- Include examples for all core responses.
- Keep mock-server independent from front-end dev server.
- Use TypeScript.
- Do not use Express as the default enterprise mock-server.

## References

Read `references/01-openapi-rules.md` before generating contracts.
