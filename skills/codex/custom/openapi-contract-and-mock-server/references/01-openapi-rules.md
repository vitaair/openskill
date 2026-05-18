# OpenAPI Rules

## Versioning

Use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

## Required Sections

- `openapi`
- `info`
- `servers`
- `paths`
- `components.schemas`
- `components.responses`

## Compatibility Breaking Changes

- Removing a path.
- Removing a response field.
- Changing a field type.
- Adding a new required request field.
- Changing status code semantics.

## Error Model

Use a common error shape:

```json
{
  "code": "PERMISSION_DENIED",
  "message": "权限不足",
  "traceId": "mock-trace-id"
}
```
