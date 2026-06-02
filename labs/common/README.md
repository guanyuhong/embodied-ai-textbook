# embodied_lab：平台无关教学实验框架

本目录提供一套**纯 Python 标准库**的最小可运行框架，用于支撑教材的基础实验。
它实现了完整闭环：

```text
任务包(JSON/YAML) → 仿真执行(Runner) → 轨迹回放(Replay) → 指标评估(Metrics)
```

设计目标是：**在没有任何商业平台资料、没有 GPU、普通机房的条件下也能跑通实验**，
从而让实验 1/2/3/5 不被外部平台资料卡死。

## 与平台的关系（重要边界）

- 本框架的任务包格式标识为 `embodied-lab-task/v0`，是**面向教学的抽象格式**，
  **不是任何商业平台（含 RaysTwins）的官方任务包格式**。
- `Runner` 只依赖抽象的环境接口（`reset` / `step` / `render`）。`GridWorld` 是默认内置后端。
- 接入 RaysTwins、PyBullet、Isaac 等真实后端时，应另写一个实现相同接口的适配器。
  RaysTwins 的安装部署、官方任务包 schema、Runner 命令、回放格式等细节**需平台方补充**。

## 快速开始

无需安装任何依赖（JSON 任务包）。在本目录下执行：

```bash
# 1. 校验任务包
python3 -m embodied_lab.cli validate --task examples/warehouse_nav.json

# 2. 执行任务并打印 ASCII 回放
python3 -m embodied_lab.cli run --task examples/warehouse_nav.json --render

# 3. 回放已保存的轨迹
python3 -m embodied_lab.cli replay --trajectory outputs/warehouse_nav_demo.json

# 4. 多种子批量评估（对比 random / bfs / astar）
python3 -m embodied_lab.cli benchmark --task examples/warehouse_nav.json --episodes 20
```

YAML 任务包为可选项，需要 `pip install pyyaml`；JSON 任务包零依赖。

## 任务包字段（v0）

| 字段 | 含义 |
|---|---|
| `schema` | 固定 `embodied-lab-task/v0` |
| `id` / `title` / `description` | 任务标识与说明 |
| `world.type` | 当前内置后端仅支持 `gridworld` |
| `world.size` | `[width, height]` |
| `world.start` / `world.goal` | 起点 / 目标，`[x, y]` |
| `world.obstacles` | 障碍物坐标列表 |
| `agent.type` | `random` / `bfs` / `astar` |
| `agent.max_steps` | 单次运行最大步数 |
| `metrics` | 需统计的指标名 |
| `seed` | 随机种子（影响 random 智能体） |

## 模块结构

| 模块 | 职责 | 对应实验 |
|---|---|---|
| `task_package.py` | 任务包加载与校验 | 实验 3 任务包建模 |
| `gridworld.py` | 栅格环境（状态/动作/反馈） | 实验 1 GridWorld |
| `agents.py` | random / BFS / A* 智能体 | 实验 1、实验 2 |
| `runner.py` | 执行任务并记录轨迹 | 实验 5 |
| `metrics.py` | 成功率/碰撞/路径长度/步数 | 实验 5、第 8 章 |
| `replay.py` | 轨迹保存与 ASCII 回放 | 实验 5、第 8 章 |
| `cli.py` | 命令行入口 | 全部 |

## 教学用法建议

- **实验 1（GridWorld）**：用 `random` 智能体观察状态—动作—反馈，理解为何随机策略低效。
- **实验 2（A\*）**：对比 `bfs` 与 `astar` 的扩展节点与路径，理解启发式搜索。
- **实验 3（任务包建模）**：让学生自行编写/修改任务包并通过 `validate`，理解可复现实验。
- **实验 5（回放评估）**：用 `benchmark` 跑多种子，填写实验报告中的指标表与失败分析。
