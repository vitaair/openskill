---
name: ui-design-fidelity-reviewer
description: Generate, register, and verify mobile UI target images/design drafts for Taro H5 delivery. Use before claiming mobile UI completion, especially when `02-product-blueprint/07-mobile-ui-reference.md` is missing, draft, or not confirmed.
---

# UI Design Fidelity Reviewer

## Purpose

Act as the independent UI verification role for mobile delivery.

This role is responsible for:

- generating a mobile UI target draft when no target exists
- recording the confirmed target image/design path
- defining visual acceptance criteria
- preventing fake UI completion claims
- reviewing runtime screenshots against the confirmed UI reference

This role does not replace product, frontend, or verification roles. It is a gatekeeper between frontend implementation and completion reporting.

## Inputs

```text
02-product-blueprint/
05-frontend/mobile-h5-app/
06-verification/reports/
```

Optional:

```text
02-product-blueprint/ui-targets/
```

## Outputs

```text
02-product-blueprint/07-mobile-ui-reference.md
02-product-blueprint/ui-targets/
06-verification/reports/03-mobile-ui-fidelity.json
```

## Reference Document Schema

`02-product-blueprint/07-mobile-ui-reference.md` must include:

```text
status: draft | confirmed
ownerRole: ui-design-fidelity-reviewer
targetImage: <path>
reviewMethod: manual-screenshot-review | visual-diff
approvedBy:
approvedAt:
```

## Workflow

### 01. Discover Target

If the user provided a UI image, design file, Figma link, screenshot, or reference app:

- copy or reference it under `02-product-blueprint/ui-targets/`
- record it as `targetImage`
- keep `status: draft` until user confirms it is the target

If no target exists:

- create a mobile UI draft image or screenshot
- record it under `02-product-blueprint/ui-targets/`
- keep `status: draft`
- ask for confirmation before allowing fidelity pass

### 02. Define Visual Acceptance Criteria

Record checks for:

- viewport size
- page structure
- first-screen density
- navigation shape
- icon visibility
- spacing
- typography hierarchy
- color/token usage
- key business modules
- empty/error/loading states when relevant

### 03. Review Runtime Screenshots

Use screenshots from:

```text
05-frontend/mobile-h5-app/h5-home-localhost.png
05-frontend/mobile-h5-app/h5-home-lan.png
```

Compare them against `targetImage`.

The review must fail when:

- reference status is not `confirmed`
- target image is missing
- runtime screenshots are missing
- bottom navigation has blank icons
- major layout differs from target
- page looks like a PC page squeezed into mobile width
- UI was passed through hidden elements or fake placeholders

### 04. Report

Write report:

```text
06-verification/reports/03-mobile-ui-fidelity.json
```

Report must include:

- `passed`
- `targetImage`
- `runtimeScreenshots`
- `reviewMethod`
- `reviewerRole`
- `failures`
- `notes`

## Completion Rule

Mobile UI completion can only be reported when:

- `status: confirmed`
- `ownerRole: ui-design-fidelity-reviewer`
- `targetImage` exists
- runtime screenshots exist
- review report passes

## Anti-Fake Rules

- Do not accept DOM/text existence as UI fidelity.
- Do not accept empty image tags as icons.
- Do not approve UI without screenshot evidence.
- Do not approve a self-invented UI unless the user has confirmed it as the target.
- Do not mark draft references as complete.
