"""教学智能体：随机、BFS、A*。

- RandomAgent：随机动作，作为对照基线（实验 1）。
- BFSAgent：在自由栅格上做广度优先搜索得到最短路径（实验 1/2）。
- AStarAgent：曼哈顿启发式 A*（实验 2）。

规划型智能体在 reset() 时拿到完整地图（全可观测，便于教学对比搜索算法），
随后逐步吐出动作。若无可行路径，act() 返回 None，由 Runner 判定失败。
"""

from __future__ import annotations

import heapq
import random
from collections import deque

from .gridworld import GridWorld, ACTIONS, _DELTA


def _neighbors(env: GridWorld, cell):
    for action in ACTIONS:
        dx, dy = _DELTA[action]
        nxt = (cell[0] + dx, cell[1] + dy)
        if env.is_free(nxt):
            yield action, nxt


def _actions_from_path(path):
    """把坐标路径转换成动作序列。"""
    actions = []
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        for action, (dx, dy) in _DELTA.items():
            if (x0 + dx, y0 + dy) == (x1, y1):
                actions.append(action)
                break
    return actions


class RandomAgent:
    def __init__(self, env: GridWorld, seed: int = 0):
        self.env = env
        self._rng = random.Random(seed)

    def reset(self) -> None:
        pass

    def act(self, observation):
        return self._rng.choice(ACTIONS)


class BFSAgent:
    def __init__(self, env: GridWorld, seed: int = 0):
        self.env = env
        self._plan: list[str] = []
        self._cursor = 0

    def reset(self) -> None:
        self._plan = _actions_from_path(self._search())
        self._cursor = 0

    def _search(self):
        start, goal = self.env.start, self.env.goal
        frontier = deque([start])
        came_from = {start: None}
        while frontier:
            current = frontier.popleft()
            if current == goal:
                break
            for _action, nxt in _neighbors(self.env, current):
                if nxt not in came_from:
                    came_from[nxt] = current
                    frontier.append(nxt)
        if goal not in came_from:
            return []
        path = [goal]
        while path[-1] != start:
            path.append(came_from[path[-1]])
        path.reverse()
        return path

    def act(self, observation):
        if self._cursor >= len(self._plan):
            return None
        action = self._plan[self._cursor]
        self._cursor += 1
        return action


class AStarAgent(BFSAgent):
    @staticmethod
    def _heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _search(self):
        start, goal = self.env.start, self.env.goal
        open_heap = [(self._heuristic(start, goal), 0, start)]
        came_from = {start: None}
        cost = {start: 0}
        while open_heap:
            _f, g, current = heapq.heappop(open_heap)
            if current == goal:
                break
            for _action, nxt in _neighbors(self.env, current):
                new_cost = g + 1
                if nxt not in cost or new_cost < cost[nxt]:
                    cost[nxt] = new_cost
                    priority = new_cost + self._heuristic(nxt, goal)
                    heapq.heappush(open_heap, (priority, new_cost, nxt))
                    came_from[nxt] = current
        if goal not in came_from:
            return []
        path = [goal]
        while path[-1] != start:
            path.append(came_from[path[-1]])
        path.reverse()
        return path


_REGISTRY = {"random": RandomAgent, "bfs": BFSAgent, "astar": AStarAgent}


def make_agent(agent_type: str, env: GridWorld, seed: int = 0):
    key = agent_type.lower()
    if key not in _REGISTRY:
        raise ValueError(f"未知 agent 类型：{agent_type}，可选 {sorted(_REGISTRY)}")
    return _REGISTRY[key](env, seed=seed)
