"""任务包：教学用结构化任务描述。

schema 标识为 "embodied-lab-task/v0"，是面向教学的抽象格式，
不等同于任何商业平台的官方任务包格式。
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

SCHEMA_ID = "embodied-lab-task/v0"
KNOWN_AGENTS = {"random", "bfs", "astar"}


@dataclass
class TaskPackage:
    id: str
    title: str
    world: dict[str, Any]
    agent: dict[str, Any]
    metrics: list[str] = field(default_factory=lambda: ["success", "collisions", "path_length", "steps"])
    description: str = ""
    seed: int = 0
    schema: str = SCHEMA_ID
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def max_steps(self) -> int:
        return int(self.agent.get("max_steps", 200))

    @property
    def agent_type(self) -> str:
        return str(self.agent.get("type", "astar")).lower()


def _load_raw(path: str) -> dict[str, Any]:
    ext = os.path.splitext(path)[1].lower()
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    if ext in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover - 取决于环境
            raise RuntimeError(
                "读取 YAML 任务包需要 pyyaml。请 `pip install pyyaml`，"
                "或改用 JSON 任务包（无需任何依赖）。"
            ) from exc
        return yaml.safe_load(text)
    return json.loads(text)


def validate_task_package(data: dict[str, Any]) -> list[str]:
    """返回错误列表，空列表表示通过。"""
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["任务包顶层必须是对象。"]

    if data.get("schema") != SCHEMA_ID:
        errors.append(f"schema 建议为 '{SCHEMA_ID}'，当前为 {data.get('schema')!r}。")

    for key in ("id", "title", "world", "agent"):
        if key not in data:
            errors.append(f"缺少必填字段：{key}")

    world = data.get("world", {})
    if isinstance(world, dict):
        if world.get("type") != "gridworld":
            errors.append("当前内置后端仅支持 world.type == 'gridworld'。")
        size = world.get("size")
        if not (isinstance(size, (list, tuple)) and len(size) == 2):
            errors.append("world.size 必须为 [width, height]。")
        else:
            width, height = size

            def _in_bounds(cell: Any) -> bool:
                return (
                    isinstance(cell, (list, tuple))
                    and len(cell) == 2
                    and 0 <= cell[0] < width
                    and 0 <= cell[1] < height
                )

            for key in ("start", "goal"):
                cell = world.get(key)
                if not _in_bounds(cell):
                    errors.append(f"world.{key} 必须在 [0,{width}) x [0,{height}) 范围内。")
            obstacles = world.get("obstacles", [])
            if not isinstance(obstacles, list):
                errors.append("world.obstacles 必须为列表。")
            else:
                obstacle_set = {tuple(o) for o in obstacles if isinstance(o, (list, tuple)) and len(o) == 2}
                for key in ("start", "goal"):
                    cell = world.get(key)
                    if isinstance(cell, (list, tuple)) and tuple(cell) in obstacle_set:
                        errors.append(f"world.{key} 不能落在障碍物上。")
    else:
        errors.append("world 必须是对象。")

    agent = data.get("agent", {})
    if isinstance(agent, dict):
        agent_type = str(agent.get("type", "")).lower()
        if agent_type not in KNOWN_AGENTS:
            errors.append(f"agent.type 应为 {sorted(KNOWN_AGENTS)} 之一，当前为 {agent_type!r}。")
        max_steps = agent.get("max_steps", 200)
        if not (isinstance(max_steps, int) and max_steps > 0):
            errors.append("agent.max_steps 必须为正整数。")
    else:
        errors.append("agent 必须是对象。")

    return errors


def load_task_package(path: str, strict: bool = True) -> TaskPackage:
    data = _load_raw(path)
    errors = validate_task_package(data)
    blocking = [e for e in errors if not e.startswith("schema 建议为")]
    if strict and blocking:
        raise ValueError("任务包校验失败：\n  - " + "\n  - ".join(errors))
    return TaskPackage(
        id=data["id"],
        title=data["title"],
        world=data["world"],
        agent=data["agent"],
        metrics=data.get("metrics", ["success", "collisions", "path_length", "steps"]),
        description=data.get("description", ""),
        seed=int(data.get("seed", 0)),
        schema=data.get("schema", SCHEMA_ID),
        raw=data,
    )
