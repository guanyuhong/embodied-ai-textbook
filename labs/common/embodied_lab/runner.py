"""Runner：执行任务包，产出轨迹与运行结果。

这是教学用的内置 Runner。它只依赖抽象的环境接口（reset/step），
因此可被真实平台后端替换。RaysTwins 等平台的 Runner 命令/接口"需平台方补充"。
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

from .task_package import TaskPackage
from .gridworld import GridWorld
from .agents import make_agent


@dataclass
class RunResult:
    task_id: str
    agent_type: str
    success: bool
    steps: int
    collisions: int
    path_length: int
    reached_goal: bool
    trajectory: list[dict[str, Any]] = field(default_factory=list)
    world: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_task(task: TaskPackage) -> RunResult:
    if task.world.get("type") != "gridworld":
        raise ValueError("内置 Runner 仅支持 gridworld。其他后端需平台方补充适配器。")

    env = GridWorld(task.world)
    agent = make_agent(task.agent_type, env, seed=task.seed)

    state = env.reset()
    agent.reset()

    trajectory: list[dict[str, Any]] = []
    collisions = 0
    path_length = 0
    done = False
    step = 0

    for step in range(1, task.max_steps + 1):
        action = agent.act(state)
        if action is None:  # 规划器判定无可行路径或计划已耗尽
            break
        prev = state
        state, reward, done, info = env.step(action)
        if info.get("collision"):
            collisions += 1
        if state != prev:
            path_length += 1
        trajectory.append(
            {
                "step": step,
                "state": list(prev),
                "action": action,
                "next_state": list(state),
                "collision": bool(info.get("collision")),
                "reward": reward,
            }
        )
        if done:
            break

    return RunResult(
        task_id=task.id,
        agent_type=task.agent_type,
        success=done,
        steps=len(trajectory),
        collisions=collisions,
        path_length=path_length,
        reached_goal=done,
        trajectory=trajectory,
        world=task.world,
    )
