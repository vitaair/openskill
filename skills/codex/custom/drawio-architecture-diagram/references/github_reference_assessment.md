# GitHub 外部参考项目评估

评估时间：2026-05-14

## 已本地化项目

| 项目 | 本地路径 | 上游地址 | 定位 |
|---|---|---|---|
| GitDiagram | `vendor/github-references/gitdiagram` | `https://github.com/ahmedkhaleel2004/gitdiagram` | GitHub 仓库到交互式架构图的生成工具 |
| OpenGithubs profile | `vendor/github-references/OpenGithubs` | `https://github.com/OpenGithubs/OpenGithubs` | OpenGithubs 社区主页与项目说明 |
| OpenGithubs weekly | `vendor/github-references/weekly` | `https://github.com/OpenGithubs/weekly` | GitHub 精选项目周刊 |
| OpenGithubs weekly rank | `vendor/github-references/github-weekly-rank` | `https://github.com/OpenGithubs/github-weekly-rank` | GitHub 每周飙升榜 |

说明：`https://github.com/OpenGithubs` 是账号主页，不是单一仓库。已按参考价值克隆 profile 仓库和两个代表性索引仓库。

## GitDiagram 参考价值

结论：高。适合作为“源码/仓库自动生成架构图”的流程参考，但不能直接作为软著正式图输出链路。

可借鉴能力：

| 能力 | GitDiagram 做法 | 软著 Skill 可采用方式 |
|---|---|---|
| 仓库资料提取 | 读取默认分支、递归文件树、README，并过滤依赖、图片、缓存等噪声文件 | SR-03/SR-07 可增加“源码结构快照”，先过滤再抽取模块事实 |
| 结构化图模型 | 先生成解释，再生成 groups/nodes/edges 的结构化图模型 | SR-10 可先生成 drawio-neutral graph JSON，再渲染为 drawio |
| 图模型校验 | 校验 group id、node id、edge 引用、节点 path 是否真实存在 | SR-10 必须增加 drawio spec 校验，防止节点、连线、路径虚构 |
| 重试反馈 | 图模型不合法时把 validation feedback 返给模型重试 | 可用于质检整改角色：图不合规时自动给出整改反馈 |
| 节点路径绑定 | 节点可绑定真实仓库路径并点击跳转 | 软著材料可保留“源码映射表”，但正式 PDF 图不强制做交互 |
| 渲染分层 | groups + nodes + edges，节点 shape 支持 box/database/queue/document/circle/hexagon | 可映射到 drawio 组件框、数据库、文档、队列、判断等图形 |

不采用内容：

- 不采用 Mermaid 作为正式提交图输出。软著正式链路仍是 `.drawio + SVG + PNG`。
- 不引入远程服务、R2、Redis、Vercel/Railway 等运行依赖。
- 不引入浏览器交互式图作为提交材料，仅参考交互式状态看板思路。

## OpenGithubs 参考价值

结论：中。它不是画图项目，但适合做“外部参考项目发现和评分”的素材源。

可借鉴能力：

| 能力 | 参考方式 | 软著 Skill 可采用方式 |
|---|---|---|
| 项目发现 | 周刊、月刊、榜单按时间维护开源项目清单 | `reference_projects.html` 可增加“来源/榜单/更新时间/领域”字段 |
| 项目元数据 | 项目名、简介、stars、趋势、期刊链接 | 外部参考项目索引可按 stars、主题域、用途分类 |
| 长期维护 | 每周/月更新，形成历史索引 | 软著 Skill 的参考库可按“已本地化/待评估/已采用/废弃”维护状态 |

不采用内容：

- 不作为架构图模板来源。
- 不作为软著项目事实来源。
- 不自动把榜单项目内容写入申报材料。

## 对软著 Skill 的优化建议

1. 新增 `repo-graph-model` 中间层：
   - 输入：源码目录、README、系统说明、功能事实表。
   - 输出：`groups/nodes/edges` 结构化 JSON。
   - 校验：节点 ID、连线端点、源码路径、模块名称是否存在。

2. SR-10 图生成链路升级：
   - 事实输入 -> graph JSON -> drawio spec -> `.drawio` -> SVG/PNG。
   - 不能直接从自然语言生成最终图。

3. 外部参考项目索引升级：
   - 增加来源类型：模板库、图形库、图生成工具、项目发现清单。
   - 增加参考价值：高/中/低。
   - 增加采用方式：直接模板、方法论、流程参考、仅索引。

4. 保留本地化原则：
   - 所有参考项目 clone 到 `vendor/`。
   - 正式流程只读参考，不运行外部服务。
   - 不把外部项目源码、示例业务名、示例图直接写入软著材料。
