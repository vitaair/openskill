---
name: verification-runner
description: Create and run enterprise verification for generated apps, contracts, mock servers, and H5 flows. Use when producing `06-verification/` with Node, TypeScript, Playwright, Ajv schema validation, OpenAPI checks, compatibility checks, and reports.
---

# Verification Runner

## Purpose

Verify the generated project before backend implementation and front-end/back-end integration.

## Inputs

```text
01-domain-model/
03-contracts/
04-mock-server/
05-frontend/
```

## Outputs

```text
06-verification/
  package.json
  tests/
  reports/
```

## Technology

- Node
- TypeScript
- Playwright
- Ajv
- openapi-diff
- Schemathesis where useful

## Required Checks

1. Domain model conforms to JSON Schema.
2. OpenAPI is valid.
3. OpenAPI changes are compatible unless explicitly versioned.
4. Mock-server health endpoint works.
5. Core APIs return valid data.
6. Taro H5 loads successfully.
7. Core flows pass:
   - home page
   - todo complete
   - message read
   - service filter
   - template/flow detail
8. Browser console has no blocking errors.
9. Feature list to frontend traceability passes with no missing features.
10. Mobile UI fidelity passes against a confirmed target UI reference.

## Mandatory Gates

For H5 projects, `npm run system:check` must fail when:

- the app only works on localhost but not LAN
- the frontend imports mock data directly
- the bottom navigation contains blank icons
- the page has red overlay / runtime error
- feature coverage is incomplete
- `02-product-blueprint/07-mobile-ui-reference.md` is missing, not confirmed, or has no target image

## Reports

Write reports to:

```text
06-verification/reports/
```

Include screenshots for failed H5 tests.
