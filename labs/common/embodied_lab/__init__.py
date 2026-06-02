"""embodied_lab：平台无关的教学实验框架。

定位：
  - 这是一套用于高校教学的最小可运行框架，纯标准库实现，可在普通机房直接跑通。
  - 它提供"任务包 → 仿真执行 → 轨迹回放 → 指标评估"的完整闭环，用于支撑
    实验 1（GridWorld）、实验 2（A*）、实验 3（任务包建模）、实验 5（回放评估）。
  - 框架中的任务包格式是面向教学的抽象（schema: embodied-lab-task/v0），
    不是任何商业平台的官方格式。

与平台的关系：
  - Runner 仅依赖抽象的 Environment 接口；GridWorld 是默认的内置后端。
  - 接入 RaysTwins / PyBullet / Isaac 等真实后端时，应另写一个实现相同接口的适配器；
    RaysTwins 的安装、任务包官方 schema、Runner 命令等细节"需平台方补充"。
"""

from .task_package import TaskPackage, load_task_package, validate_task_package
from .gridworld import GridWorld
from .runner import RunResult, run_task
from .metrics import compute_metrics, aggregate_metrics

__all__ = [
    "TaskPackage",
    "load_task_package",
    "validate_task_package",
    "GridWorld",
    "RunResult",
    "run_task",
    "compute_metrics",
    "aggregate_metrics",
]
