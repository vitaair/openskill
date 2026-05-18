# Domain Model Schema Guide

## Minimum Shape

```json
{
  "project": {
    "code": "yjxzs-drug",
    "name": "药交小助手药品版"
  },
  "targetUsers": [
    "药品卖方交易主体"
  ],
  "roles": [
    {
      "code": "seller",
      "name": "卖方交易主体"
    }
  ],
  "modules": [
    {
      "code": "trade-collaboration",
      "name": "交易协同"
    }
  ],
  "features": [
    {
      "id": "feature-bargain-todo",
      "category": "交易协同",
      "type": "议价管理",
      "name": "药品议价待办提醒",
      "desc": "对买方发起的药品议价进行提醒",
      "frequency": "每日上下午集中推送两次",
      "remark": "统计类，提示待处理数量",
      "template": "待办提醒：您有xx条药品议价待处理，请及时回应。",
      "sourceRef": "00-requirements-input/01-source-function-list.md"
    }
  ]
}
```

## Required Schema Behavior

- Require `project`, `targetUsers`, `modules`, and `features`.
- Require `id`, `category`, `type`, `name`, and `desc` for each feature.
- Allow optional `frequency`, `remark`, `template`, and `sourceRef`.
- Keep schema strict enough to catch missing core fields.
