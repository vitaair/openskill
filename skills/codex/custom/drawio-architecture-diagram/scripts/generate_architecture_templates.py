from __future__ import annotations

from pathlib import Path

from drawio_architecture_engine import diagram_specs, write_diagram_files


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "templates" / "diagrams" / "architecture"


def module(x: int, y: int, w: int, h: int, label: str, fill: str, stroke: str, font_size: int = 10) -> dict[str, object]:
    return {
        "id": label.lower().replace(" ", "_").replace("/", "_").replace("\n", "_"),
        "label": label,
        "shape": "component",
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "fill": fill,
        "stroke": stroke,
        "font_size": font_size,
    }


def mid(label: str) -> str:
    return label.lower().replace(" ", "_").replace("/", "_").replace("\n", "_")


def zones() -> list[dict[str, object]]:
    return [
        {"id": "left_zone", "label": "", "shape": "zone", "x": 34, "y": 76, "w": 155, "h": 292, "fill": "#FFFFFF", "stroke": "#C9D7EC"},
        {"id": "main_zone", "label": "", "shape": "zone", "x": 215, "y": 76, "w": 360, "h": 292, "fill": "#FFFFFF", "stroke": "#C9D7EC"},
        {"id": "right_zone", "label": "", "shape": "zone", "x": 602, "y": 76, "w": 155, "h": 292, "fill": "#FFFFFF", "stroke": "#C9D7EC"},
    ]


