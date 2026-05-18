---
name: domain-model-to-product-blueprint
description: Convert a validated domain model into product blueprints, page maps, user flows, state flows, permission matrices, and component rules. Use after `01-domain-model/domain-model.json` exists and before generating OpenAPI contracts, mock servers, or front-end code.
---

# Domain Model To Product Blueprint

## Purpose

Turn the domain model into a product execution plan. This step decides pages, flows, states, permissions, and reusable business components.

## Inputs

```text
01-domain-model/domain-model.json
01-domain-model/01-domain-model.md
```

## Outputs

```text
02-product-blueprint/
  01-page-map.md
  02-user-flow.md
  03-state-flow.md
  04-permission-matrix.md
  05-component-rules.md
```

## Workflow

1. Identify product surfaces:
   - Mobile workbench
   - Todo center
   - Message center
   - Service center
   - Profile/status/data page
   - PC admin when required
2. Map domain features to pages.
3. Define user flows for core tasks.
4. Define state transitions for todo handling, message read state, service subscription, and permission checks.
5. Define RBAC permission matrix.
6. Define reusable components.

## Standard Page Map

For YJXZS-like mobile projects:

- 首页: 经营概览、关键预警、今日重点、快捷操作
- 待办: 议价、合同、资质、价格确认等可处理事项
- 消息: 公告、结果、预警、反馈
- 服务: 分类筛选、模板查看、流程指引
- 我的/数据: 企业状态、产品状态、交易指标

PC admin is a parallel management line and should use Umi + Ant Design Pro when generated.

## Component Rules

Use NutUI React for mobile base components. Wrap business components:

- `MetricCard`
- `TodoItem`
- `MessageItem`
- `ServiceCard`
- `StatusBadge`
- `TemplatePreview`
- `FlowTimeline`
- `PermissionGuard`

## Rules

- Keep product blueprint independent from framework implementation.
- Do not write code in this step.
- Use numeric Markdown filenames.
