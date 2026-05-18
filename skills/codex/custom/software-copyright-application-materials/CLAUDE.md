# Claude Code Entry

This is the packaged Claude Code entry for `softcopy-application-materials`.

Start with:

```text
<SOFTWARE_COPYRIGHT_WORKSPACE>/00_入口与索引/00_新会话入口.md
```

Use this Skill workspace root:

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

Important references:

```text
软著申请材料/00_通用说明/00_资料状态识别入口.md
软著申请材料/00_通用说明/00_项目类型识别入口.md
软著申请材料/00_通用说明/00_软著Skill本地记忆宫殿规范.md
软著申请材料/00_通用说明/00_软著图生成规范_next_ai_drawio.md
软著申请材料/tools/README.md
<LOCAL_SKILL_WORKSPACE>/NextAIDrawIO写作SKILL/SKILL.md
<LOCAL_SKILL_WORKSPACE>/DrawIO架构图生成SKILL/SKILL.md
```

Keep this file as a pointer only. The source of truth lives in the referenced files.

Formal architecture diagrams must use `DrawIO架构图生成SKILL`; it may use `NextAIDrawIO写作SKILL` for diagram writing and validation before `.drawio` packaging/export.
Final documents embed generated PNG/SVG screenshots; keep `.drawio/cells.xml` as source.
