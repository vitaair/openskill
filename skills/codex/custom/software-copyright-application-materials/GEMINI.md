# Gemini Entry

This is the packaged Gemini entry for `softcopy-application-materials`.

Canonical context entry:

```text
<SOFTWARE_COPYRIGHT_WORKSPACE>/00_入口与索引/00_新会话入口.md
```

Work from this Skill workspace root:

```text
<LOCAL_PATH>
```

Project directories under `软著申请材料/PJ*-...` are targets only, not the workspace root.

Current work object:

```text
软著申报材料写作 Skill/工具
软著申请材料/00_通用说明/
软著申请材料/tools/
```

Follow the shared rules in `软著申请材料/00_通用说明/`. Run `00_资料状态识别入口.md` before `00_项目类型识别入口.md`. Do not duplicate external skills or projects. Do not use MCP for diagram production.

Formal diagrams must call/reference:

```text
<LOCAL_SKILL_WORKSPACE>/NextAIDrawIO写作SKILL/SKILL.md
<LOCAL_SKILL_WORKSPACE>/DrawIO架构图生成SKILL/SKILL.md
```

Use `DrawIO架构图生成SKILL` for formal architecture diagram generation/export; it may use `NextAIDrawIO写作SKILL` for layout plan, diagram brief, mxCell writing, and validation feedback before `.drawio` packaging/export.
Final documents embed generated PNG/SVG screenshots; keep `.drawio/cells.xml` as source.
