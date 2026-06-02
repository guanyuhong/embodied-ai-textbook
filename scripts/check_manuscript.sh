#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# 待检查的正文目标。结构检查只作用于 manuscript/chapters，词级检查作用于全部。
CONTENT_TARGETS=(README.md manuscript/chapters labs teacher student)

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "未找到 $PYTHON_BIN，请安装 Python 3 后重试。" >&2
  exit 2
fi

EXTRA_ARGS=()
# 设置环境变量 LINT_STRICT=1 可将 warning 视为失败（用于 CI 严格闸门）。
if [[ "${LINT_STRICT:-0}" == "1" ]]; then
  EXTRA_ARGS+=(--strict)
fi

echo "== 运行教材稿件确定性检查 =="
set +e
"$PYTHON_BIN" scripts/lint_manuscript.py "${CONTENT_TARGETS[@]}" ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}
STATUS=$?
set -e

echo
if [[ "$STATUS" -eq 0 ]]; then
  echo "检查通过。请仍人工检查 git diff。"
else
  echo "检查未通过（退出码 $STATUS）。请修复 Blocker 后重试。"
fi
exit "$STATUS"
