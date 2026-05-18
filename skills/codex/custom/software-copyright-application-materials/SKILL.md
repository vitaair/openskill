---
name: software-copyright-application-materials
description: Use this skill for software copyright application materials, including project type recognition, operation manuals, design descriptions, source-code exhibits, screenshot continuity checks, draw.io diagram generation, PDF submission packages, and cross-session handoff under this workspace.
---

# Softcopy Application Materials

This is the canonical local skill package for the software copyright application materials workflow. Keep the workspace root separate from this skill package.

Skill package directory:

```text
<LOCAL_SKILL_WORKSPACE>/软著申报材料写作SKILL
```

Before any work, read these files from the Skill workspace root:

```text
<SOFTWARE_COPYRIGHT_WORKSPACE>/00_入口与索引/00_新会话入口.md
<SOFTWARE_COPYRIGHT_WORKSPACE>/软著申请材料/00_通用说明/00_资料状态识别入口.md
<SOFTWARE_COPYRIGHT_WORKSPACE>/软著申请材料/00_通用说明/00_项目类型识别入口.md
<SOFTWARE_COPYRIGHT_WORKSPACE>/软著申请材料/00_通用说明/00_软著Skill本地记忆宫殿规范.md
<SOFTWARE_COPYRIGHT_WORKSPACE>/软著申请材料/00_通用说明/00_软著图生成规范_next_ai_drawio.md
外部图写作 Skill：<LOCAL_SKILL_WORKSPACE>/NextAIDrawIO写作SKILL/SKILL.md
外部架构图生成 Skill：<LOCAL_SKILL_WORKSPACE>/DrawIO架构图生成SKILL/SKILL.md
<SOFTWARE_COPYRIGHT_WORKSPACE>/软著申请材料/tools/README.md
```

Skill workspace root:

```text
<LOCAL_PATH>
```

Always treat this directory as the workspace root for `softcopy-application-materials`. Concrete project directories under `软著申请材料/PJ*-...` are working targets, not the skill workspace root.

Current work object:

```text
软著申报材料写作 Skill/工具
软著申请材料/00_通用说明/
软著申请材料/tools/
```

Use `PJ*-...` paths only when working on a concrete software copyright project. The short symlink path is only to keep an old conversation cwd alive.

References in this skill:

- `references/提交材料清单.md`: read when creating a new material package or checking required submission artifacts.
- `references/版本与原创口径.md`: read when deciding version wording, originality wording, or whether an upgrade/version statement is needed.
- `references/PDF与递交载体规范.md`: read when exporting Word/PDF, preparing scanned attachments, or building a final submission package.
- `references/递交前核对清单.md`: read before final delivery, packaging, or user-facing submission guidance.
- `references/PJ5大数据二期三件套生成规范.md`: read when generating or regenerating the current PJ5 three-system package.

Hard rules:

- Keep external skills/projects independent; reference or call them, do not copy them.
- Always run the material-status branch before project-type classification. Existing project documents must be learned and fact-extracted before generation; evidence-poor projects only produce draft or pending-confirmation materials.
- Do not use MCP for diagram production.
- Formal architecture diagrams must call/reference `DrawIO架构图生成SKILL`; that skill may reference `NextAIDrawIO写作SKILL` for layout plan, diagram brief, mxCell writing, and validation feedback. Final outputs are `.drawio + PNG/SVG + MD/PDF`.
- Final documents embed the generated PNG/SVG screenshots; `.drawio` and `cells.xml` are retained as editable/provenance sources.
- `SR-04:application-fields` 的节点名称统一为“软著申请表”。该节点是人工确认项，负责整理软件名称、版本、著作权人、日期、发表状态、运行环境等申请表字段；不得由自动流程猜测最终事实。
- P4 节点名称统一为：`SR-12 图文内容质检`、`SR-13 图文内容整改`、`SR-13A 图文版式复核`。
- P2、P3 是软著材料参考的系统材料整理和提交版准备阶段；正式材料必须独立进入 `P4 材料落地阶段`，并拆成 `SR-11A 软著申请表落地`、`SR-11B 软件说明书落地`、`SR-11C 软件源代码落地` 三个文件级节点后，才允许进入质量验证。
- `SR-04A 模板提取` 和 `SR-04B 模板规则生成` 属于 P2 材料策划阶段，不放在 P0。P0 只处理项目接入、入口分流和记忆上下文。
- `SR-13:remediation` 跑 P4 图文内容整改流程时必须执行，但自动修复范围排除 SR-04。遇到 SR-04 问题时只生成人工确认项、修订建议和回传记录，不直接代填或修复申请表最终字段。
- `SR-13A:visual-design-review` 在软著材料主流程中显示为“图文版式复核”，只检查截图、图示、Word/PDF 版式和图文一致性；HTML 看板 UI 美工审查属于看板支线，不混入正式材料 P4。
- Prefer `rg` for search and read files in small chunks.
- For the current PJ5 three-system package, the formal submission folder must contain only `01_系统说明书`, `02_源程序代码`, and `03_计算机软件著作权登记申请表` under each of `md/`, `word/`, and `pdf/`.
- Application forms generated from legacy `.doc` templates must normalize checkbox text to `☑/□`; never allow LibreOffice-converted `R/£` checkbox artifacts to remain in formal Word/PDF outputs.
