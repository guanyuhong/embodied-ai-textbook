#!/usr/bin/env python3
"""解析审计报告开头的 YAML front-matter，输出机读裁决。

用途：让 Auditor 报告的 verdict 可被脚本/CI 消费，而不是停留在自然语言。

退出码：
  0  verdict == pass
  1  verdict == fix（需修改后合并）
  2  verdict == block（不建议合并）
  3  报告缺少 front-matter 或字段非法
"""

from __future__ import annotations

import re
import sys

VERDICT_EXIT = {"pass": 0, "fix": 1, "block": 2}


def extract_front_matter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("用法：audit_verdict.py <审计报告.md>", file=sys.stderr)
        return 3
    with open(argv[0], "r", encoding="utf-8") as handle:
        text = handle.read()

    fields = extract_front_matter(text)
    verdict = fields.get("verdict", "").lower()
    if verdict not in VERDICT_EXIT:
        print(f"未找到合法 verdict（pass/fix/block）：{argv[0]}", file=sys.stderr)
        return 3

    print(f"verdict={verdict} "
          f"blocking={fields.get('blocking_issues', '?')} "
          f"suggested={fields.get('suggested_issues', '?')} "
          f"raystwins_ok={fields.get('raystwins_boundary_ok', '?')} "
          f"structure_ok={fields.get('structure_ok', '?')} "
          f"needs_vendor_docs={fields.get('needs_vendor_docs', '?')}")
    return VERDICT_EXIT[verdict]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
