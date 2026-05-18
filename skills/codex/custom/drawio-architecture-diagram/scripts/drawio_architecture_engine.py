#!/usr/bin/env python3
"""Minimal unified entrypoint for the soft-copyright materials engine."""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = ENGINE_ROOT.parents[1]
DEFAULT_TEMPLATE_ROOT = WORKSPACE_ROOT / "00_软著模板"
SYSTEM_DRAWIO_APP = Path("/Applications/draw.io.app")
BACKGROUND_DRAWIO_APP = ENGINE_ROOT / ".cache" / "drawio-background" / "draw.io.app"

RULES = [
    "rules/material_status.md",
    "rules/evidence_levels.md",
    "rules/project_types.md",
    "rules/material_strategy.md",
    "rules/manual_review_rules.md",
    "rules/design_review_rules.md",
    "rules/screenshot_chain.md",
    "rules/application_fields.md",
    "rules/final_checklist.md",
    "rules/submission_artifacts.md",
    "rules/version_originality.md",
    "rules/pdf_delivery.md",
    "rules/memory_policy.md",
    "rules/template_extraction.md",
    "rules/generated_template_rules.md",
]

TEMPLATES = {
    "00_材料说明/资料状态识别报告.md": "templates/material_inventory.md",
    "00_材料说明/截图链路清单.md": "templates/screenshot_index.md",
    "01_申请表/申请表字段确认.md": "templates/application_form/README.md",
    "04_提交版/md/01_操作手册.md": "templates/manual/README.md",
    "04_提交版/md/01_设计说明.md": "templates/design/README.md",
}

DIRS = [
    "00_材料说明",
    "01_申请表",
    "02_源代码",
    "03_截图",
    "03_截图/drawio",
    "03_截图/drawio/diagram-source",
    "04_提交版/md",
    "04_提交版/word",
    "04_提交版/pdf",
    "05_质检",
]

TEMPLATE_MANIFEST = [
    ("application-form", "1、软著申请表-模板.doc", "申请表模板"),
    ("manual-sample", "2、软件说明书范本.doc", "软件说明书范本"),
    ("source-code-sample", "3、软件源代码范本.doc", "软件源代码范本"),
]

TEMPLATE_RULES = [
    (
        "application-form",
        "申请表模板规则",
        "约束软件全称、版本号、著作权人、日期、开发/运行环境、权利取得方式等字段；正式材料中所有名称和版本必须与申请表一致。",
        "SR-04 申请表字段、SR-11 提交版、SR-12 质检",
    ),
    (
        "manual-sample",
        "软件说明书模板规则",
        "约束软件概述、运行环境、功能模块、操作步骤、截图说明和图文顺序；操作手册必须体现登录、主界面、模块跳转和按钮结果。",
        "SR-06 操作手册、SR-09 截图链、SR-12 质检",
    ),
    (
        "source-code-sample",
        "源代码模板规则",
        "约束源程序材料页数、代码连续性、模块覆盖、源码与说明书功能一致性；禁止用依赖包和构建产物冒充核心源码。",
        "SR-08 源码选择、SR-11 提交版、SR-12 质检",
    ),
]


def timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")


def project_name(project_root: Path, software_name: str) -> str:
    return software_name.strip() or project_root.name


def memory_file_path(project_root: Path) -> Path:
    return project_root / "00_材料说明" / f"ai-memory-softcopy-{project_root.name}.md"


def read_confirmations(project_root: Path) -> list[dict]:
    path = project_root / "00_材料说明" / "sr_confirmations.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    confirmations = data.get("confirmations", [])
    return confirmations if isinstance(confirmations, list) else []


def memory_base_lines(project_root: Path, software_name: str) -> list[str]:
    return [
        f"# ai-memory-softcopy-{software_name}",
        "",
        f"更新时间：{timestamp()}",
        "",
        "## 1. 入口：身份与目标",
        "",
        f"- 软件名称：{software_name}",
        "- 申请目标：软著申报材料生成/补齐/质检。",
        "",
        "## 2. 门厅：全局规则",
        "",
        "- 先资料状态识别，再项目类型识别，再生成材料。",
        "",
        "## 3. 地图：知识索引",
        "",
        "- 资料状态识别报告：00_材料说明/资料状态识别报告.md",
        "- 项目类型识别报告：00_材料说明/项目类型识别报告.md",
        "- 截图链路清单：00_材料说明/截图链路清单.md",
        "",
        "## 4. 展厅：核心概念",
        "",
        "- 待补充。",
        "",
        "## 5. 工坊：操作流程",
        "",
        "- 待补充。",
        "",
        "## 6. 档案室：决策记录",
        "",
        "- 待补充。",
        "",
        "## 7. 警示墙：风险与坑",
        "",
        "- 待补充。",
        "",
        "## 8. 工作台：当前任务状态",
        "",
        "- 已初始化材料目录与基础模板。",
        "",
        "## 9. 出口：复盘与下次启动提示",
        "",
        "- 下次先读取本文件、资料状态识别报告、项目类型识别报告。",
        "",
    ]


def write_memory_summary(project_root: Path, memory: Path) -> None:
    confirmations = read_confirmations(project_root)
    text = memory.read_text(encoding="utf-8", errors="ignore")
    summary_lines = [
        "",
        "## SR 节点版本摘要",
        "",
        f"- 更新时间：{timestamp()}",
        f"- 项目路径：{project_root}",
        f"- 确认记录数：{len(confirmations)}",
    ]
    for item in confirmations[-12:]:
        summary_lines.append(
            "- {created_at} | {stage} | {status} | {note}".format(
                created_at=item.get("created_at", ""),
                stage=item.get("stage", ""),
                status=item.get("status", ""),
                note=str(item.get("note", "")).replace("\n", " "),
            )
        )

    marker = "\n## SR 节点版本摘要\n"
    if marker in text:
        text = text.split(marker, 1)[0].rstrip() + "\n" + "\n".join(summary_lines) + "\n"
    else:
        text = text.rstrip() + "\n" + "\n".join(summary_lines) + "\n"
    memory.write_text(text, encoding="utf-8")


def ensure_memory_version(project_root: Path, note: str = "") -> Path:
    if not project_root.exists():
        raise SystemExit(f"Project root does not exist: {project_root}")

    material_dir = project_root / "00_材料说明"
    material_dir.mkdir(parents=True, exist_ok=True)
    memory = memory_file_path(project_root)
    software_name = project_root.name

    if not memory.exists() or memory.stat().st_size == 0:
        memory.write_text("\n".join(memory_base_lines(project_root, software_name)), encoding="utf-8")

    if not has_stage_confirmation(project_root, "SR-14:memory-version"):
        confirm_stage(
            project_root,
            "SR-14:memory-version",
            "confirmed",
            note or "项目记忆已建立或更新，记忆版本节点完成",
        )
    write_memory_summary(project_root, memory)
    return memory


def copy_template(src_rel: str, dst: Path, software_name: str, project_root: Path, overwrite: bool) -> None:
    src = ENGINE_ROOT / src_rel
    if dst.exists() and not overwrite:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    text = text.replace("待填写", "待填写")
    header = (
        f"<!-- Generated by softcopy_engine.py at {timestamp()} -->\n"
        f"<!-- software_name: {software_name} -->\n"
        f"<!-- project_root: {project_root} -->\n\n"
    )
    dst.write_text(header + text, encoding="utf-8")


