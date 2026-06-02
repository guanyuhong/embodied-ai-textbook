# 附录 B Python 与实验环境速查

> 骨架。用于承接全部实验与 labs/common 框架，定位为速查。

## B.1 Python 基础回顾

- 数据类型、列表/字典、函数、类。
- 待补充。

## B.2 实验环境准备

- Python 3 安装与版本检查。
- labs/common 零依赖运行说明（详见 labs/common/README.md）。
- 可选依赖：YAML 任务包需 `pip install pyyaml`。
- 待补充。

## B.3 常用命令速查

```bash
# 校验 / 运行 / 回放 / 批量评估教学任务包
python3 -m embodied_lab.cli validate  --task examples/warehouse_nav.json
python3 -m embodied_lab.cli run       --task examples/warehouse_nav.json --render
python3 -m embodied_lab.cli replay    --trajectory outputs/warehouse_nav_demo.json
python3 -m embodied_lab.cli benchmark --task examples/warehouse_nav.json --episodes 20
```
