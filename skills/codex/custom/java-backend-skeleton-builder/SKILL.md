---
name: java-backend-skeleton-builder
description: Generate Java backend skeletons from OpenAPI contracts using Spring Boot MVC, Gradle, MyBatis by default, MySQL 8 by default, with optional MyBatis-Plus, JPA, PostgreSQL, and OceanBase support. Use after `03-contracts/openapi.yaml` is stable enough for backend implementation.
---

# Java Backend Skeleton Builder

## Purpose

Generate a Java backend skeleton that can replace the mock-server during integration.

## Inputs

```text
03-contracts/openapi.yaml
```

## Outputs

```text
07-backend-skeleton-java/
```

## Default Stack

- Spring Boot MVC
- Gradle
- MyBatis
- MySQL 8
- Jackson

## Supported Variants

- MyBatis-Plus
- JPA
- PostgreSQL
- OceanBase

## Dependency Rules

Do not default to:

- Hutool
- fastjson / fastjson2
- Large all-purpose utility libraries

Prefer:

- JDK
- Spring Framework
- Spring Boot
- Jackson
- Small project-specific utility classes only when needed

## Workflow

1. Generate server stubs from OpenAPI using OpenAPI Generator.
2. Ensure Gradle project structure.
3. Add MyBatis mapper/service/controller layering.
4. Configure MySQL 8 default profile.
5. Add placeholder profiles for PostgreSQL and OceanBase if required.
6. Keep generated controllers aligned with OpenAPI paths.

## Rules

- API paths and response structures must remain compatible with OpenAPI.
- Front-end should switch only API base URL when moving from mock-server to backend.
- Use Gradle Wrapper when producing a runnable skeleton.
