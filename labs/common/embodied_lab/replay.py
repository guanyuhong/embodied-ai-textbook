"""回放：把轨迹保存为 JSON，并以 ASCII 帧序列重放。

对应教材第 8 章的"轨迹记录与回放"与"可解释评估"。
"""

from __future__ import annotations

import json
from typing import Any

from .gridworld import GridWorld


def save_trajectory(path: str, result_dict: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(result_dict, handle, ensure_ascii=False, indent=2)


def load_trajectory(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def render_frames(result_dict: dict[str, Any]) -> list[str]:
    """根据轨迹逐帧渲染 ASCII 画面。"""
    world = result_dict["world"]
    env = GridWorld(world)
    frames: list[str] = []

    header = f"task={result_dict.get('task_id')} agent={result_dict.get('agent_type')}"
    frames.append(header + "\n" + env.render(env.start))

    for record in result_dict.get("trajectory", []):
        state = tuple(record["next_state"])
        tag = " [碰撞]" if record.get("collision") else ""
        frame = f"step={record['step']} action={record['action']}{tag}\n" + env.render(state)
        frames.append(frame)
    return frames


def print_replay(result_dict: dict[str, Any]) -> None:
    for frame in render_frames(result_dict):
        print(frame)
        print("-" * (2 * result_dict["world"]["size"][0]))
