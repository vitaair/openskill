# PJ5 大数据二期三件套生成规范

本规范用于复现当前 PJ5 三个医药大数据软著申报材料。目标是生成与当前工作区一致的正式提交版材料，而不是生成历史过程文件。

## 工作区

当前材料工作区：

```text
<SOFTWARE_COPYRIGHT_WORKSPACE>/软著申请材料/PJ5-YJS-大数据二期三件套
```

公共申请表模板：

```text
<SOFTWARE_COPYRIGHT_WORKSPACE>/软著申请材料/00_通用说明/00_申请表-模版.doc
```

源工程位置：

```text
<LOCAL_PATH>
```

## 三个申报系统

| 项目 | 软件全称 | 简称 | 版本 |
| --- | --- | --- | --- |
| PJ1 | 医药主数据管理系统 | MDM | V1.0 |
| PJ2 | 医药数据资产目录系统 | DAC | V1.0 |
| PJ3 | 医药交易主题分析系统 | DWA | V1.0 |

统一归属关系说明：

```text
以上三个系统均为医药大数据平台的核心组成系统，分别承担主数据治理、数据资产管理与交易分析三大核心职能。
```

不得在申报名称中使用旧长名或“子系统”表述。

## 生成入口

在工作区根目录执行：

```bash
./build.sh all
```

该入口必须完成：

1. 生成 `01_系统说明书.md/.docx/.pdf`。
2. 生成 `02_源程序代码.md/.docx/.pdf`。
3. 基于公共模板生成 `03_计算机软件著作权登记申请表.md/.docx/.pdf`。
4. 清理 `04_提交版/md`、`04_提交版/word`、`04_提交版/pdf` 中除 01、02、03 以外的文件。

单项目生成：

```bash
./build.sh pj1
./build.sh pj2
./build.sh pj3
```

## 核心脚本

| 脚本 | 职责 |
| --- | --- |
| `tools/build_soft_copyright_materials.py` | 统一编排三项目生成、Word 导出、PDF 导出和提交目录清理。 |
| `tools/build_pj1_operation_manual.py` | 生成 PJ1 系统说明书。 |
| `tools/build_project_system_description.py` | 生成 PJ2/PJ3 系统说明书。 |
| `tools/build_pj1_source_package.py` | 生成 PJ1 源程序代码鉴别材料。 |
| `tools/build_project_source_package.py` | 生成 PJ2/PJ3 源程序代码鉴别材料。 |
| `tools/build_application_forms.py` | 从公共 `.doc` 模板生成三项目登记申请表。 |
| `tools/export_md_to_docx.py` | Markdown 到 Word 的统一导出器，使用软著要求的黑色字体、A4、表格自适应。 |
| `tools/check_soft_copyright_rules.py` | 调用公共质检脚本并叠加 PJ5 项目定制规则。 |

## 源程序配置

源码摘录配置必须存在：

```text
config/pj1_extract.yaml
config/pj2_extract.yaml
config/pj3_extract.yaml
```

每个配置必须包含软件全称、简称、`V1.0`、`front_30_pages`、`back_30_pages` 和 `generated_material_line`。源程序 PDF 必须为 60 页，前后各 30 页口径。

## 申请表规则

申请表必须从公共模板派生，但不得保留模板里的示例系统名或 LibreOffice 转换异常符号。

必须使用稳定勾选符：

```text
☑应用软件
☑原创
☑未发表
☑独立开发
☑原始取得
☑全部
☑企业法人
☑一般交存
☑一种文档
```

不得出现：

```text
R应用软件
£嵌入式软件
R原创
£已发表
R未发表
R独立开发
R原始取得
R企业法人
R一般交存
R一种文档
£例外交存
```

## 正式提交目录

每个项目的 `04_提交版` 只保留以下文件：

```text
md/01_系统说明书.md
md/02_源程序代码.md
md/03_计算机软件著作权登记申请表.md
word/01_系统说明书.docx
word/02_源程序代码.docx
word/03_计算机软件著作权登记申请表.docx
pdf/01_系统说明书.pdf
pdf/02_源程序代码.pdf
pdf/03_计算机软件著作权登记申请表.pdf
```

不要在正式提交目录保留 `00_提交材料清单`、主体证明、代理委托书、PDF 检查表或其它过程文件。

## 验证

生成后必须执行：

```bash
<LOCAL_PATH> tools/check_soft_copyright_rules.py
```

期望输出：

```text
PASS
```

视觉复核申请表时使用 Documents 技能的 `render_docx.py` 渲染 Word 到 PNG，确认申请表为 2 页、勾选框显示正常、没有空白页。

## 版本记录

每轮生成、质检和修复必须维护两个独立文件：

```text
00_公共来源材料/材料索引/质检报告版本记录.md
00_公共来源材料/材料索引/质检问题修复版本记录.md
```

`质检报告版本记录.md` 只记录质检报告版本、范围、结论和剩余人工确认项；`质检问题修复版本记录.md` 只记录风险点、修复动作、影响文件和验证结果。不要把两类记录混在 `05_质检_本轮汇总` 或普通进度文件里。

## 常见故障

- 如果申请表出现 `R/£`，说明模板转换后的勾选符没有被脚本覆盖，修复 `tools/build_application_forms.py` 后重新生成。
- 如果 `04_提交版` 出现 00、05、06 等多余文件，修复或重跑 `tools/build_soft_copyright_materials.py` 的清理逻辑。
- 如果 PDF 未更新，确认 `/opt/homebrew/bin/soffice` 可用，并重新执行 `./build.sh all`。
- 如果截图比例错误，优先修复系统说明书生成脚本中的截图预处理，不要手工改 Word。