def init_project(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    project_root.mkdir(parents=True, exist_ok=True)
    software_name = project_name(project_root, args.software_name)

    for rel in DIRS:
        (project_root / rel).mkdir(parents=True, exist_ok=True)

    for dst_rel, src_rel in TEMPLATES.items():
        copy_template(src_rel, project_root / dst_rel, software_name, project_root, args.overwrite)

    memory = memory_file_path(project_root)
    if args.overwrite or not memory.exists():
        memory.write_text("\n".join(memory_base_lines(project_root, software_name)), encoding="utf-8")

    confirm_stage(project_root, "SR-00:entry-dispatch", "confirmed", "softcopy_engine.py 初始化项目目录和基础模板")
    ensure_memory_version(project_root, "初始化项目记忆并完成记忆版本节点")
    print(f"OK initialized: {project_root}")


def list_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    ignored = {".git", "node_modules", "dist", "build", ".next", "__pycache__"}
    result: list[Path] = []
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.is_file():
            result.append(path)
    return result


def has_any(files: list[Path], patterns: tuple[str, ...]) -> bool:
    lowered = [str(path).lower() for path in files]
    return any(any(pattern in item for pattern in patterns) for item in lowered)


def has_stage_confirmation(project_root: Path, stage: str) -> bool:
    path = project_root / "00_材料说明" / "sr_confirmations.json"
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return any(item.get("stage") == stage for item in data.get("confirmations", []))


def default_entry_dispatch(project_root: Path, source_root: Path | None = None) -> str:
    source = source_root or project_root
    files = list_files(source)
    has_existing_softcopy = has_any(files, ("软著", "著作权", "申请表", "源程序", "操作手册", "设计说明"))
    if has_existing_softcopy:
        return "默认入口分流：既有项目/已有软著材料审核整改"
    if files:
        return "默认入口分流：既有项目/资料补齐或生成"
    return "默认入口分流：新项目初始化"


def ensure_entry_dispatch(project_root: Path, source_root: Path | None = None) -> None:
    if has_stage_confirmation(project_root, "SR-00:entry-dispatch"):
        return
    confirm_stage(project_root, "SR-00:entry-dispatch", "confirmed", default_entry_dispatch(project_root, source_root))


def detect_material_status(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    source_root = Path(args.source_root).expanduser().resolve() if args.source_root else project_root
    ensure_entry_dispatch(project_root, source_root)
    files = list_files(source_root)

    has_source = has_any(files, (".py", ".java", ".js", ".ts", ".tsx", ".vue", ".cs", ".go", ".php", ".swift", ".kt"))
    has_screenshot = has_any(files, (".png", ".jpg", ".jpeg", ".webp"))
    has_docs = has_any(files, ("需求", "prd", "设计", "说明书", "手册", ".doc", ".docx", ".md", ".pdf"))
    has_api_or_db = has_any(files, ("swagger", "openapi", "接口", "数据库", ".sql", "schema"))
    has_existing_softcopy = has_any(files, ("软著", "著作权", "申请表", "源程序", "操作手册", "设计说明"))

    if has_existing_softcopy:
        branch = "E"
        completeness = "已有软著材料"
        route = "已有材料审核整改"
    elif has_docs and has_source and has_screenshot and has_api_or_db:
        branch = "A"
        completeness = "完整"
        route = "基于资料整理"
    elif has_source and not has_docs:
        branch = "C"
        completeness = "仅源码"
        route = "基于源码反推"
    elif has_docs or has_screenshot or has_api_or_db:
        branch = "B"
        completeness = "部分"
        route = "补齐缺口后生成"
    else:
        branch = "D"
        completeness = "仅业务描述或空目录"
        route = "暂停补料"

    out = project_root / "00_材料说明" / "资料状态识别报告.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "\n".join(
            [
                "# 资料状态识别报告",
                "",
                f"识别时间：{timestamp()}",
                f"项目路径：{project_root}",
                f"来源路径：{source_root}",
                "",
                "| 项 | 内容 |",
                "|---|---|",
                f"| 资料状态分支 | {branch} |",
                f"| 资料完整度 | {completeness} |",
                f"| 推荐软著路线 | {route} |",
                f"| 文件数量 | {len(files)} |",
                f"| 是否发现源码 | {'是' if has_source else '否'} |",
                f"| 是否发现截图 | {'是' if has_screenshot else '否'} |",
                f"| 是否发现文档 | {'是' if has_docs else '否'} |",
                f"| 是否发现接口/数据库资料 | {'是' if has_api_or_db else '否'} |",
                f"| 是否发现已有软著材料 | {'是' if has_existing_softcopy else '否'} |",
                "",
                "## 缺口提示",
                "",
                f"- 源码：{'已发现' if has_source else '缺失或未识别'}",
                f"- 截图：{'已发现' if has_screenshot else '缺失或未识别'}",
                f"- 项目文档：{'已发现' if has_docs else '缺失或未识别'}",
                f"- 接口/数据库资料：{'已发现' if has_api_or_db else '缺失或未识别'}",
                "",
                "## 下一步",
                "",
                "- 继续执行项目类型识别和材料策略规划。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    confirm_stage(project_root, "SR-01:material-status", "confirmed", f"自动生成资料状态识别报告：{branch}")
    ensure_memory_version(project_root, f"资料状态识别已写入项目记忆：{branch}")
    print(out)


def infer_project_type(source_root: Path) -> tuple[str, str]:
    files = list_files(source_root)
    names = " ".join(str(path).lower() for path in files)
    if any(key in names for key in ("androidmanifest.xml", "pubspec.yaml", ".swift", ".kt")):
        return "T5", "移动端应用"
    if any(key in names for key in (".csproj", ".xaml", "electron", "pyqt", "tkinter", "winforms", "wpf")):
        return "T2", "桌面软件"
    if any(key in names for key in ("serial", "usb", "device", "collector", "protocol", "采集", "设备", "校准")):
        return "T6", "嵌入式/设备配套软件"
    if any(key in names for key in ("analyzer", "predict", "score", "model", "report", "检测", "评分", "分析")):
        return "T3", "算法检测/分析软件"
    if any(key in names for key in ("cli", "batch", "script", "convert", "clean", "etl", "批处理", "转换")):
        return "T4", "工具/批处理软件"
    if any(key in names for key in ("swagger", "openapi", "controller", "service", "api", "sdk")) and not any(
        key in names for key in ("vue", "react", "vite", "router", "page")
    ):
        return "T7", "库/组件/API 服务"
    if any(key in names for key in ("package.json", "vite.config", "vue", "react", "router", "controller", "pom.xml")):
        return "T1", "Web 管理系统"
    return "待确认", "识别证据不足"


def read_project_type_report(project_root: Path) -> tuple[str, str] | None:
    report = project_root / "00_材料说明" / "项目类型识别报告.md"
    if not report.exists():
        return None
    text = report.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"\|\s*主类型\s*\|\s*([^|]+?)\s*\|", text)
    if not match:
        return None
    value = match.group(1).strip()
    parts = value.split(maxsplit=1)
    if not parts:
        return None
    return parts[0], parts[1] if len(parts) > 1 else ""


def project_type_payload(source_root: Path) -> dict[str, object]:
    files = list_files(source_root)
    names = " ".join(str(path).lower() for path in files)
    screenshot_names = " ".join(path.stem for path in files if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"})
    web_signals = [key for key in ("package.json", "vite.config", "vue", "react", "router", "controller", "service", "pom.xml") if key in names]
    api_signals = [key for key in ("controller", "resource", "service", "api", "swagger", "openapi") if key in names]
    ui_signals = [key for key in ("登录", "首页", "列表", "新增", "弹窗", "管理") if key in screenshot_names]
    analysis_tags = [key for key in ("分析", "血缘", "影响", "关联", "指标") if key in screenshot_names or key in names]

    if web_signals and ui_signals:
        main_type, type_name, confidence = "T1", "Web 管理系统", 95
    elif web_signals:
        main_type, type_name, confidence = "T1", "Web 管理系统", 88
    elif api_signals and not ui_signals:
        main_type, type_name, confidence = "T7", "库/组件/API 服务", 82
    else:
        inferred, inferred_name = infer_project_type(source_root)
        main_type, type_name, confidence = inferred, inferred_name, 70 if inferred != "待确认" else 50

    tags = []
    if analysis_tags:
        tags.append("数据分析")
    if api_signals:
        tags.append("接口服务")
    if ui_signals:
        tags.append("后台管理界面")
    if "导入" in screenshot_names or "导出" in screenshot_names:
        tags.append("导入导出")

    return {
        "main_type": main_type,
        "type_name": type_name,
        "confidence": confidence,
        "tags": tags or ["待确认"],
        "web_signals": web_signals,
        "api_signals": api_signals,
        "ui_signals": ui_signals,
        "analysis_tags": analysis_tags,
        "file_count": len(files),
    }


def identify_project_type(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    source_root = Path(args.source_root).expanduser().resolve() if args.source_root else project_root
    ensure_entry_dispatch(project_root, source_root)
    payload = project_type_payload(source_root)
    out = project_root / "00_材料说明" / "项目类型识别报告.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "\n".join(
            [
                "# 项目类型识别报告",
                "",
                f"识别时间：{timestamp()}",
                f"项目路径：{project_root}",
                f"来源路径：{source_root}",
                "",
                "| 字段 | 内容 |",
                "|---|---|",
                f"| 主类型 | {payload['main_type']} {payload['type_name']} |",
                f"| 置信度 | {payload['confidence']}% |",
                f"| 附加标签 | {'、'.join(payload['tags'])} |",
                f"| 文件数量 | {payload['file_count']} |",
                f"| Web 信号 | {'、'.join(payload['web_signals']) or '未识别'} |",
                f"| 接口信号 | {'、'.join(payload['api_signals']) or '未识别'} |",
                f"| UI 信号 | {'、'.join(payload['ui_signals']) or '未识别'} |",
                f"| 分析类信号 | {'、'.join(payload['analysis_tags']) or '未识别'} |",
                "",
                "## 材料策略建议",
                "",
                "- 交互形态：浏览器后台管理界面。",
                "- 截图策略：覆盖登录、首页、列表、新增、审核、详情、分析类页面及按钮结果。",
                "- 说明书策略：操作手册优先，设计说明补充模块结构、接口与数据流。",
                "- 源码策略：优先节选前端页面、后端 Controller/Resource/Service、数据管理与审核相关模块。",
                "",
                "## 风险提示",
                "",
                "- 若申请表的软件分类与本报告不同，需人工确认后再进入提交版。",
                "- 分析类功能仅作为附加标签，不覆盖主类型 Web 管理系统。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    confirm_stage(project_root, "SR-02:project-type", "confirmed", f"项目类型识别完成：{payload['main_type']} {payload['type_name']}")
    ensure_memory_version(project_root, f"项目类型识别已写入项目记忆：{payload['main_type']}")
    print(out)


def clean_module_name(path: Path) -> str:
    stem = re.sub(r"^\d+_", "", path.stem)
    stem = re.sub(r"_(用户操作手册|IMG\d+|正式截图|截图).*", "", stem)
    stem = re.sub(r"按钮|页面|列表|弹窗", lambda m: m.group(0), stem)
    return stem.strip("_") or path.stem


def build_function_facts(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    source_root = Path(args.source_root).expanduser().resolve() if args.source_root else project_root
    ensure_entry_dispatch(project_root, source_root)
    files = list_files(source_root)
    screenshot_files = [
        path for path in files
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and "node_modules" not in path.parts
    ]
    source_files = [
        path for path in files
        if path.suffix.lower() in {".java", ".js", ".ts", ".tsx", ".vue", ".py", ".sql"} and "node_modules" not in path.parts
    ]
    doc_files = [
        path for path in files
        if path.suffix.lower() in {".md", ".doc", ".docx", ".pdf"} and "node_modules" not in path.parts
    ]

    modules: dict[str, dict[str, object]] = {}
    for image in screenshot_files:
        name = clean_module_name(image)
        if name in {"README", "用户手册前80张联系表"}:
            continue
        item = modules.setdefault(name, {"screenshots": [], "sources": [], "docs": []})
        item["screenshots"].append(image)

    source_text = " ".join(path.stem.lower() for path in source_files)
    for name, item in modules.items():
        compact = re.sub(r"管理|列表|新增|审核|详情|分析|设置|导入|提交|同步", "", name).lower()
        matched_sources = [path for path in source_files if compact and compact in path.stem.lower()]
        if not matched_sources and source_files:
            matched_sources = source_files[:3]
        item["sources"] = matched_sources[:5]
        item["docs"] = doc_files[:3]

    out = project_root / "00_材料说明" / "功能事实表.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in sorted(modules):
        item = modules[name]
        screenshots = item["screenshots"]
        sources = item["sources"]
        docs = item["docs"]
        if screenshots and sources:
            level = "L2"
            risk = "可用"
        elif screenshots or sources or docs:
            level = "L3"
            risk = "可用"
        else:
            level = "L5"
            risk = "待确认"
        evidence_paths = []
        for path in list(screenshots)[:2] + list(sources)[:2] + list(docs)[:1]:
            try:
                evidence_paths.append(str(path.relative_to(project_root)))
            except ValueError:
                evidence_paths.append(str(path))
        rows.append(
            "| {name} | 系统提供{name}相关功能，可作为软著材料中的功能模块或操作步骤事实。 | {level} | {evidence} | 操作手册/设计说明/源码材料 | {risk} |".format(
                name=name,
                level=level,
                evidence="<br>".join(evidence_paths) or "待补证",
                risk=risk,
            )
        )

    if not rows:
        rows.append("| 待确认功能 | 当前资料不足以形成可入稿功能事实。 | L5 | 待补证 | 草案 | 待确认 |")

    out.write_text(
        "\n".join(
            [
                "# 功能事实表",
                "",
                f"生成时间：{timestamp()}",
                f"项目路径：{project_root}",
                f"来源路径：{source_root}",
                "",
                "| 功能/模块 | 事实描述 | 证据等级 | 证据路径 | 对应材料 | 风险状态 |",
                "|---|---|---|---|---|---|",
                *rows,
                "",
                "## 证据等级口径",
                "",
                "- L2：截图与源码/文档互相印证。",
                "- L3：单一资料可证明，入稿时需保留证据路径。",
                "- L5：需要人工补证或确认。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    confirm_stage(project_root, "SR-03:facts", "confirmed", f"功能事实表生成完成，功能条目数：{len(rows)}")
    ensure_memory_version(project_root, f"功能事实表已写入项目记忆，条目数：{len(rows)}")
    print(out)


APPLICATION_FIELD_ORDER = [
    "软件全称",
    "软件简称",
    "版本号",
    "著作权人",
    "开发完成日期",
    "首次发表日期",
    "开发方式",
    "权利取得方式",
    "权利范围",
    "开发硬件环境",
    "运行硬件环境",
    "开发操作系统",
    "运行平台/操作系统",
    "开发工具",
    "运行支撑环境",
    "软件分类",
    "软件作品说明",
    "源程序量",
    "开发目的",
    "面向领域/行业",
    "主要功能",
    "技术特点",
]


def parse_markdown_field_table(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith("|") or "---" in line or "填写项" in line:
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) >= 2 and parts[0]:
            fields[parts[0]] = parts[1]
    return fields


def infer_application_field_defaults(project_root: Path) -> dict[str, str]:
    app_md = project_root / "04_提交版" / "md" / "03_计算机软件著作权登记申请表.md"
    fields = parse_markdown_field_table(app_md)
    fields.setdefault("开发方式", fields.get("开发方式") or "独立开发")
    fields.setdefault("权利取得方式", fields.get("权利取得方式") or "原始取得")
    fields.setdefault("权利范围", fields.get("权利范围") or "全部权利")
    fields.setdefault("运行平台/操作系统", "浏览器/服务器操作系统待确认")
    fields.setdefault("开发工具", "IDE/代码编辑器待确认")
    fields.setdefault("运行支撑环境", "JDK、Web 浏览器、数据库/中间件待确认")
    return fields


def generate_application_fields(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    ensure_entry_dispatch(project_root, project_root)
    fields = infer_application_field_defaults(project_root)
    out = project_root / "01_申请表" / "申请表字段确认.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    missing = []
    for field in APPLICATION_FIELD_ORDER:
        value = fields.get(field, "").strip()
        if value:
            status = "已提取待复核"
            source = "提交版申请表/规则默认"
        else:
            value = "待确认"
            status = "待确认"
            source = "用户确认"
            missing.append(field)
        rows.append(f"| {field} | {value} | {source} | {status} |")

    out.write_text(
        "\n".join(
            [
                "# 申请表字段确认",
                "",
                f"生成时间：{timestamp()}",
                f"项目路径：{project_root}",
                f"来源申请表：04_提交版/md/03_计算机软件著作权登记申请表.md",
                "",
                "| 字段 | 建议值 | 来源 | 状态 |",
                "|---|---|---|---|",
                *rows,
                "",
                "## 缺失或需人工确认字段",
                "",
                *(f"- {field}" for field in missing),
                *(["- 未发现空缺字段；仍需人工复核主体、日期和环境字段。"] if not missing else []),
                "",
                "## 入稿边界",
                "",
                "- 本文件用于 SR-04 申请表字段节点，不等同于最终用户确认。",
                "- 标记为“待确认”的字段不得直接进入最终提交版。",
                "- 软件名称、版本、著作权人、日期、运行环境应在提交前由用户最终确认。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    status = "needs-fix" if missing else "confirmed"
    note = "申请表字段已提取，需人工复核" if missing else "申请表字段提取完成"
    confirm_stage(project_root, "SR-04:application-fields", status, f"{note}，待确认字段数：{len(missing)}")
    ensure_memory_version(project_root, f"申请表字段状态已写入项目记忆，待确认字段数：{len(missing)}")
    print(out)


def plan_materials(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    source_root = Path(args.source_root).expanduser().resolve() if args.source_root else project_root
    ensure_entry_dispatch(project_root, source_root)
    type_from_report = read_project_type_report(project_root)
    type_code, type_name = type_from_report or infer_project_type(source_root)
    out = project_root / "00_材料说明" / "材料策略报告.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    if type_code == "T7":
        manual = "弱化操作手册，设计说明优先"
        design = "接口设计、模块结构、调用流程、核心函数"
    elif type_code in {"T3", "T6"}:
        manual = "操作步骤与专业说明并重"
        design = "算法/设备流程、逻辑框图、运行设计"
    else:
        manual = "操作手册为主"
        design = "结构图、流程图、接口/模块映射补充"

    out.write_text(
        "\n".join(
            [
                "# 材料策略报告",
                "",
                f"生成时间：{timestamp()}",
                f"项目路径：{project_root}",
                f"来源路径：{source_root}",
                "",
                "| 项 | 内容 |",
                "|---|---|",
                f"| 项目类型 | {type_code} {type_name} |",
                f"| 项目类型来源 | {'项目类型识别报告' if type_from_report else '源码/资料自动初判'} |",
                f"| 操作手册策略 | {manual} |",
                f"| 设计说明策略 | {design} |",
                "| 截图策略 | 按 `templates/screenshot_index.md` 建立连续截图链 |",
                "| 图示策略 | 通过 `adapters/drawio_adapter.md` 生成 `.drawio + PNG/SVG` |",
                "| 质检策略 | 通过 `adapters/qc_adapter.md` 旁路检查 |",
                "",
                "## 后续动作",
                "",
                "1. 补齐项目类型识别报告。",
                "2. 补齐功能事实表。",
                "3. 根据截图链和图示计划生成材料。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    confirm_stage(project_root, "SR-05:material-architecture", "confirmed", f"自动生成材料策略报告：{type_code}")
    ensure_memory_version(project_root, f"材料策略已写入项目记忆：{type_code}")
    print(out)


def extract_templates(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    ensure_entry_dispatch(project_root, project_root)
    template_root = Path(args.template_root).expanduser().resolve() if args.template_root else DEFAULT_TEMPLATE_ROOT
    out_dir = project_root / "00_材料说明" / "软著模板"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    missing = []
    for template_id, filename, title in TEMPLATE_MANIFEST:
        src = template_root / filename
        dst = out_dir / filename
        if src.exists():
            if args.copy:
                shutil.copy2(src, dst)
                target = dst
            else:
                target = src
            rows.append((template_id, title, src, target, "已提取"))
        else:
            missing.append(filename)
            rows.append((template_id, title, src, "", "缺失"))

    report = project_root / "00_材料说明" / "软著模板提取报告.md"
    report.write_text(
        "\n".join(
            [
                "# 软著模板提取报告",
                "",
                f"提取时间：{timestamp()}",
                f"项目路径：{project_root}",
                f"模板来源：{template_root}",
                f"提取方式：{'复制到项目目录' if args.copy else '登记引用路径'}",
                "",
                "| 模板ID | 模板名称 | 来源路径 | 项目内路径/引用路径 | 状态 |",
                "|---|---|---|---|---|",
                *(
                    f"| {template_id} | {title} | {src} | {target} | {status} |"
                    for template_id, title, src, target, status in rows
                ),
                "",
                "## 使用边界",
                "",
                "- 模板用于字段、格式、章节和源码材料结构参考。",
                "- 模板不得覆盖当前项目正式提交稿。",
                "- 生成正式 Word/PDF 前，仍需按项目事实、截图链和源码材料重新填充。",
                "- 如模板缺失，必须先补齐模板再进入正式排版阶段。",
                "",
            ]
        ),
        encoding="utf-8",
    )

    status = "needs-fix" if missing else "confirmed"
    note = "软著模板提取完成" if not missing else "软著模板提取存在缺失：" + "、".join(missing)
    confirm_stage(project_root, "SR-04A:template-extraction", status, note)
    ensure_memory_version(project_root, f"模板提取状态已写入项目记忆：{status}")
    print(report)


def file_summary(path: Path) -> str:
    if not path.exists():
        return "缺失"
    size = path.stat().st_size
    return f"{size} bytes"


def generate_template_rules(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    ensure_entry_dispatch(project_root, project_root)
    template_root = Path(args.template_root).expanduser().resolve() if args.template_root else DEFAULT_TEMPLATE_ROOT
    engine_rule = ENGINE_ROOT / "rules" / "generated_template_rules.md"
    project_report = project_root / "00_材料说明" / "模板规则生成报告.md"
    project_report.parent.mkdir(parents=True, exist_ok=True)

    missing = []
    rows = []
    for template_id, filename, title in TEMPLATE_MANIFEST:
        src = template_root / filename
        if not src.exists():
            missing.append(filename)
        rows.append((template_id, title, src, file_summary(src)))

    lines = [
        "# 模板规则生成结果",
        "",
        f"生成时间：{timestamp()}",
        f"模板来源：{template_root}",
        "",
        "## 模板清单",
        "",
        "| 模板ID | 模板名称 | 文件路径 | 文件状态 |",
        "|---|---|---|---|",
        *(f"| {template_id} | {title} | {src} | {summary} |" for template_id, title, src, summary in rows),
        "",
        "## 生成规则",
        "",
        "| 模板ID | 规则名称 | 规则内容 | 应用节点 |",
        "|---|---|---|---|",
        *(f"| {template_id} | {name} | {rule} | {nodes} |" for template_id, name, rule, nodes in TEMPLATE_RULES),
        "",
        "## 全链路应用",
        "",
        "- SR-04 申请表字段：以申请表模板约束字段完整性和一致性。",
        "- SR-06/SR-07 文档生成：以软件说明书范本约束章节结构、截图说明和设计说明深度。",
        "- SR-08 源码选择：以源代码范本约束源码材料格式和页数/连续性。",
        "- SR-11 提交版：以三个模板共同约束 Word/PDF 输出结构。",
        "- SR-12 质检：模板规则进入旁路检查、质检角色和最终核对清单。",
        "",
    ]
    engine_rule.write_text("\n".join(lines), encoding="utf-8")
    project_report.write_text("\n".join(lines), encoding="utf-8")

    status = "needs-fix" if missing else "confirmed"
    note = "模板规则生成完成" if not missing else "模板规则生成存在缺失：" + "、".join(missing)
    confirm_stage(project_root, "SR-04B:template-rule-generation", status, note)
    ensure_memory_version(project_root, f"模板规则生成状态已写入项目记忆：{status}")
    print(project_report)


def check_sidecar(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    ensure_entry_dispatch(project_root, project_root)
    issues: list[str] = []
    target_dirs = [
        project_root / "01_申请表",
        project_root / "04_提交版" / "md",
    ]
    if args.include_material_notes:
        target_dirs.append(project_root / "00_材料说明")
    md_files = [path for folder in target_dirs for path in list_files(folder) if path.suffix.lower() == ".md"]
    placeholders = ("待填写", "待确认", "示例", "占位")
    image_re = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in placeholders:
            if marker in text:
                issues.append(f"[占位残留] {path}: 包含 `{marker}`")
        for match in image_re.findall(text):
            if match.startswith(("http://", "https://")):
                continue
            image_path = (path.parent / match).resolve()
            if not image_path.exists():
                issues.append(f"[图片缺失] {path}: {match}")
        if "```mermaid" in text.lower():
            issues.append(f"[图示风险] {path}: 包含 Mermaid 代码块")

    status = "confirmed" if not issues else "needs-fix"
    out = project_root / "05_质检" / "旁路检查报告.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "\n".join(
            [
                "# 旁路检查报告",
                "",
                f"检查时间：{timestamp()}",
                f"项目路径：{project_root}",
                "",
                f"检查范围：{'提交材料 + 材料说明' if args.include_material_notes else '提交材料'}",
                f"检查文件数：{len(md_files)}",
                f"问题数：{len(issues)}",
                "",
                "## 问题",
                "",
                *(f"- {issue}" for issue in issues),
                *(["- 未发现轻量规则问题。"] if not issues else []),
                "",
            ]
        ),
        encoding="utf-8",
    )
    confirm_stage(project_root, "SR-12:qc", status, f"旁路检查完成，问题数：{len(issues)}")
    ensure_memory_version(project_root, f"旁路检查结果已写入项目记忆，问题数：{len(issues)}")
    print(out)


def evaluate_switch(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    check_report = project_root / "05_质检" / "旁路检查报告.md"
    status_log = project_root / "00_材料说明" / "sr_confirmations.json"
    template_report = project_root / "00_材料说明" / "软著模板提取报告.md"
    out = project_root / "05_质检" / "engine生产切换评估.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    ran_real_validation = check_report.exists() and status_log.exists()
    issue_count = 999
    if check_report.exists():
        text = check_report.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"问题数：(\d+)", text)
        if match:
            issue_count = int(match.group(1))

    has_drawio = any((project_root / "03_截图").glob("drawio/*.drawio")) if (project_root / "03_截图").exists() else False
    has_pdf = bool(list((project_root / "04_提交版" / "pdf").glob("*.pdf"))) if (project_root / "04_提交版" / "pdf").exists() else False
    has_template_report = template_report.exists()

    if not ran_real_validation:
        level = "L0"
        conclusion = "不可切换：尚未完成真实项目旁路验证。"
    elif not has_template_report:
        level = "L1"
        conclusion = "可旁路辅助：尚未完成软著模板提取登记。"
    elif issue_count > 0:
        level = "L1"
        conclusion = "可旁路辅助：仍存在提交材料占位、缺图或轻量检查问题。"
    elif not has_drawio or not has_pdf:
        level = "L2"
        conclusion = "可生成草稿：轻量检查通过，但 drawio 或 PDF/DOCX 生产链路尚未完整验证。"
    else:
        level = "L3"
        conclusion = "可评估部分生产：仍需多项目稳定验证后再考虑默认切换。"

    out.write_text(
        "\n".join(
            [
                "# engine 生产切换评估",
                "",
                f"评估时间：{timestamp()}",
                f"项目路径：{project_root}",
                "",
                "| 项 | 结果 |",
                "|---|---|",
                f"| 真实项目旁路验证 | {'已完成' if ran_real_validation else '未完成'} |",
                f"| 旁路检查问题数 | {issue_count if issue_count != 999 else '未知'} |",
                f"| 软著模板提取报告 | {'已生成' if has_template_report else '未生成'} |",
                f"| 是否发现 drawio 源文件 | {'是' if has_drawio else '否'} |",
                f"| 是否发现 PDF 提交稿 | {'是' if has_pdf else '否'} |",
                f"| 建议切换等级 | {level} |",
                "",
                f"结论：{conclusion}",
                "",
                "## 建议",
                "",
                "- 旧 Skill 继续作为生产主入口。",
                "- engine 继续作为旁路检查和工程化底座。",
                "- 待提交材料占位和图链路问题关闭后，再评估 L2/L3。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(out)


def confirm_stage(project_root: Path, stage: str, status: str, note: str) -> None:
    script = ENGINE_ROOT / "scripts" / "confirm_softcopy_stage.py"
    cmd = [
        sys.executable,
        str(script),
        "--project-root",
        str(project_root),
        "--stage",
        stage,
        "--status",
        status,
        "--actor",
        "softcopy_engine.py",
        "--note",
        note,
    ]
    subprocess.run(cmd, check=True)


def confirm_command(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    confirm_stage(project_root, args.stage, args.status, args.note)


def sync_memory_command(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    memory = ensure_memory_version(project_root, args.note)
    print(memory)


def run_p1_command(args: argparse.Namespace) -> None:
    detect_material_status(args)
    identify_project_type(args)
    build_function_facts(args)


def run_p2_command(args: argparse.Namespace) -> None:
    generate_application_fields(args)
    plan_materials(args)


def count_files(root: Path, suffixes: set[str]) -> int:
    return sum(1 for path in list_files(root) if path.suffix.lower() in suffixes)


def write_p3_report(project_root: Path, node_id: str, title: str, status: str, note: str, evidence: list[Path], issues: list[str]) -> Path:
    out = project_root / "00_材料说明" / f"{node_id.replace(':', '_')}_{title}报告.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {title}报告",
        "",
        f"生成时间：{timestamp()}",
        f"项目路径：{project_root}",
        f"节点：{node_id}",
        f"状态：{status}",
        f"结论：{note}",
        "",
        "## 证据",
        "",
    ]
    if evidence:
        for path in evidence:
            try:
                display = path.relative_to(project_root)
            except ValueError:
                display = path
            lines.append(f"- {display}")
    else:
        lines.append("- 未发现可登记证据。")
    lines.extend(["", "## 缺口", ""])
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("- 未发现本节点轻量缺口。")
    out.write_text("\n".join(str(line) for line in lines) + "\n", encoding="utf-8")
    return out


def xml_escape(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg_text(
    label: str,
    x: int,
    y: int,
    width: int,
    line_height: int = 18,
    color: str = "#172033",
    font_size: int | None = None,
) -> str:
    lines = [line.strip() for line in label.split("\n") if line.strip()]
    if not lines:
        return ""
    if font_size is None:
        longest = max(len(line) for line in lines)
        font_size = max(10, min(14, int(width / max(1, longest) * 0.9)))
    line_height = max(line_height, font_size + 4)
    start_y = y - ((len(lines) - 1) * line_height // 2)
    return "\n".join(
        f'<text x="{x}" y="{start_y + index * line_height}" text-anchor="middle" '
        f'dominant-baseline="middle" '
        f'font-family="PingFang SC, Microsoft YaHei, Arial, sans-serif" font-size="{font_size}" '
        f'fill="{color}">{xml_escape(line)}</text>'
        for index, line in enumerate(lines)
    )


def diagram_specs(project_root: Path) -> list[dict[str, object]]:
    software_name = project_root.name.replace("PJ1-", "")
    return [
        {
            "slug": "PJ1_系统架构图",
            "title": f"{software_name}平台架构定位图",
            "diagram_type": "大数据平台基础架构裁剪图/组件图",
            "summary": "基于医药大数据平台总体架构进行裁剪，按平台能力区而非业务流程绘制，突出本系统在大数据治理中心中的主数据治理、元数据管理、审核流转和血缘分析边界。",
            "nodes": [
                {"id": "source_zone", "label": "", "shape": "zone", "x": 24, "y": 60, "w": 92, "h": 340, "fill": "#FFFFFF", "stroke": "#B8CBE8"},
                {"id": "platform_zone", "label": "", "shape": "zone", "x": 138, "y": 64, "w": 528, "h": 336, "fill": "#FFFFFF", "stroke": "#B8CBE8"},
                {"id": "app_zone", "label": "", "shape": "zone", "x": 684, "y": 61, "w": 92, "h": 340, "fill": "#FFFFFF", "stroke": "#B8CBE8"},
                {"id": "source_title", "label": "数据源", "shape": "component", "x": 29, "y": 80, "w": 72, "h": 28, "fill": "#0F6FB7", "stroke": "#0F6FB7", "font_size": 10, "font_color": "#FFFFFF"},
                {"id": "internal_source", "label": "", "shape": "component", "x": 35, "y": 120, "w": 60, "h": 88, "fill": "#F4F8FF", "stroke": "#4B7DBF"},
                {"id": "internal_title", "label": "内部数据源", "shape": "label", "x": 35, "y": 120, "w": 60, "h": 16, "fill": "#E8F2FF", "stroke": "#4B7DBF", "font_size": 8, "font_color": "#245B91"},
                {"id": "internal_biz", "label": "业务库", "shape": "component", "x": 42, "y": 144, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "internal_catalog", "label": "目录库", "shape": "component", "x": 42, "y": 167, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "internal_base", "label": "基础数据", "shape": "component", "x": 42, "y": 188, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "external_source", "label": "", "shape": "component", "x": 35, "y": 226, "w": 60, "h": 92, "fill": "#F4F8FF", "stroke": "#4B7DBF"},
                {"id": "external_title", "label": "外部数据源", "shape": "label", "x": 35, "y": 226, "w": 60, "h": 16, "fill": "#E8F2FF", "stroke": "#4B7DBF", "font_size": 8, "font_color": "#245B91"},
                {"id": "external_api", "label": "接口数据", "shape": "component", "x": 47, "y": 256, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "external_file", "label": "文件数据", "shape": "component", "x": 47, "y": 277, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "external_sync", "label": "同步数据", "shape": "component", "x": 47, "y": 298, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "input_label_top", "label": "输入", "shape": "arrow_label", "x": 98, "y": 165, "w": 56, "h": 22, "fill": "#5D6678", "stroke": "#5D6678", "font_size": 8, "font_color": "#FFFFFF"},
                {"id": "input_label_bottom", "label": "输入", "shape": "arrow_label", "x": 98, "y": 246, "w": 56, "h": 22, "fill": "#5D6678", "stroke": "#5D6678", "font_size": 8, "font_color": "#FFFFFF"},
                {"id": "platform_title", "label": "平台总体架构", "shape": "component", "x": 250, "y": 66, "w": 300, "h": 24, "fill": "#FFFFFF", "stroke": "#FFFFFF", "font_size": 15},
                {"id": "top_blue_band", "label": "", "shape": "component", "x": 155, "y": 91, "w": 505, "h": 28, "fill": "#0F6FB7", "stroke": "#0F6FB7"},
                {"id": "middle_purple_band", "label": "", "shape": "component", "x": 155, "y": 131, "w": 505, "h": 149, "fill": "#8B52B5", "stroke": "#6E3F99"},
                {"id": "ops_band", "label": "管控运维", "shape": "component", "x": 160, "y": 91, "w": 72, "h": 28, "fill": "#0F6FB7", "stroke": "#0F6FB7", "font_size": 10, "font_color": "#FFFFFF"},
                {"id": "capability_layer_title", "label": "数据能力层", "shape": "label", "x": 155, "y": 132, "w": 505, "h": 18, "fill": "#8B52B5", "stroke": "#8B52B5", "font_size": 10, "font_color": "#FFFFFF"},
                {"id": "meta_tab", "label": "基础数据管理", "shape": "component", "x": 232, "y": 94, "w": 78, "h": 22, "fill": "#E8F2FF", "stroke": "#4B7DBF", "font_size": 8},
                {"id": "std_tab", "label": "元数据管理", "shape": "component", "x": 314, "y": 94, "w": 70, "h": 22, "fill": "#E8F2FF", "stroke": "#4B7DBF", "font_size": 8},
                {"id": "quality_tab", "label": "标准管理", "shape": "component", "x": 388, "y": 94, "w": 64, "h": 22, "fill": "#E8F2FF", "stroke": "#4B7DBF", "font_size": 8},
                {"id": "security_tab", "label": "数据质量管理", "shape": "component", "x": 456, "y": 94, "w": 76, "h": 22, "fill": "#E8F2FF", "stroke": "#4B7DBF", "font_size": 8},
                {"id": "log_tab", "label": "数据安全管理", "shape": "component", "x": 536, "y": 94, "w": 76, "h": 22, "fill": "#E8F2FF", "stroke": "#4B7DBF", "font_size": 8},
                {"id": "access_module", "label": "", "shape": "component", "x": 160, "y": 154, "w": 94, "h": 120, "fill": "#8B52B5", "stroke": "#6E3F99"},
                {"id": "process_module", "label": "", "shape": "component", "x": 272, "y": 154, "w": 94, "h": 120, "fill": "#FFF6DA", "stroke": "#C29224"},
                {"id": "mdm_module", "label": "", "shape": "component", "x": 384, "y": 154, "w": 94, "h": 120, "fill": "#FDECEC", "stroke": "#C45D5D"},
                {"id": "service_module", "label": "", "shape": "component", "x": 496, "y": 154, "w": 94, "h": 120, "fill": "#8B52B5", "stroke": "#6E3F99"},
                {"id": "analysis_module", "label": "", "shape": "component", "x": 608, "y": 154, "w": 42, "h": 120, "fill": "#E8F2FF", "stroke": "#4B7DBF"},
                {"id": "access_title", "label": "数据接入", "shape": "label", "x": 160, "y": 156, "w": 94, "h": 24, "fill": "#6E3F99", "stroke": "#6E3F99", "font_size": 9, "font_color": "#FFFFFF"},
                {"id": "access_import", "label": "数据导入", "shape": "component", "x": 170, "y": 184, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 8},
                {"id": "access_api", "label": "接口采集", "shape": "component", "x": 170, "y": 207, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 8},
                {"id": "access_file", "label": "文件采集", "shape": "component", "x": 170, "y": 230, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 8},
                {"id": "access_table", "label": "库表采集", "shape": "component", "x": 170, "y": 253, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 8},
                {"id": "process_title", "label": "数据处理", "shape": "label", "x": 272, "y": 156, "w": 94, "h": 24, "fill": "#D8A92F", "stroke": "#C29224", "font_size": 9},
                {"id": "process_clean", "label": "数据清洗", "shape": "component", "x": 282, "y": 184, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#DAB85E", "font_size": 8},
                {"id": "process_std", "label": "标准转换", "shape": "component", "x": 282, "y": 207, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#DAB85E", "font_size": 8},
                {"id": "process_quality", "label": "质量校验", "shape": "component", "x": 282, "y": 230, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#DAB85E", "font_size": 8},
                {"id": "process_task", "label": "任务调度", "shape": "component", "x": 282, "y": 253, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#DAB85E", "font_size": 8},
                {"id": "mdm_title", "label": "大数据治理中心", "shape": "label", "x": 384, "y": 156, "w": 94, "h": 24, "fill": "#C45D5D", "stroke": "#C45D5D", "font_size": 9, "font_color": "#7A2E2E"},
                {"id": "mdm_master", "label": "主数据管理", "shape": "component", "x": 394, "y": 184, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#E2A6A6", "font_size": 8},
                {"id": "mdm_metadata", "label": "元数据管理", "shape": "component", "x": 394, "y": 207, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#E2A6A6", "font_size": 8},
                {"id": "mdm_index", "label": "指标维度", "shape": "component", "x": 394, "y": 230, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#E2A6A6", "font_size": 8},
                {"id": "mdm_lineage", "label": "影响/血缘", "shape": "component", "x": 394, "y": 253, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#E2A6A6", "font_size": 8},
                {"id": "service_title", "label": "数据服务", "shape": "label", "x": 496, "y": 156, "w": 94, "h": 24, "fill": "#6E3F99", "stroke": "#6E3F99", "font_size": 9, "font_color": "#FFFFFF"},
                {"id": "service_exchange", "label": "交换共享", "shape": "component", "x": 506, "y": 184, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 8},
                {"id": "service_catalog", "label": "服务目录", "shape": "component", "x": 506, "y": 207, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 8},
                {"id": "service_api", "label": "服务接口", "shape": "component", "x": 506, "y": 230, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 8},
                {"id": "service_auth", "label": "数据授权", "shape": "component", "x": 506, "y": 253, "w": 74, "h": 18, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 8},
                {"id": "analysis_title", "label": "分析", "shape": "label", "x": 614, "y": 162, "w": 30, "h": 18, "fill": "#4B7DBF", "stroke": "#4B7DBF", "font_size": 9, "font_color": "#245B91"},
                {"id": "analysis_asset", "label": "资产", "shape": "component", "x": 614, "y": 188, "w": 30, "h": 20, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 8},
                {"id": "analysis_stat", "label": "统计", "shape": "component", "x": 614, "y": 221, "w": 30, "h": 20, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 8},
                {"id": "analysis_viz", "label": "可视", "shape": "component", "x": 614, "y": 252, "w": 30, "h": 18, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 8},
                {"id": "data_band", "label": "", "shape": "component", "x": 155, "y": 292, "w": 505, "h": 28, "fill": "#8B52B5", "stroke": "#6E3F99"},
                {"id": "data_theme", "label": "数据主题", "shape": "label", "x": 160, "y": 298, "w": 68, "h": 16, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 9, "font_color": "#FFFFFF"},
                {"id": "data_table", "label": "库表管理", "shape": "component", "x": 300, "y": 298, "w": 68, "h": 16, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 7},
                {"id": "data_lineage", "label": "数据血缘", "shape": "component", "x": 380, "y": 298, "w": 68, "h": 16, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 7},
                {"id": "data_metric", "label": "指标维度", "shape": "component", "x": 460, "y": 298, "w": 68, "h": 16, "fill": "#FFFFFF", "stroke": "#C9B7DD", "font_size": 7},
                {"id": "app_title", "label": "数据应用", "shape": "component", "x": 694, "y": 80, "w": 72, "h": 28, "fill": "#0F6FB7", "stroke": "#0F6FB7", "font_size": 10, "font_color": "#FFFFFF"},
                {"id": "apps", "label": "", "shape": "component", "x": 700, "y": 127, "w": 60, "h": 166, "fill": "#F4F8FF", "stroke": "#4B7DBF", "font_size": 8},
                {"id": "app_biz", "label": "业务应用", "shape": "component", "x": 707, "y": 146.5, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "app_policy", "label": "政策关联", "shape": "component", "x": 707, "y": 169, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "app_industry", "label": "行业监管", "shape": "component", "x": 707, "y": 191.5, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "app_price", "label": "产品价格", "shape": "component", "x": 707, "y": 214.5, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "app_trade", "label": "交易分析", "shape": "component", "x": 707, "y": 237.5, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "app_report", "label": "统计报表", "shape": "component", "x": 707, "y": 258.5, "w": 46, "h": 15, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 7},
                {"id": "output_label", "label": "输出", "shape": "arrow_label", "x": 660, "y": 211, "w": 47, "h": 20, "fill": "#5D6678", "stroke": "#5D6678", "font_size": 8, "font_color": "#FFFFFF"},
                {"id": "support_arrow", "label": "", "shape": "bar_arrow", "x": 155, "y": 330, "w": 505, "h": 60, "fill": "#0F6FB7", "stroke": "#0F6FB7", "font_size": 10, "font_color": "#FFFFFF"},
                {"id": "support_base", "label": "统一支撑", "shape": "label", "x": 160, "y": 346, "w": 94, "h": 28, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 9, "font_color": "#FFFFFF"},
                {"id": "support_govern", "label": "统一治理", "shape": "component", "x": 300, "y": 352, "w": 68, "h": 16, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 8},
                {"id": "support_auth", "label": "统一权限", "shape": "component", "x": 380, "y": 352, "w": 68, "h": 16, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 8},
                {"id": "support_security", "label": "统一安全", "shape": "component", "x": 460, "y": 352, "w": 68, "h": 16, "fill": "#FFFFFF", "stroke": "#9DB9DC", "font_size": 8},
            ],
            "edges": [],
        },
        {
            "slug": "PJ1_主数据管理流程图",
            "title": f"{software_name}主数据管理流程图",
            "diagram_type": "UML 活动图",
            "summary": "按 UML 活动图风格体现主数据库表、主数据内容、模板与审核的核心业务流程。",
            "nodes": [
                {"id": "uml_start", "label": "", "shape": "uml_start", "x": 50, "y": 144, "w": 28, "h": 28, "fill": "#172033", "stroke": "#172033"},
                {"id": "login", "label": "登录系统\n进入首页", "shape": "activity", "x": 105, "y": 125, "w": 120, "h": 64, "fill": "#E8F2FF", "stroke": "#4B7DBF"},
                {"id": "table", "label": "主数据库表管理\n新增/配置/保存", "shape": "activity", "x": 270, "y": 125, "w": 150, "h": 64, "fill": "#EAF7EE", "stroke": "#4E9B61"},
                {"id": "sync", "label": "同步元数据\n生成字段结构", "shape": "activity", "x": 465, "y": 125, "w": 145, "h": 64, "fill": "#FFF6DA", "stroke": "#C29224"},
                {"id": "table_decision", "label": "库表\n审核通过?", "shape": "decision", "x": 655, "y": 112, "w": 95, "h": 95, "fill": "#FFEDED", "stroke": "#C45D5D"},
                {"id": "template", "label": "模板管理\n字段展示设置", "shape": "activity", "x": 270, "y": 285, "w": 150, "h": 64, "fill": "#F3ECFF", "stroke": "#8364B5"},
                {"id": "content", "label": "主数据内容管理\n新增/导入/提交", "shape": "activity", "x": 465, "y": 285, "w": 145, "h": 64, "fill": "#F4F7FB", "stroke": "#7A8798"},
                {"id": "content_decision", "label": "内容\n审核通过?", "shape": "decision", "x": 655, "y": 270, "w": 95, "h": 95, "fill": "#EAF7EE", "stroke": "#4E9B61"},
                {"id": "uml_end", "label": "", "shape": "uml_end", "x": 770, "y": 304, "w": 30, "h": 30, "fill": "#172033", "stroke": "#172033"},
            ],
            "edges": [
                ("uml_start", "login", ""),
                ("login", "table", "进入模块"),
                ("table", "sync", "同步"),
                ("sync", "table_decision", "提交"),
                ("table_decision", "template", "[通过]"),
                ("template", "content", "套用模板"),
                ("content", "content_decision", "提交审核"),
                ("content_decision", "uml_end", "[通过]"),
            ],
        },
        {
            "slug": "PJ1_数据血缘分析流程图",
            "title": f"{software_name}数据血缘分析流程图",
            "diagram_type": "数据流向图",
            "summary": "体现元数据、关联分析、影响分析和血缘分析的逻辑链路。",
            "nodes": [
                {"id": "metadata", "label": "元数据对象\n表/字段/关系", "shape": "data", "x": 75, "y": 100, "w": 145, "h": 68, "fill": "#E8F2FF", "stroke": "#4B7DBF"},
                {"id": "relation", "label": "关联分析\n对象关系识别", "shape": "activity", "x": 310, "y": 100, "w": 150, "h": 68, "fill": "#EAF7EE", "stroke": "#4E9B61"},
                {"id": "impact", "label": "影响分析\n下游影响范围", "shape": "activity", "x": 545, "y": 100, "w": 150, "h": 68, "fill": "#FFF6DA", "stroke": "#C29224"},
                {"id": "lineage", "label": "血缘分析\n上下游链路", "shape": "activity", "x": 300, "y": 285, "w": 150, "h": 68, "fill": "#FFEDED", "stroke": "#C45D5D"},
                {"id": "report", "label": "分析结果\n展示/决策辅助", "shape": "data", "x": 585, "y": 285, "w": 150, "h": 68, "fill": "#F3ECFF", "stroke": "#8364B5"},
            ],
            "edges": [
                ("metadata", "relation", "选择对象"),
                ("relation", "impact", "推导影响"),
                ("relation", "lineage", "追踪血缘"),
                ("impact", "report", "输出范围"),
                ("lineage", "report", "输出链路"),
            ],
        },
    ]


def render_drawio(spec: dict[str, object]) -> str:
    nodes = {node["id"]: node for node in spec["nodes"]}  # type: ignore[index]
    cells = [
        '<mxCell id="0"/>',
        '<mxCell id="1" parent="0"/>',
        '<mxCell id="canvas_background" value="" '
        'style="rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFFFF;strokeColor=#D7DCE5;" '
        'vertex="1" parent="1"><mxGeometry x="0" y="0" width="800" height="450" as="geometry"/></mxCell>',
        f'<mxCell id="diagram_title" value="{xml_escape(spec["title"])}" '
        'style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;'
        'fontColor=#172033;fontFamily=PingFang SC;fontSize=24;fontStyle=1;" '
        'vertex="1" parent="1"><mxGeometry x="34" y="20" width="560" height="34" as="geometry"/></mxCell>',
    ]
    for node in spec["nodes"]:  # type: ignore[index]
        label = xml_escape(str(node["label"]).replace("\n", "<br>"))
        shape = str(node.get("shape", "activity"))
        font_size = int(node.get("font_size", 14))
        font_color = str(node.get("font_color", "#172033"))
        if shape == "zone":
            style = (
                "rounded=1;whiteSpace=wrap;html=1;arcSize=4;dashed=1;"
                f"fillColor={node['fill']};strokeColor={node['stroke']};fontColor={font_color};"
                f"fontFamily=PingFang SC;fontSize={font_size};"
            )
        elif shape == "label":
            style = (
                "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;"
                f"fontColor={font_color};fontFamily=PingFang SC;fontSize={font_size};"
            )
        elif shape == "bar_arrow":
            style = (
                "shape=singleArrow;whiteSpace=wrap;html=1;arrowWidth=0.28;arrowSize=0.12;"
                f"fillColor={node['fill']};strokeColor={node['stroke']};fontColor={font_color};"
                f"fontFamily=PingFang SC;fontSize={font_size};fontStyle=1;"
            )
        elif shape == "arrow_label":
            style = (
                "shape=singleArrow;whiteSpace=wrap;html=1;arrowWidth=0.36;arrowSize=0.24;"
                f"fillColor={node['fill']};strokeColor={node['stroke']};fontColor={font_color};"
                f"fontFamily=PingFang SC;fontSize={font_size};fontStyle=1;"
            )
        elif shape == "decision":
            style = (
                "rhombus;whiteSpace=wrap;html=1;"
                f"fillColor={node['fill']};strokeColor={node['stroke']};fontColor={font_color};"
                f"fontFamily=PingFang SC;fontSize={font_size if 'font_size' in node else 13};"
            )
        elif shape in {"uml_start", "uml_end"}:
            style = (
                "ellipse;whiteSpace=wrap;html=1;"
                f"fillColor={node['fill']};strokeColor={node['stroke']};fontColor={font_color};"
                f"fontFamily=PingFang SC;fontSize={font_size if 'font_size' in node else 12};"
            )
        elif shape == "database":
            style = (
                "shape=cylinder3d;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;"
                f"fillColor={node['fill']};strokeColor={node['stroke']};fontColor={font_color};"
                f"fontFamily=PingFang SC;fontSize={font_size};"
            )
        elif shape == "data":
            style = (
                "shape=parallelogram;whiteSpace=wrap;html=1;fixedSize=1;"
                f"fillColor={node['fill']};strokeColor={node['stroke']};fontColor={font_color};"
                f"fontFamily=PingFang SC;fontSize={font_size};"
            )
        else:
            style = (
                "rounded=1;whiteSpace=wrap;html=1;arcSize=10;"
                f"fillColor={node['fill']};strokeColor={node['stroke']};fontColor={font_color};"
                f"fontFamily=PingFang SC;fontSize={font_size};"
            )
        cells.append(
            f'<mxCell id="{xml_escape(node["id"])}" value="{label}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{node["x"]}" y="{node["y"]}" width="{node["w"]}" height="{node["h"]}" as="geometry"/>'
            "</mxCell>"
        )
    for index, (source, target, label) in enumerate(spec["edges"], start=1):  # type: ignore[index]
        cells.append(
            f'<mxCell id="edge{index}" value="{xml_escape(label)}" '
            'style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;'
            'html=1;endArrow=block;endFill=1;strokeColor=#5D6678;fontSize=12;fontColor=#5D6678;" '
            f'edge="1" parent="1" source="{xml_escape(source)}" target="{xml_escape(target)}">'
            '<mxGeometry relative="1" as="geometry"/>'
            "</mxCell>"
        )
    return (
        '<mxfile host="app.diagrams.net" agent="softcopy-materials-engine" version="24.7.17">'
        f'<diagram id="{xml_escape(spec["slug"])}" name="{xml_escape(spec["title"])}">'
        '<mxGraphModel dx="960" dy="720" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
        'arrows="1" fold="1" page="1" pageScale="1" pageWidth="800" pageHeight="450" math="0" shadow="0">'
        f'<root>{"".join(cells)}</root>'
        "</mxGraphModel>"
        "</diagram>"
        "</mxfile>\n"
    )


def arrow_polygon(x: int, y: int, prev_x: int, prev_y: int) -> str:
    size = 9
    if abs(x - prev_x) >= abs(y - prev_y):
        if x >= prev_x:
            points = [(x, y), (x - size, y - 5), (x - size, y + 5)]
        else:
            points = [(x, y), (x + size, y - 5), (x + size, y + 5)]
    else:
        if y >= prev_y:
            points = [(x, y), (x - 5, y - size), (x + 5, y - size)]
        else:
            points = [(x, y), (x - 5, y + size), (x + 5, y + size)]
    return '<polygon points="{}" fill="#5D6678"/>'.format(" ".join(f"{px},{py}" for px, py in points))


def node_anchor(node: dict[str, object], side: str) -> tuple[int, int]:
    x = int(node["x"])
    y = int(node["y"])
    w = int(node["w"])
    h = int(node["h"])
    cx = x + w // 2
    cy = y + h // 2
    shape = str(node.get("shape", "activity"))
    if shape == "decision":
        if side == "left":
            return x, cy
        if side == "right":
            return x + w, cy
        if side == "top":
            return cx, y
        return cx, y + h
    if side == "left":
        return x, cy
    if side == "right":
        return x + w, cy
    if side == "top":
        return cx, y
    return cx, y + h


def simplify_route(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    simplified: list[tuple[int, int]] = []
    for point in points:
        if not simplified or simplified[-1] != point:
            simplified.append(point)

    changed = True
    while changed and len(simplified) >= 3:
        changed = False
        merged: list[tuple[int, int]] = [simplified[0]]
        for index in range(1, len(simplified) - 1):
            prev = merged[-1]
            current = simplified[index]
            nxt = simplified[index + 1]
            if (prev[0] == current[0] == nxt[0]) or (prev[1] == current[1] == nxt[1]):
                changed = True
                continue
            merged.append(current)
        merged.append(simplified[-1])
        simplified = merged
    return simplified


def edge_route(src: dict[str, object], dst: dict[str, object]) -> list[tuple[int, int]]:
    sx = int(src["x"])
    sy = int(src["y"])
    sw = int(src["w"])
    sh = int(src["h"])
    tx = int(dst["x"])
    ty = int(dst["y"])
    tw = int(dst["w"])
    th = int(dst["h"])
    src_cx = sx + sw // 2
    src_cy = sy + sh // 2
    dst_cx = tx + tw // 2
    dst_cy = ty + th // 2

    if tx >= sx + sw:
        start = node_anchor(src, "right")
        end = node_anchor(dst, "left")
        mid_x = (start[0] + end[0]) // 2
        return simplify_route([start, (mid_x, start[1]), (mid_x, end[1]), end])
    if sx >= tx + tw:
        start = node_anchor(src, "left")
        end = node_anchor(dst, "right")
        mid_x = (start[0] + end[0]) // 2
        return simplify_route([start, (mid_x, start[1]), (mid_x, end[1]), end])
    if ty >= sy + sh:
        start = node_anchor(src, "bottom")
        end = node_anchor(dst, "top")
        mid_y = (start[1] + end[1]) // 2
        return simplify_route([start, (start[0], mid_y), (end[0], mid_y), end])
    start = node_anchor(src, "top")
    end = node_anchor(dst, "bottom")
    mid_y = (start[1] + end[1]) // 2
    return simplify_route([start, (start[0], mid_y), (end[0], mid_y), end])


def edge_label_font_size(label: object, segment_length: int) -> int:
    text = str(label).strip()
    if not text:
        return 9
    available = max(36, segment_length - 26)
    estimated = int(available / max(1, len(text) * 0.9))
    return max(8, min(10, estimated))


def edge_label_segment_length(route: list[tuple[int, int]]) -> int:
    longest_segment = max(zip(route, route[1:]), key=lambda pair: abs(pair[1][0] - pair[0][0]) + abs(pair[1][1] - pair[0][1]))
    (lx1, ly1), (lx2, ly2) = longest_segment
    return abs(lx2 - lx1) + abs(ly2 - ly1)


def edge_label_position(route: list[tuple[int, int]], label: object, font_size: int) -> tuple[int, int]:
    longest_segment = max(zip(route, route[1:]), key=lambda pair: abs(pair[1][0] - pair[0][0]) + abs(pair[1][1] - pair[0][1]))
    (lx1, ly1), (lx2, ly2) = longest_segment
    if ly1 == ly2:
        return (lx1 + lx2) // 2, ly1 - 4
    if lx1 == lx2:
        return lx1 + 6, (ly1 + ly2) // 2 + max(3, font_size // 3)
    return (lx1 + lx2) // 2, (ly1 + ly2) // 2 - 4


def render_svg(spec: dict[str, object]) -> str:
    nodes = {str(node["id"]): node for node in spec["nodes"]}  # type: ignore[index]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 800 450">',
        '<rect x="0" y="0" width="800" height="450" rx="18" fill="#FFFFFF" stroke="#D7DCE5"/>',
        f'<text x="34" y="42" font-family="PingFang SC, Microsoft YaHei, Arial, sans-serif" '
        f'font-size="24" fill="#172033">{xml_escape(spec["title"])}</text>',
    ]
    for node in spec["nodes"]:  # type: ignore[index]
        if str(node.get("shape", "")) != "zone":
            continue
        x = int(node["x"])
        y = int(node["y"])
        w = int(node["w"])
        h = int(node["h"])
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
            f'fill="{node["fill"]}" stroke="{node["stroke"]}" stroke-width="1.6" stroke-dasharray="5 5"/>'
        )
    arrows: list[str] = []
    labels: list[str] = []
    for index, (source, target, label) in enumerate(spec["edges"], start=1):  # type: ignore[index]
        src = nodes[str(source)]
        dst = nodes[str(target)]
        route = edge_route(src, dst)
        path = " ".join(("M" if point_index == 0 else "L") + f"{x},{y}" for point_index, (x, y) in enumerate(route))
        parts.append(f'<path d="{path}" fill="none" stroke="#5D6678" stroke-width="2"/>')
        prev_x, prev_y = route[-2]
        end_x, end_y = route[-1]
        arrows.append(arrow_polygon(end_x, end_y, prev_x, prev_y))
        font_size = edge_label_font_size(label, edge_label_segment_length(route))
        label_x, label_y = edge_label_position(route, label, font_size)
        labels.append(
            f'<text x="{label_x}" y="{label_y}" text-anchor="middle" '
            f'font-family="PingFang SC, Microsoft YaHei, Arial, sans-serif" font-size="{font_size}" font-weight="400" '
            f'fill="#667085">{xml_escape(label)}</text>'
        )
    for node in spec["nodes"]:  # type: ignore[index]
        if str(node.get("shape", "")) == "zone":
            continue
        x = int(node["x"])
        y = int(node["y"])
        w = int(node["w"])
        h = int(node["h"])
        shape = str(node.get("shape", "activity"))
        font_size = int(node.get("font_size", 14))
        font_color = str(node.get("font_color", "#172033"))
        if shape == "uml_start":
            parts.append(f'<circle cx="{x + w // 2}" cy="{y + h // 2}" r="{min(w, h) // 2}" fill="#172033" stroke="#172033"/>')
        elif shape == "uml_end":
            cx = x + w // 2
            cy = y + h // 2
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{min(w, h) // 2}" fill="#FFFFFF" stroke="#172033" stroke-width="2"/>')
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{max(4, min(w, h) // 2 - 6)}" fill="#172033" stroke="#172033"/>')
        elif shape == "decision":
            points = f"{x + w // 2},{y} {x + w},{y + h // 2} {x + w // 2},{y + h} {x},{y + h // 2}"
            parts.append(f'<polygon points="{points}" fill="{node["fill"]}" stroke="{node["stroke"]}" stroke-width="2"/>')
            parts.append(svg_text(str(node["label"]), x + w // 2, y + h // 2, w, line_height=16, color=font_color, font_size=font_size))
        elif shape == "database":
            rx = 12
            top_h = 16
            parts.append(f'<path d="M{x},{y + top_h} C{x},{y - 2} {x + w},{y - 2} {x + w},{y + top_h} L{x + w},{y + h - top_h} C{x + w},{y + h + 2} {x},{y + h + 2} {x},{y + h - top_h} Z" fill="{node["fill"]}" stroke="{node["stroke"]}" stroke-width="2"/>')
            parts.append(f'<path d="M{x},{y + top_h} C{x},{y + top_h * 2} {x + w},{y + top_h * 2} {x + w},{y + top_h}" fill="none" stroke="{node["stroke"]}" stroke-width="2"/>')
            parts.append(svg_text(str(node["label"]), x + w // 2, y + h // 2 + 8, w, color=font_color, font_size=font_size))
        elif shape == "data":
            skew = 18
            points = f"{x + skew},{y} {x + w},{y} {x + w - skew},{y + h} {x},{y + h}"
            parts.append(f'<polygon points="{points}" fill="{node["fill"]}" stroke="{node["stroke"]}" stroke-width="2"/>')
            parts.append(svg_text(str(node["label"]), x + w // 2, y + h // 2, w, color=font_color, font_size=font_size))
        elif shape == "bar_arrow":
            points = f"{x},{y} {x + w - 18},{y} {x + w},{y + h // 2} {x + w - 18},{y + h} {x},{y + h} {x + 12},{y + h // 2}"
            parts.append(f'<polygon points="{points}" fill="{node["fill"]}" stroke="{node["stroke"]}" stroke-width="2"/>')
            parts.append(svg_text(str(node["label"]), x + w // 2, y + h // 2 + 3, w, line_height=14, color=font_color, font_size=font_size))
        elif shape == "arrow_label":
            notch = min(8, max(4, h // 3))
            head = min(14, max(8, w // 4))
            points = (
                f"{x},{y} {x + w - head},{y} {x + w},{y + h // 2} "
                f"{x + w - head},{y + h} {x},{y + h} {x + notch},{y + h // 2}"
            )
            parts.append(f'<polygon points="{points}" fill="{node["fill"]}" stroke="{node["stroke"]}" stroke-width="1.5"/>')
            parts.append(svg_text(str(node["label"]), x + w // 2 - 2, y + h // 2, w, line_height=12, color=font_color, font_size=font_size))
        elif shape == "label":
            parts.append(svg_text(str(node["label"]), x + w // 2, y + h // 2, w, line_height=14, color=font_color, font_size=font_size))
        else:
            parts.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
                f'fill="{node["fill"]}" stroke="{node["stroke"]}" stroke-width="2"/>'
            )
            parts.append(svg_text(str(node["label"]), x + w // 2, y + h // 2, w, color=font_color, font_size=font_size))
    parts.extend(arrows)
    parts.extend(labels)
    parts.append("</svg>\n")
    return "\n".join(parts)


def write_sr10_visual_review(project_root: Path) -> Path:
    out = project_root / "05_质检" / "SR-10_图示美工审查意见.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SR-10 图示美工审查意见",
        "",
        f"审查时间：{timestamp()}",
        f"项目路径：{project_root}",
        "审查对象：SR-10 正式图示 PNG/SVG/drawio。",
        "",
        "## 审查结论",
        "",
        "- 原问题：连线文字偏离线条，像悬浮标签；短线上的文字过大时容易挤压节点或覆盖箭头。",
        "- 原问题：系统架构图曾按通用 Web 分层重新抽象，未充分承接项目已有医药大数据平台总体架构。",
        "- 美工建议：系统架构图应优先复用项目已有平台基础架构语言，在平台分层中高亮本软件边界，避免与项目材料口径割裂。",
        "- 美工建议：系统架构图不是流程图，平台内部模块应按能力区并列呈现，内部不使用步骤式连续箭头。",
        "- 美工建议：连线文字应放在承载线段中心附近的空白侧，不压在线条上，不使用底色块，不做胶囊化处理。",
        "- 美工建议：字号根据线段长度自动适配，短线降字号，长线保持正常字号。",
        "- 美工建议：箭头、节点、连线文字的视觉层级应保持稳定，线标应小一些、细一些，不加粗，清晰但不抢过节点标题。",
        "- 本轮审查：数据主题、统一支撑、数据接入、数据处理、大数据治理中心、数据服务、分析已按层/模块标题处理，不再额外加小框，符合平台总体架构图的标题层级。",
        "- 本轮审查：输入/输出已改为箭头标签，表达上下游流向，比普通文字更直观。",
        "- 本轮审查：输出箭头原位置略压住分析能力区边界，已收窄并移动到分析区与数据应用区之间的通道，减少遮挡。",
        "- 本轮审查：管控运维从独立组件框改为无框标签，避免顶栏内出现边框色不一致的问题。",
        "- 本轮审查：分析标题从浅底白字改为深蓝字，增强与浅蓝背景的区分度。",
        "- 本轮审查：内部数据源、外部数据源从小组件框改为无框分组标题，具体数据项仍保留框，层级更清楚。",
        "- 本轮审查：输出箭头调整为指向右侧数据应用下的具体应用模块，而不是只停在数据应用外框边界。",
        "- 本轮审查：数据主题带、统一支撑带宽度调整为与顶部管控运维带一致，形成统一的平台横向层次。",
        "- 本轮审查：中间能力区补充数据能力层标题，使数据接入、数据处理、治理中心、数据服务、分析的上层归属更明确。",
        "- 本轮审查：输出箭头起点调整到数据能力层右边界，表达数据能力层整体输出到数据应用，避免误读为分析模块单独输出。",
        "- 本轮审查：数据源、管控运维、数据应用统一为一级蓝色标签，尺寸、字号、背景色保持一致；数据能力层作为能力区层名使用无框文字。",
        "- 本轮审查：按层级统一字号，一级层名 10px，二级模块/分组标题 9px，功能项 8px，边栏小项 7px。",
        "- 本轮审查：按层级区分背景色，一级平台层使用蓝色，能力域使用紫/黄/红/浅蓝，具体功能项使用白底小框。",
        "- 本轮审查：管控运维所在顶层蓝色横带取消异色描边，避免一级层名出现不必要的边框干扰。",
        "",
        "## 整改规则",
        "",
        "- 图类型规则：业务流程图按 UML 活动图风格绘制，系统架构图按分层/组件图绘制，数据血缘图按数据流向图绘制。",
        "- 架构图取材规则：若项目已有平台总体架构、基础架构或系统部署说明，必须以该架构为底稿进行裁剪和高亮，不另起一套泛化架构。",
        "- 架构图布局规则：平台架构图应采用左侧数据源、中间平台能力区、右侧数据应用、底部统一支撑的总体布局；箭头只表达外部输入输出或关键依赖，不表达业务步骤。",
        "- 软件边界规则：架构图必须在平台基础架构中标出申报软件承担的核心职责、上下游输入输出和依托的统一支撑能力。",
        "- UML 活动图：必须包含初始节点、活动节点、判断节点和终止节点；判断条件使用 `[通过]` 等条件标注。",
        "- 线标位置：取正交路由中最长线段的几何中心附近空白处，使用不重叠的最小安全距离；水平线贴近线上方，垂直线贴近线右侧。",
        "- 线标背景：透明，不绘制额外矩形或填充底色。",
        "- 线标字号：按线段长度动态计算，范围控制在 8px-10px。",
        "- 线标字重：使用常规字重，不加粗。",
        "- 线标关系：文字与线条保持约 4px-6px 的最小避让距离，使文字明确属于该条连线。",
        "- 标题处理：平台能力区标题、数据源分组标题使用无框标签；只有具体功能项使用小框，避免标题和功能项视觉层级混淆。",
        "- 色彩处理：同一色带内的标题不额外画边框；浅色能力区标题应使用深色文字，避免白字低对比。",
        "- 输入输出处理：输入/输出使用短箭头标签，放在外部数据源与平台、平台与数据应用之间，不压住功能块正文。",
        "- 层宽处理：顶部管控运维、中部数据主题、底部统一支撑三条横向能力带应保持同一左边界和右边界。",
        "- 层名处理：并列模块组上方必须有清晰层名，避免只看到模块而看不到上层归属。",
        "- 输出归属：右侧输出箭头应从数据能力层整体边界发出，不能从某一个末级模块内部发出。",
        "- 字号层级：同一层级的文字字号必须一致，不允许同为一级层名却出现 8px、10px、11px 混用。",
        "- 背景层级：背景色用于表达层级和能力域，不用于随意装饰；一级层名统一蓝底白字，功能项统一白底描边。",
        "- 一级层边框：一级蓝色层名和横带不使用异色描边；需要边界时使用同色描边或无感边界。",
        "",
        "## 验收口径",
        "",
        "- PNG 中每条线均可看见箭头。",
        "- 线标文字位于对应线段附近空白处，不游离到远离连线的位置。",
        "- 线标不出现明显压住节点正文、箭头或其他线标的情况。",
        "- SVG 与 PNG 视觉结果一致。",
        "- 系统架构图能看出本软件处于医药大数据平台治理中心/主数据治理位置，并能看出其与数据源、数据处理、数据服务、数据应用和统一支撑能力的关系。",
        "- 平台能力区标题不应被误读为功能按钮；具体功能项应保持框选、居中、可读。",
        "- 输入/输出箭头不应覆盖源数据、分析能力和数据应用的文字。",
        "- 输出箭头应指向数据应用下的应用模块区，不能只指向数据应用外框。",
        "- 管控运维、数据主题、统一支撑三条横向层应视觉等宽、对齐。",
        "- 输出箭头起点应与数据能力层右边界对齐，语义上表示平台能力层输出。",
        "- 数据源、管控运维、数据应用三个入口/分区标题应同色、同高、同宽、同字号；数据能力层作为中间能力区层名，不额外加框。",
        "- 不同层级应通过字号和背景色能一眼区分，同层级应保持视觉一致。",
        "- 管控运维层级不应出现紫色或其他异色边框。",
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def write_diagram_generation_note(project_root: Path, specs: list[dict[str, object]]) -> Path:
    out = project_root / "00_材料说明" / "SR-10_NextAIDrawIO图示生成说明.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# SR-10 NextAIDrawIO 图示生成说明",
        "",
        f"生成时间：{timestamp()}",
        f"项目路径：{project_root}",
        "图示链路：布局计划 -> .drawio 源文件 -> SVG -> PNG。",
        "一致性口径：以 .drawio 为唯一图源，优先调用 engine 缓存内的后台 draw.io 副本导出 SVG/PNG；只有本地 draw.io 不可用时才降级为内置 SVG/PNG 渲染。",
        "后台口径：后台 draw.io 副本位于 softcopy-materials-engine/.cache/drawio-background/draw.io.app，设置 LSUIElement=true，不修改 /Applications/draw.io.app。",
        "",
        "## 布局约束",
        "",
        "- 图类型必须先判定：系统架构图使用分层架构/组件图，业务流程图使用 UML 活动图，数据关系图使用数据流向图。",
        "- 系统架构图生成前必须先检查项目材料中是否存在平台总体架构、基础架构、部署架构或系统说明；存在时以已有平台架构为底稿裁剪，不用通用模板替代。",
        "- 医药大数据平台类项目的架构图应保留数据源、数据接入、数据处理、数据治理中心、数据服务共享、数据应用和统一支撑/治理/权限/安全等关键层次，并高亮申报软件承担的模块边界。",
        "- 平台架构图不得画成业务流程图；平台内部能力区以并列模块展示，避免使用从数据接入到数据应用逐步流转的连续链式箭头。",
        "- UML 活动图必须使用初始节点、活动节点、判断菱形、终止节点和带箭头控制流；判断流向使用 `[通过]` 等条件文本。",
        "- 分层架构图可使用组件框和数据库圆柱表示边界、模块、数据存储；不强行套活动图符号。",
        "- 数据流向图可使用数据对象、处理节点和数据流箭头表达元数据/血缘/分析结果。",
        "- 画布坐标控制在 x=0-800、y=0-450 范围内。",
        "- 每个节点先确定唯一 ID、坐标、尺寸、颜色和文字，再生成 drawio 单元。",
        "- 连线使用 ID 绑定 source/target，避免靠文字定位。",
        "- 所有连线必须带箭头，箭头应在 PNG/SVG 中可见，不依赖转换器不稳定的 marker 渲染。",
        "- 连线采用正交路由，不能穿过节点正文区域；连线标签位于承载线段中心附近空白处，并与线条保持最小不重叠距离。",
        "- 连线标签字号按线段长度自动适配，范围为 8px-10px，使用常规字重，避免抢过节点标题。",
        "- 正式文档嵌入由 draw.io 从 `.drawio` 导出的 PNG/SVG，源文件保留 `.drawio`。",
        "- `.drawio`、SVG、PNG 禁止长期走三套独立渲染逻辑；如发现不一致，以 `.drawio` 导出结果为准。",
        "",
        "## 图示清单",
        "",
    ]
    for spec in specs:
        lines.append(f"- {spec['title']}（{spec.get('diagram_type', '通用图')}）：{spec['summary']}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def convert_svg_to_png(svg: Path, png: Path) -> bool:
    sips = shutil.which("sips")
    if not sips:
        return False
    png.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [sips, "-s", "format", "png", str(svg), "--out", str(png)],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and png.exists() and png.stat().st_size > 0


def find_drawio_cli() -> str | None:
    background_cli = ensure_background_drawio_cli()
    candidates = [
        background_cli,
        shutil.which("drawio"),
        shutil.which("draw.io"),
        shutil.which("diagrams.net"),
        "/Applications/draw.io.app/Contents/MacOS/draw.io",
        "/Applications/diagrams.net.app/Contents/MacOS/diagrams.net",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def replace_symlink(source: Path, target: Path) -> None:
    if target.exists() or target.is_symlink():
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        else:
            target.unlink()
    os.symlink(source, target)


def ensure_background_drawio_cli() -> str | None:
    source_app = SYSTEM_DRAWIO_APP
    source_cli = source_app / "Contents" / "MacOS" / "draw.io"
    if not source_cli.exists():
        return None

    target_app = BACKGROUND_DRAWIO_APP
    target_contents = target_app / "Contents"
    target_cli = target_contents / "MacOS" / "draw.io"
    source_info = source_app / "Contents" / "Info.plist"
    target_info = target_contents / "Info.plist"

    try:
        if (
            target_cli.exists()
            and target_info.exists()
            and not (target_contents / "Frameworks").is_symlink()
            and not (target_contents / "Resources").is_symlink()
        ):
            with target_info.open("rb") as fh:
                current_info = plistlib.load(fh)
            if current_info.get("LSUIElement") is True:
                return str(target_cli)

        needs_copy = (
            not target_cli.exists()
            or (target_contents / "Frameworks").is_symlink()
            or (target_contents / "Resources").is_symlink()
        )
        if needs_copy:
            if target_app.exists():
                shutil.rmtree(target_app)
            target_app.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source_app, target_app, symlinks=False)

        with source_info.open("rb") as fh:
            info = plistlib.load(fh)
        info["LSUIElement"] = True
        info.pop("LSBackgroundOnly", None)
        with target_info.open("wb") as fh:
            plistlib.dump(info, fh)
        sign_result = subprocess.run(
            ["codesign", "--force", "--sign", "-", str(target_app)],
            check=False,
            capture_output=True,
            text=True,
        )
        if sign_result.returncode != 0:
            return None
    except OSError:
        return None
    return str(target_cli) if target_cli.exists() else None


def export_drawio(drawio: Path, output: Path, image_format: str) -> bool:
    cli = find_drawio_cli()
    if not cli:
        return False
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        cli,
        "--export",
        "--format",
        image_format,
        "--page-index",
        "0",
        "--border",
        "0",
        "--output",
        str(output),
        str(drawio),
    ]
    if image_format == "png":
        command.extend(["--scale", "2"])
    if image_format == "svg":
        command.append("--embed-diagram")
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    return result.returncode == 0 and output.exists() and output.stat().st_size > 0


def write_diagram_files(spec: dict[str, object], drawio: Path, svg: Path, png: Path) -> list[str]:
    issues: list[str] = []
    drawio.write_text(render_drawio(spec), encoding="utf-8")
    exported_svg = export_drawio(drawio, svg, "svg")
    exported_png = export_drawio(drawio, png, "png")
    if not exported_svg:
        svg.write_text(render_svg(spec), encoding="utf-8")
        issues.append(f"{drawio.name} 未能通过 draw.io 导出 SVG，已降级为内置 SVG 渲染器。")
    if not exported_png:
        if not svg.exists():
            svg.write_text(render_svg(spec), encoding="utf-8")
        if not convert_svg_to_png(svg, png):
            issues.append(f"{drawio.name} 未能通过 draw.io 导出 PNG，且 SVG 转 PNG 失败。")
        else:
            issues.append(f"{drawio.name} 未能通过 draw.io 导出 PNG，已降级为 SVG 转 PNG。")
    return issues


def run_sr10_command(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    ensure_entry_dispatch(project_root, project_root)
    drawio_dir = project_root / "03_截图" / "drawio"
    drawio_dir.mkdir(parents=True, exist_ok=True)
    specs = diagram_specs(project_root)
    evidence: list[Path] = []
    issues: list[str] = []

    generation_note = write_diagram_generation_note(project_root, specs)
    visual_review = write_sr10_visual_review(project_root)
    evidence.append(generation_note)
    evidence.append(visual_review)

    for spec in specs:
        slug = str(spec["slug"])
        drawio = drawio_dir / f"{slug}.drawio"
        svg = drawio_dir / f"{slug}.svg"
        png = drawio_dir / f"{slug}.png"
        issues.extend(write_diagram_files(spec, drawio, svg, png))
        evidence.extend([drawio, svg])
        if png.exists():
            evidence.append(png)

    status = "needs-fix" if issues else "confirmed"
    note = f"NextAIDrawIO 图示链路生成完成，图示数：{len(specs)}，正式文件数：{len([p for p in evidence if p.suffix.lower() in {'.drawio', '.svg', '.png'}])}"
    report = write_p3_report(project_root, "SR-10:diagrams", "图示", status, note, evidence, issues)
    confirm_stage(project_root, "SR-10:diagrams", status, f"{note}；报告：{report.relative_to(project_root)}")
    ensure_memory_version(project_root, "SR-10 图示节点已生成 .drawio/SVG/PNG 并写入项目记忆")
    print(report)


def run_p3_command(args: argparse.Namespace) -> None:
    project_root = Path(args.project_root).expanduser().resolve()
    ensure_entry_dispatch(project_root, project_root)

    md_dir = project_root / "04_提交版" / "md"
    word_dir = project_root / "04_提交版" / "word"
    pdf_dir = project_root / "04_提交版" / "pdf"
    screenshot_dir = project_root / "03_截图"
    source_dir = project_root / "02_源代码"

    manual_md = md_dir / "01_系统说明书.md"
    source_md = md_dir / "02_源程序代码.md"
    app_md = md_dir / "03_计算机软件著作权登记申请表.md"
    manual_docx = word_dir / "01_系统说明书.docx"
    source_docx = word_dir / "02_源程序代码.docx"
    app_docx = word_dir / "03_计算机软件著作权登记申请表.docx"
    manual_pdf = pdf_dir / "01_系统说明书.pdf"
    source_pdf = pdf_dir / "02_源程序代码.pdf"
    app_pdf = pdf_dir / "03_计算机软件著作权登记申请表.pdf"

    screenshot_count = count_files(screenshot_dir, {".png", ".jpg", ".jpeg", ".webp"})
    source_count = count_files(source_dir, {".java", ".js", ".ts", ".tsx", ".vue", ".py", ".sql", ".md"})
    drawio_files = [path for path in list_files(screenshot_dir) if path.suffix.lower() in {".drawio", ".svg"}]

    p3_nodes = [
        (
            "SR-06:operation-manual",
            "操作手册",
            [manual_md, manual_docx, manual_pdf],
            [],
            f"系统说明书/操作手册材料已登记，截图数：{screenshot_count}",
        ),
        (
            "SR-07:design-description",
            "设计说明",
            [manual_md],
            [],
            "系统说明书材料已登记，可作为设计说明/说明书路线输入",
        ),
        (
            "SR-08:source-selection",
            "源码选择",
            [source_md, source_docx, source_pdf, source_dir / "PJ1源码摘录" / "源码摘录索引.md"],
            [],
            f"源码材料已登记，源码/说明文件数：{source_count}",
        ),
        (
            "SR-09:screenshot-chain",
            "截图链",
            [screenshot_dir / "截图候选清单.md", screenshot_dir / "章节图片" / "章节图片索引.md"],
            [] if screenshot_count else ["未发现截图文件。"],
            f"截图链材料已登记，截图数：{screenshot_count}",
        ),
        (
            "SR-10:diagrams",
            "图示",
            drawio_files,
            [] if drawio_files else ["未发现 .drawio/.svg 正式图示源文件，需按 NextAIDrawIO 链路补齐。"],
            f"图示链路登记完成，正式图示源文件数：{len(drawio_files)}",
        ),
        (
            "SR-11:submission",
            "提交版",
            [manual_md, source_md, app_md, manual_docx, source_docx, app_docx, manual_pdf, source_pdf, app_pdf],
            [],
            "MD/Word/PDF 提交版材料已登记",
        ),
    ]

    for node_id, title, evidence, issues, note in p3_nodes:
        existing = [path for path in evidence if path.exists()]
        node_issues = list(issues)
        if node_id != "SR-10:diagrams" and not existing:
            node_issues.append("未发现本节点对应材料。")
        status = "needs-fix" if node_issues else "confirmed"
        report = write_p3_report(project_root, node_id, title, status, note, existing, node_issues)
        confirm_note = f"{note}；报告：{report.relative_to(project_root)}"
        confirm_stage(project_root, node_id, status, confirm_note)
    ensure_memory_version(project_root, "P3 材料生成阶段已执行并写入项目记忆")


def list_rules(_: argparse.Namespace) -> None:
    for rel in RULES:
        path = ENGINE_ROOT / rel
        print(path)


def show_paths(_: argparse.Namespace) -> None:
    print(f"ENGINE_ROOT={ENGINE_ROOT}")
    print(f"CAPABILITY_MAP={ENGINE_ROOT / 'CAPABILITY_MAP.md'}")
    print(f"PIPELINE={ENGINE_ROOT / 'pipelines' / 'softcopy_generation_pipeline.md'}")


def show_dashboard_server_command(args: argparse.Namespace) -> None:
    script = ENGINE_ROOT / "scripts" / "status_server.py"
    print(f"{sys.executable} {script} --host {args.host} --port {args.port}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Initialize a project material directory")
    init.add_argument("--project-root", required=True)
    init.add_argument("--software-name", default="")
    init.add_argument("--overwrite", action="store_true")
    init.set_defaults(func=init_project)

    confirm = sub.add_parser("confirm", help="Record an SR confirmation")
    confirm.add_argument("--project-root", required=True)
    confirm.add_argument("--stage", required=True)
    confirm.add_argument("--status", default="confirmed", choices=["confirmed", "blocked", "needs-fix", "skipped"])
    confirm.add_argument("--note", default="已确认")
    confirm.set_defaults(func=confirm_command)

    sync_memory = sub.add_parser("sync-memory", help="Create/update project memory and confirm SR-14")
    sync_memory.add_argument("--project-root", required=True)
    sync_memory.add_argument("--note", default="项目记忆已建立或更新，记忆版本节点完成")
    sync_memory.set_defaults(func=sync_memory_command)

    rules = sub.add_parser("list-rules", help="List migrated rule files")
    rules.set_defaults(func=list_rules)

    paths = sub.add_parser("show-paths", help="Show important engine paths")
    paths.set_defaults(func=show_paths)

    server_cmd = sub.add_parser("show-dashboard-server-command", help="Print the optional dashboard CLI bridge command")
    server_cmd.add_argument("--host", default="127.0.0.1")
    server_cmd.add_argument("--port", default="8765")
    server_cmd.set_defaults(func=show_dashboard_server_command)

    detect = sub.add_parser("detect", help="Generate a lightweight material-status report")
    detect.add_argument("--project-root", required=True)
    detect.add_argument("--source-root", default="")
    detect.set_defaults(func=detect_material_status)

    plan = sub.add_parser("plan", help="Generate a lightweight material strategy report")
    plan.add_argument("--project-root", required=True)
    plan.add_argument("--source-root", default="")
    plan.set_defaults(func=plan_materials)

    project_type = sub.add_parser("identify-project-type", help="Generate SR-02 project type report")
    project_type.add_argument("--project-root", required=True)
    project_type.add_argument("--source-root", default="")
    project_type.set_defaults(func=identify_project_type)

    facts = sub.add_parser("build-facts", help="Generate SR-03 function fact table")
    facts.add_argument("--project-root", required=True)
    facts.add_argument("--source-root", default="")
    facts.set_defaults(func=build_function_facts)

    p1 = sub.add_parser("run-p1", help="Run P1 evidence identification stage")
    p1.add_argument("--project-root", required=True)
    p1.add_argument("--source-root", default="")
    p1.set_defaults(func=run_p1_command)

    app_fields = sub.add_parser("generate-application-fields", help="Generate SR-04 application field confirmation")
    app_fields.add_argument("--project-root", required=True)
    app_fields.add_argument("--source-root", default="")
    app_fields.set_defaults(func=generate_application_fields)

    p2 = sub.add_parser("run-p2", help="Run P2 material planning stage")
    p2.add_argument("--project-root", required=True)
    p2.add_argument("--source-root", default="")
    p2.set_defaults(func=run_p2_command)

    p3 = sub.add_parser("run-p3", help="Run P3 material generation stage")
    p3.add_argument("--project-root", required=True)
    p3.add_argument("--source-root", default="")
    p3.set_defaults(func=run_p3_command)

    sr10 = sub.add_parser("run-sr10", help="Run SR-10 diagram generation with drawio/SVG/PNG outputs")
    sr10.add_argument("--project-root", required=True)
    sr10.set_defaults(func=run_sr10_command)

    templates = sub.add_parser("extract-templates", help="Extract/register soft-copyright template files")
    templates.add_argument("--project-root", required=True)
    templates.add_argument("--template-root", default=str(DEFAULT_TEMPLATE_ROOT))
    templates.add_argument("--copy", action="store_true", help="Copy templates into project 00_材料说明/软著模板")
    templates.set_defaults(func=extract_templates)

    template_rules = sub.add_parser("generate-template-rules", help="Generate rules from soft-copyright templates")
    template_rules.add_argument("--project-root", required=True)
    template_rules.add_argument("--template-root", default=str(DEFAULT_TEMPLATE_ROOT))
    template_rules.set_defaults(func=generate_template_rules)

    check = sub.add_parser("check", help="Run a sidecar lightweight material check")
    check.add_argument("--project-root", required=True)
    check.add_argument(
        "--include-material-notes",
        action="store_true",
        help="Also scan 00_材料说明; default scans submission-related material only.",
    )
    check.set_defaults(func=check_sidecar)

    evaluate = sub.add_parser("evaluate-switch", help="Evaluate whether engine can become production executor")
    evaluate.add_argument("--project-root", required=True)
    evaluate.set_defaults(func=evaluate_switch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