def architecture_templates() -> list[dict[str, object]]:
    blue = ("#E8F2FF", "#4B7DBF")
    green = ("#EAF7EE", "#4E9B61")
    yellow = ("#FFF6DA", "#C29224")
    red = ("#FFEDED", "#C45D5D")
    purple = ("#F3ECFF", "#8364B5")
    gray = ("#F4F7FB", "#7A8798")
    return [
        {
            "slug": "ARCH01_业务架构图模板",
            "title": "业务架构图模板",
            "diagram_type": "业务架构",
            "summary": "用于表达业务目标、业务能力、核心流程、组织角色和指标闭环。",
            "nodes": zones()
            + [
                module(58, 96, 108, 42, "业务目标\n战略/范围", *blue),
                module(58, 166, 108, 42, "组织角色\n部门/岗位", *green),
                module(58, 236, 108, 42, "外部参与方\n客户/伙伴", *gray),
                module(245, 96, 126, 48, "业务能力域\n能力地图", *purple),
                module(245, 168, 126, 48, "核心业务流程\n端到端链路", *yellow),
                module(245, 240, 126, 48, "业务规则\n策略/约束", *red),
                module(420, 132, 120, 50, "业务服务\n服务目录", *green),
                module(420, 220, 120, 50, "运营指标\n质量/效率", *blue),
                module(628, 132, 104, 44, "业务结果\n交付物", *yellow),
                module(628, 220, 104, 44, "改进闭环\n监控反馈", *purple),
            ],
            "edges": [
                (mid("业务目标\n战略/范围"), mid("业务能力域\n能力地图"), "驱动"),
                (mid("组织角色\n部门/岗位"), mid("核心业务流程\n端到端链路"), "执行"),
                (mid("业务能力域\n能力地图"), mid("业务服务\n服务目录"), "服务化"),
                (mid("核心业务流程\n端到端链路"), mid("业务结果\n交付物"), "输出"),
                (mid("运营指标\n质量/效率"), mid("改进闭环\n监控反馈"), "评估"),
            ],
        },
        {
            "slug": "ARCH02_产品架构图模板",
            "title": "产品架构图模板",
            "diagram_type": "产品架构",
            "summary": "用于表达产品端、功能域、平台能力、运营能力和路线规划。",
            "nodes": [
                {"id": "product_frame", "label": "", "shape": "zone", "x": 55, "y": 80, "w": 690, "h": 290, "fill": "#FFFFFF", "stroke": "#C9D7EC"},
                module(84, 100, 130, 42, "用户入口\nWeb/App/小程序", *blue),
                module(246, 100, 130, 42, "核心功能\n主流程", *purple),
                module(408, 100, 130, 42, "增值功能\n扩展能力", *yellow),
                module(570, 100, 130, 42, "运营后台\n配置/审核", *green),
                module(84, 190, 130, 52, "用户体系\n账号/权限", *green),
                module(246, 190, 130, 52, "内容体系\n对象/资源", *blue),
                module(408, 190, 130, 52, "交易/服务体系\n订单/服务", *red),
                module(570, 190, 130, 52, "数据体系\n统计/分析", *purple),
                module(164, 292, 470, 36, "产品路线：当前能力 / 规划能力 / 后续扩展", *gray),
            ],
            "edges": [],
        },
        {
            "slug": "ARCH03_系统架构图模板",
            "title": "系统架构图模板",
            "diagram_type": "系统架构",
            "summary": "用于表达用户、接入层、服务层、数据层、外部系统和运维支撑。",
            "nodes": [
                module(54, 176, 110, 54, "用户/终端\n浏览器/客户端", *blue),
                module(222, 92, 132, 54, "接入层\n网关/认证", *green),
                module(222, 176, 132, 54, "应用服务层\n业务服务", *yellow),
                module(222, 260, 132, 54, "数据访问层\nDAO/Repository", *purple),
                module(424, 176, 132, 54, "核心服务\n模块/组件", *red),
                {"id": "database", "label": "数据库/缓存\n文件存储", "shape": "database", "x": 424, "y": 260, "w": 132, "h": 74, "fill": gray[0], "stroke": gray[1], "font_size": 10},
                module(626, 144, 110, 54, "外部系统\n第三方服务", *blue),
                module(626, 236, 110, 54, "监控运维\n日志/告警", *green),
            ],
            "edges": [
                (mid("用户/终端\n浏览器/客户端"), mid("接入层\n网关/认证"), "访问"),
                (mid("接入层\n网关/认证"), mid("应用服务层\n业务服务"), "路由"),
                (mid("应用服务层\n业务服务"), mid("核心服务\n模块/组件"), "调用"),
                (mid("核心服务\n模块/组件"), "database", "读写"),
                (mid("核心服务\n模块/组件"), mid("外部系统\n第三方服务"), "集成"),
            ],
        },
        {
            "slug": "ARCH04_数据架构图模板",
            "title": "数据架构图模板",
            "diagram_type": "数据架构",
            "summary": "用于表达数据源、采集、处理、治理、存储、服务和应用消费。",
            "nodes": [
                module(46, 98, 96, 48, "内部数据源", *blue),
                module(46, 182, 96, 48, "外部数据源", *gray),
                module(190, 134, 102, 54, "数据采集\n接口/文件/库表", *purple),
                module(330, 100, 102, 54, "数据处理\n清洗/转换", *yellow),
                module(330, 190, 102, 54, "数据治理\n标准/质量", *red),
                {"id": "data_store", "label": "数据存储\n贴源/标准/主题", "shape": "database", "x": 480, "y": 128, "w": 108, "h": 76, "fill": green[0], "stroke": green[1], "font_size": 10},
                module(630, 100, 100, 48, "数据服务\nAPI/目录", *blue),
                module(630, 190, 100, 48, "数据应用\n分析/报表", *purple),
                module(200, 292, 390, 34, "元数据 / 血缘 / 指标 / 权限 / 安全", *gray),
            ],
            "edges": [
                (mid("内部数据源"), mid("数据采集\n接口/文件/库表"), "输入"),
                (mid("外部数据源"), mid("数据采集\n接口/文件/库表"), "输入"),
                (mid("数据采集\n接口/文件/库表"), mid("数据处理\n清洗/转换"), "处理"),
                (mid("数据处理\n清洗/转换"), "data_store", "入库"),
                ("data_store", mid("数据服务\nAPI/目录"), "发布"),
                (mid("数据服务\nAPI/目录"), mid("数据应用\n分析/报表"), "消费"),
            ],
        },
        {
            "slug": "ARCH05_技术架构图模板",
            "title": "技术架构图模板",
            "diagram_type": "技术架构",
            "summary": "用于表达前端技术、服务技术、中间件、数据组件、基础设施和运维安全。",
            "nodes": [
                module(70, 96, 660, 34, "前端技术：Web / App / 小程序 / 可视化组件", *blue),
                module(70, 148, 660, 34, "服务技术：API 网关 / 微服务框架 / 任务调度 / 权限认证", *green),
                module(70, 200, 660, 34, "中间件：消息队列 / 缓存 / 搜索引擎 / 文件服务", *yellow),
                module(70, 252, 660, 34, "数据组件：关系数据库 / 分布式存储 / 数据仓库 / 元数据", *purple),
                module(70, 304, 660, 34, "基础设施：容器 / 虚拟机 / 网络 / 监控 / 日志 / 安全", *red),
            ],
            "edges": [],
        },
        {
            "slug": "ARCH06_应用架构图模板",
            "title": "应用架构图模板",
            "diagram_type": "应用架构",
            "summary": "用于表达前端 UI、展示层、应用服务层、基础服务层和基础设施层。",
            "nodes": [
                module(70, 82, 600, 42, "前端 UI：APP / PC / 小程序 / M 站", *blue),
                module(70, 140, 600, 48, "展示层：页面 / 运营系统 / 管理端 / 运维入口", *red),
                module(70, 206, 600, 54, "应用服务层：应用服务 / 权限服务 / 工作流 / 对接平台服务", *blue),
                module(70, 278, 600, 54, "基础服务层：基础服务 / 通用能力 / 任务调度 / 文件服务", *red),
                module(70, 356, 600, 42, "基础设施层：MySQL / Redis / ES / 消息队列 / 监控 / 日志", *blue),
                module(690, 140, 52, 120, "中台", *red),
                module(690, 82, 52, 80, "前台", *green),
            ],
            "edges": [],
        },
        {
            "slug": "ARCH07_功能架构图模板",
            "title": "功能架构图模板",
            "diagram_type": "功能架构",
            "summary": "用于表达系统功能域、一级功能、二级功能和横向公共能力。",
            "nodes": [
                module(312, 78, 176, 42, "系统功能体系", *blue),
                module(72, 154, 140, 52, "基础管理\n用户/角色/字典", *green),
                module(252, 154, 140, 52, "核心业务\n新增/编辑/审核", *yellow),
                module(432, 154, 140, 52, "查询分析\n统计/报表/导出", *purple),
                module(612, 154, 140, 52, "系统运维\n日志/监控/配置", *red),
                module(72, 256, 680, 44, "公共能力：权限控制 / 数据范围 / 消息通知 / 操作留痕 / 异常处理", *gray),
            ],
            "edges": [
                (mid("系统功能体系"), mid("基础管理\n用户/角色/字典"), "包含"),
                (mid("系统功能体系"), mid("核心业务\n新增/编辑/审核"), "包含"),
                (mid("系统功能体系"), mid("查询分析\n统计/报表/导出"), "包含"),
                (mid("系统功能体系"), mid("系统运维\n日志/监控/配置"), "包含"),
            ],
        },
        {
            "slug": "ARCH08_信息架构图模板",
            "title": "信息架构图模板",
            "diagram_type": "信息架构",
            "summary": "用于表达首页、导航、栏目、详情页、操作页和辅助信息之间的组织关系。",
            "nodes": [
                module(334, 72, 132, 40, "首页/入口", *blue),
                module(88, 150, 120, 44, "导航 A\n列表/详情", *green),
                module(250, 150, 120, 44, "导航 B\n查询/筛选", *yellow),
                module(412, 150, 120, 44, "导航 C\n配置/维护", *purple),
                module(574, 150, 120, 44, "导航 D\n帮助/设置", *red),
                module(88, 246, 606, 44, "信息组织：分类 / 标签 / 搜索 / 面包屑 / 状态 / 操作入口", *gray),
                module(250, 326, 300, 34, "用户路径：入口 -> 栏目 -> 详情 -> 操作 -> 反馈", *blue),
            ],
            "edges": [
                (mid("首页/入口"), mid("导航 A\n列表/详情"), "进入"),
                (mid("首页/入口"), mid("导航 B\n查询/筛选"), "进入"),
                (mid("首页/入口"), mid("导航 C\n配置/维护"), "进入"),
                (mid("首页/入口"), mid("导航 D\n帮助/设置"), "进入"),
            ],
        },
    ]


