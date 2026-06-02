"""命令行入口。

用法（在 labs/common 目录下）：
  python -m embodied_lab.cli validate --task examples/warehouse_nav.json
  python -m embodied_lab.cli run      --task examples/warehouse_nav.json --render
  python -m embodied_lab.cli replay   --trajectory outputs/warehouse_nav_demo.json
  python -m embodied_lab.cli benchmark --task examples/warehouse_nav.json --episodes 20
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .task_package import load_task_package, validate_task_package, _load_raw
from .runner import run_task
from .metrics import compute_metrics, aggregate_metrics
from .replay import save_trajectory, load_trajectory, print_replay


def _cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_task_package(_load_raw(args.task))
    if errors:
        print("任务包校验问题：")
        for e in errors:
            print(f"  - {e}")
        blocking = [e for e in errors if not e.startswith("schema 建议为")]
        return 1 if blocking else 0
    print("任务包校验通过。")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    task = load_task_package(args.task)
    result = run_task(task)
    metrics = compute_metrics(result)

    print("== 运行结果 ==")
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    out_dir = args.out or "outputs"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{result.task_id}.json")
    save_trajectory(out_path, result.to_dict())
    print(f"\n轨迹已保存：{out_path}")

    if args.render:
        print()
        print_replay(result.to_dict())
    return 0 if result.success else 3


def _cmd_replay(args: argparse.Namespace) -> int:
    data = load_trajectory(args.trajectory)
    print_replay(data)
    return 0


def _cmd_benchmark(args: argparse.Namespace) -> int:
    base = load_task_package(args.task)
    results = []
    for i in range(args.episodes):
        raw = dict(base.raw)
        raw["seed"] = base.seed + i
        task = load_task_package_from_dict(raw)
        results.append(run_task(task))
    print(json.dumps(aggregate_metrics(results), ensure_ascii=False, indent=2))
    return 0


def load_task_package_from_dict(raw):
    from .task_package import TaskPackage, SCHEMA_ID

    return TaskPackage(
        id=raw["id"],
        title=raw["title"],
        world=raw["world"],
        agent=raw["agent"],
        metrics=raw.get("metrics", ["success", "collisions", "path_length", "steps"]),
        description=raw.get("description", ""),
        seed=int(raw.get("seed", 0)),
        schema=raw.get("schema", SCHEMA_ID),
        raw=raw,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="embodied_lab", description="平台无关教学实验框架")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="校验任务包")
    p_validate.add_argument("--task", required=True)
    p_validate.set_defaults(func=_cmd_validate)

    p_run = sub.add_parser("run", help="执行任务包")
    p_run.add_argument("--task", required=True)
    p_run.add_argument("--render", action="store_true", help="打印 ASCII 回放")
    p_run.add_argument("--out", default=None, help="轨迹输出目录")
    p_run.set_defaults(func=_cmd_run)

    p_replay = sub.add_parser("replay", help="回放已保存的轨迹")
    p_replay.add_argument("--trajectory", required=True)
    p_replay.set_defaults(func=_cmd_replay)

    p_bench = sub.add_parser("benchmark", help="多种子批量评估")
    p_bench.add_argument("--task", required=True)
    p_bench.add_argument("--episodes", type=int, default=10)
    p_bench.set_defaults(func=_cmd_benchmark)

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
