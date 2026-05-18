# Agent Entry

This is the packaged cross-tool entry for `softcopy-application-materials`.

Read `<SOFTWARE_COPYRIGHT_WORKSPACE>/00_入口与索引/00_新会话入口.md` first. It is the canonical handoff for this workspace.

Then load only the needed references from:

```text
软著申请材料/00_通用说明/
软著申请材料/tools/
```

Skill workspace root:

```text
<LOCAL_PATH>
```

Concrete `软著申请材料/PJ*-...` directories are project targets, not the workspace root.

Current work object:

```text
软著申报材料写作 Skill/工具
软著申请材料/00_通用说明/
软著申请材料/tools/
```

Rules:

- Use the `PJ*-...` project paths for new work.
- Run `00_资料状态识别入口.md` before `00_项目类型识别入口.md`; existing documents are evidence to learn from, not text to overwrite blindly.
- Treat `3.zly/记忆宫殿SKILL` and `3.zly/next-ai-draw-io` as independent external references.
- Treat `3.zly/NextAIDrawIO写作SKILL` as the required external diagram-writing skill.
- Treat `3.zly/DrawIO架构图生成SKILL` as the required external architecture-diagram generation/export skill.
- Do not duplicate external projects or skills into this workspace.
- Do not use MCP for diagram production.
- Generate formal architecture diagrams by using `DrawIO架构图生成SKILL`; it may reference `NextAIDrawIO写作SKILL` for layout plan, diagram brief, mxCell content, and validation feedback.
- Final documents embed generated PNG/SVG screenshots; retain `.drawio/cells.xml` as source.
