#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

CONTENT_TARGETS=(README.md manuscript/chapters labs teacher student)

echo "== Checking prohibited marketing or platform-binding phrases =="
if rg -n "全球领先|颠覆性|唯一选择|最强|完全基于 RaysTwins|替代所有主流仿真平台" "${CONTENT_TARGETS[@]}"; then
  echo "Found prohibited or high-risk phrases above. Review required."
  exit 1
else
  echo "OK"
fi

echo
echo "== Checking RaysTwins technical-detail risk words =="
if rg -n "RaysTwins.*(SDK|API|Runner|任务包|schema|命令)|RaysTwins 已支持|云端 Runner|本地/云端 Runner" "${CONTENT_TARGETS[@]}"; then
  echo "Review the lines above. If a concrete RaysTwins SDK/API/schema/Runner detail is asserted, cite source or add: 需平台方补充."
else
  echo "OK"
fi

echo
echo "== Checking chapter structure for existing chapter drafts =="
shopt -s nullglob
chapters=(manuscript/chapters/*.md)
if (( ${#chapters[@]} == 0 )); then
  echo "No chapter drafts found."
else
  required=(
    "本章导读"
    "学习目标"
    "关键问题"
    "核心概念"
    "理论基础"
    "方法与算法"
    "平台与工具"
    "RaysTwins 教学辅助案例"
    "本章小结"
    "思考题"
    "实验任务"
    "拓展阅读"
  )
  for chapter in "${chapters[@]}"; do
    for heading in "${required[@]}"; do
      if ! rg -q "$heading" "$chapter"; then
        echo "Missing '$heading' in $chapter"
        exit 1
      fi
    done
  done
  echo "OK"
fi

echo
echo "All checks completed."
