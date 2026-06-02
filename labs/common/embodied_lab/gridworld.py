"""GridWorld：内置的二维栅格环境（默认教学后端）。

坐标约定：cell = (x, y)，0 <= x < width，0 <= y < height。
动作：up / down / left / right。撞墙或越界视为一次碰撞，位置保持不变。

Runner 仅依赖此处暴露的 reset / step / render 接口。接入真实仿真平台
（如 RaysTwins、PyBullet）时，应实现同样的接口作为可替换后端。
"""

from __future__ import annotations

from typing import Any

ACTIONS = ("up", "down", "left", "right")
_DELTA = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


class GridWorld:
    def __init__(self, world: dict[str, Any]):
        self.width, self.height = world["size"]
        self.start = tuple(world["start"])
        self.goal = tuple(world["goal"])
        self.obstacles = {tuple(o) for o in world.get("obstacles", [])}
        self.state = self.start
        self.actions = ACTIONS

    def reset(self) -> tuple[int, int]:
        self.state = self.start
        return self.state

    def is_free(self, cell: tuple[int, int]) -> bool:
        x, y = cell
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return cell not in self.obstacles

    def step(self, action: str) -> tuple[tuple[int, int], float, bool, dict[str, Any]]:
        dx, dy = _DELTA[action]
        x, y = self.state
        candidate = (x + dx, y + dy)
        collision = not self.is_free(candidate)
        if not collision:
            self.state = candidate
        done = self.state == self.goal
        reward = 10.0 if done else (-1.0 if collision else -0.1)
        info = {"collision": collision}
        return self.state, reward, done, info

    def render(self, state: tuple[int, int] | None = None) -> str:
        cur = state if state is not None else self.state
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = (x, y)
                if cell == cur:
                    row.append("A")
                elif cell == self.goal:
                    row.append("G")
                elif cell == self.start:
                    row.append("S")
                elif cell in self.obstacles:
                    row.append("#")
                else:
                    row.append(".")
            rows.append(" ".join(row))
        return "\n".join(rows)
