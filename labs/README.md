# 实验目录说明

本目录存放教材配套实验。设计原则：

1. **平台无关优先**：基础实验先用 `labs/common/`（纯 Python 框架）跑通，
   不依赖任何商业平台资料；RaysTwins / PyBullet / Isaac 仅作为可替换后端。
2. **可复现**：实验通过结构化任务包描述，结果可回放、可评估。
3. **小步交付**：每个实验单独成一个 PR。

## 共享框架

`labs/common/` 提供 `embodied_lab`：任务包 → Runner → 回放 → 指标 的完整闭环。
详见 `labs/common/README.md`。

## 实验与框架对应关系

| 实验 | 名称 | 可用框架能力 | 平台依赖 |
|---|---|---|---|
| lab01 | GridWorld 具身智能体 | `gridworld` + `random` 智能体 | 无 |
| lab02 | A* 路径规划 | `bfs` / `astar` 智能体对比 | 无 |
| lab03 | 具身任务包建模 | `task_package` 校验 | 无 |
| lab04 | 视觉场景理解 | （图像/VLM，框架外） | 需素材，详见各实验 README |
| lab05 | 轨迹回放与评估 | `runner` + `replay` + `metrics` | 无（RaysTwins 回放格式需平台方补充） |
| lab06 | LLM 任务规划器 | 由 LLM 产出任务包，交框架执行 | 需 LLM API |

> 综合实验涉及 RaysTwins / Isaac 等真实后端时，相关安装、任务包 schema、
> Runner 命令、回放格式**需平台方补充**，在补充前以本地 mock 框架替代演示。
