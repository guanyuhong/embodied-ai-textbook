# 项目进度与阻塞跟踪

> 本文件是 Human Editor 的总控看板。每次 Writer / Auditor 任务完成后更新对应行。
> 状态取值：未开始 / 写作中 / 待审计 / 审计中 / 待修改 / 已合并。

## 1. 章节进度

| 章 | 标题 | 状态 | 负责分支 | 阻塞项 |
|---|---|---|---|---|
| 1 | 具身智能概论 | 未开始 |  |  |
| 2 | 具身智能系统架构 | 未开始 |  |  |
| 3 | 机器人基础与运动控制 | 未开始 |  | 内容偏重，建议分"必讲/选讲"两档 |
| 4 | 具身智能任务建模 | 未开始 |  | 可先用 labs/common 任务包格式作教学抽象 |
| 5 | 视觉感知与场景理解 | 未开始 |  | 建议补"定位与建图(SLAM)"基础 |
| 6 | 导航与路径规划 | 未开始 |  | 可用 labs/common 的 BFS/A* demo |
| 7 | 机器人操作与抓取 | 未开始 |  |  |
| 8 | 反馈、评估与回放 | 未开始 |  | 可用 labs/common 的 metrics/replay |
| 9 | 强化学习基础 | 未开始 |  |  |
| 10 | 模仿学习与数据闭环 | 未开始 |  |  |
| 11 | 大模型与具身智能体 | 未开始 |  | 前沿，时效性强，引用需 verified |
| 12 | 数字孪生与具身仿真平台 | 未开始 |  |  |
| 13 | Sim2Real 与真实机器人部署 | 未开始 |  | 真实 ROS2/硬件需平台方补充 |
| 14 | 高校实验平台与课程实践 | 未开始 |  | RaysTwins 部署/Runner 需平台方补充 |
| 15 | 综合项目 | 未开始 |  |  |
| 16 | 项目展示与拓展方向 | 未开始 |  | 12 项结构对本章偏刚性，考虑轻量模板 |

## 2. 实验进度

| 实验 | 名称 | 状态 | 可落地性 | 阻塞项 |
|---|---|---|---|---|
| lab01 | GridWorld 具身智能体 | 框架就绪 | ✅ 可用 labs/common | 无 |
| lab02 | A* 路径规划 | 框架就绪 | ✅ 可用 labs/common | 无 |
| lab03 | 具身任务包建模 | 框架就绪 | ✅ 可用 labs/common | 无 |
| lab04 | 视觉场景理解 | 未开始 | ⚠️ 需图像/VLM 素材 | 素材与 API |
| lab05 | 轨迹回放与评估 | 框架就绪 | ✅ 可用 labs/common | RaysTwins 回放格式需平台方补充 |
| lab06 | LLM 任务规划器 | 未开始 | ⚠️ 需 LLM API | API 接入方式 |

## 3. 平台资料缺口 → 阻塞映射

> 来源：references/raystwins/README.md。在补齐前，相关实验以 labs/common 的 mock 框架替代。

| 待补资料 | 阻塞的章节/实验 | 当前替代方案 | 负责人 | 状态 |
|---|---|---|---|---|
| 任务包官方 schema | ch04 / lab03 | embodied-lab-task/v0 教学抽象 |  | 待平台方补充 |
| Runner 使用流程/命令 | ch02 / ch14 / 综合实验 | labs/common 内置 Runner |  | 待平台方补充 |
| 回放文件格式 | ch08 / lab05 | labs/common 轨迹 JSON |  | 待平台方补充 |
| 机器人/场景/传感器资产列表 | ch03 / ch05 / ch07 | 文字描述 + GridWorld 抽象 |  | 待平台方补充 |
| 训练/推理提交接口 | ch09 / ch10 | 仅讲通用流程 |  | 待平台方补充 |
| ROS2 对接说明 | ch13 | 仅讲通用 Sim2Real 风险 |  | 待平台方补充 |
| 可公开的平台截图/架构图授权 | ch01 / ch12 / ch14 | 暂用占位说明 |  | 待平台方补充 |
| 图片型 PDF 的可抽取文本 | 全部 RaysTwins 实质内容 | 仅作背景参考 |  | 待平台方补充（建议提供文本版/OCR） |

## 4. 参考来源核验缺口

> 来源：references/sources.yaml。`verified: false` 的条目合并前需核对。

- [ ] 核验全部 `sources` 条目的标题/作者/年份/链接。
- [ ] 补登 SLAM/定位入门资料（gaps.slam_tutorial）。
- [ ] 补登模仿学习入门资料（gaps.imitation_learning）。
- [ ] 补登 Sim2Real 综述（gaps.sim2real）。
- [ ] 登记具身智能综述与 VLA 代表性工作（embodied_ai_survey / vla_reference）。
- [ ] 核验 `caai_embodied_ai_whitepaper_2026`：确认《中国人工智能系列白皮书：具身智能（2026版）》的公开来源或授权状态。

## 5. 新增资料吸收待办

| 来源 | 可补强章节 | 建议吸收方式 | 状态 |
|---|---|---|---|
| `caai_embodied_ai_whitepaper_2026` | ch01 | 拓展阅读中作为国内综述与行业趋势选读；不大改正文主体 | 待来源核验 |
| `caai_embodied_ai_whitepaper_2026` | ch02 | 补“关键技术地图”：感知、推理、操作、导航、交互、强化学习、群体具身智能、世界模型、具身大模型、安全 | 待章节写作时吸收 |
| `caai_embodied_ai_whitepaper_2026` | ch11 | 补“VLA -> WAM”前沿趋势，定位为选读/趋势，不写成成熟工程结论 | 待章节写作时吸收 |
| `caai_embodied_ai_whitepaper_2026` | ch12 | 补数据集、模拟器、仿真平台开放化与标准化、数据飞轮、真实数据与仿真数据互补关系 | 待章节写作时吸收 |
| `caai_embodied_ai_whitepaper_2026` | ch13 | 补虚实结合方法：域随机化、系统辨识、真实感仿真、人工实时干预、语言/世界模型辅助迁移 | 待章节写作时吸收 |
| `caai_embodied_ai_whitepaper_2026` | ch08 / ch13 | 补具身智能安全：越狱、后门、幻觉、传感器攻击、对抗样本、安全控制 | 待章节写作时吸收 |
| `caai_embodied_ai_whitepaper_2026` | ch15 | 作为项目选题池参考：生活服务、工业、农业、交通、能源与电力 | 待项目章写作时吸收 |

## 6. 教学配套进度

| 交付物 | 路径 | 状态 |
|---|---|---|
| 教学大纲 | teacher/teaching_syllabus.md | 未开始 |
| 课件大纲 | teacher/slide_outline.md | 未开始 |
| 评分 Rubric | teacher/grading_rubric.md | 未开始 |
| 学生项目模板 | student/project_template.md | 未开始 |
