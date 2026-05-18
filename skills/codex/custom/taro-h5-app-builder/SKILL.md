---
name: taro-h5-app-builder
description: Build mobile H5 front-end apps using React, Taro, TypeScript, and NutUI React from OpenAPI contracts and product blueprints. Use when creating `05-frontend/mobile-h5-app/` that calls an independent mock-server through HTTP APIs.
---

# Taro H5 App Builder

## Purpose

Generate the mobile front-end app. The first target is Taro H5, with future downstream expansion to mini programs and App.

## Inputs

```text
02-product-blueprint/
03-contracts/openapi.yaml
04-mock-server/
```

## Outputs

```text
05-frontend/mobile-h5-app/
```

## Technology

- React
- Taro
- TypeScript
- NutUI React
- openapi-typescript + openapi-fetch

## Standard Pages

- `home`
- `todo`
- `messages`
- `services`
- `profile`

## Standard Components

Use NutUI React for base components. Wrap business components:

- `MetricCard`
- `TodoItem`
- `MessageItem`
- `ServiceCard`
- `StatusBadge`
- `Sheet`
- `TemplatePreview`
- `FlowTimeline`
- `PermissionGuard`

## API Rules

- Front-end must call the independent mock-server through HTTP.
- H5 should support localhost and LAN access. Prefer deriving the API host from `window.location.hostname`, with an explicit override such as `window.__YJXZS_API_BASE_URL__` when integrating with a real backend.
- Do not import mock data directly into pages.
- Keep API access inside `src/api`.
- Generate or align API types from OpenAPI.

## Rules

- Build an operational app surface, not a landing page.
- Keep mobile H5 as the first delivery target.
- Preserve later Taro targets: mini program and App.
- Mobile UI must match a confirmed target image/design. Without a confirmed target, produce a draft and do not claim UI completion.
- Do not use empty images, hidden DOM, or text-only checks to fake UI completion.