def write_readme(specs: list[dict[str, object]]) -> None:
    lines = [
        "# 架构图模板库",
        "",
        "来源参考：https://www.cnblogs.com/wuhuixuri/articles/18342003",
        "",
        "说明：本目录将文章中的八类架构图抽象为软著材料可复用模板。模板只复用图类型、层级和布局方法，不复制文章图片内容。",
        "",
        "| 模板 | 类型 | 用途 |",
        "|---|---|---|",
    ]
    for spec in specs:
        lines.append(f"| `{spec['slug']}` | {spec['diagram_type']} | {spec['summary']} |")
    lines.extend(
        [
            "",
            "## 使用规则",
            "",
            "- 生成正式材料前，必须用项目事实替换模板占位文本。",
            "- 软著提交图必须保留 `.drawio` 源文件，并导出 SVG/PNG。",
            "- 平台型项目优先使用数据架构图、系统架构图、技术架构图和应用架构图模板。",
            "- 流程类图仍按 UML 活动图规则生成，不用架构图模板代替。",
            "",
        ]
    )
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    specs = architecture_templates()
    platform_spec = diagram_specs(Path("PJ1-大数据平台"))[0]
    platform_spec = {
        **platform_spec,
        "slug": "ARCH09_大数据平台总体架构复刻模板",
        "title": "大数据平台总体架构复刻模板",
        "diagram_type": "平台总体架构",
        "summary": "基于用户手动调整后的 PJ1 架构图沉淀，适用于大数据平台、数据治理、主数据管理、数据资产类项目。",
    }
    specs.append(platform_spec)
    for spec in specs:
        slug = str(spec["slug"])
        drawio = OUT / f"{slug}.drawio"
        svg = OUT / f"{slug}.svg"
        png = OUT / f"{slug}.png"
        write_diagram_files(spec, drawio, svg, png)
    write_readme(specs)
    print(f"generated {len(specs)} architecture templates: {OUT}")


if __name__ == "__main__":
    main()
