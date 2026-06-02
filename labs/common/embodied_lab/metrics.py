"""指标：从运行结果计算评估指标，并支持多次运行的聚合。

教学指标对应教材第 8 章（反馈、评估与回放）：
成功率、碰撞数、路径长度、步数。
"""

from __future__ import annotations

from typing import Any, Iterable

from .runner import RunResult


def compute_metrics(result: RunResult) -> dict[str, Any]:
    return {
        "task_id": result.task_id,
        "agent_type": result.agent_type,
        "success": result.success,
        "steps": result.steps,
        "collisions": result.collisions,
        "path_length": result.path_length,
        "reached_goal": result.reached_goal,
    }


def aggregate_metrics(results: Iterable[RunResult]) -> dict[str, Any]:
    results = list(results)
    n = len(results)
    if n == 0:
        return {"runs": 0}
    success = sum(1 for r in results if r.success)
    return {
        "runs": n,
        "success_rate": round(success / n, 4),
        "avg_steps": round(sum(r.steps for r in results) / n, 2),
        "avg_collisions": round(sum(r.collisions for r in results) / n, 2),
        "avg_path_length": round(sum(r.path_length for r in results) / n, 2),
    }
