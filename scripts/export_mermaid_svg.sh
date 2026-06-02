#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v npx >/dev/null 2>&1; then
  echo "未找到 npx（需要 Node.js/npm）。请先安装 Node.js，或在 CI 中运行该脚本。" >&2
  exit 2
fi

detect_chrome() {
  # 优先用系统浏览器，避免 puppeteer 下载浏览器失败/耗时。
  local candidates=(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
  )
  for p in "${candidates[@]}"; do
    if [[ -x "$p" ]]; then
      echo "$p"
      return 0
    fi
  done
  return 1
}

if [[ -z "${PUPPETEER_EXECUTABLE_PATH:-}" ]]; then
  if CHROME_PATH="$(detect_chrome)"; then
    export PUPPETEER_EXECUTABLE_PATH="$CHROME_PATH"
  fi
fi

echo "== Export Mermaid .mmd -> .svg =="
echo "提示：首次运行请先执行 npm install"
echo

shopt -s nullglob
FILES=(figures/**/*.mmd)
if (( ${#FILES[@]} == 0 )); then
  echo "未找到 figures/**/*.mmd"
  exit 0
fi

for src in "${FILES[@]}"; do
  dst="${src%.mmd}.svg"
  echo "- ${src} -> ${dst}"
  npx -y mmdc -i "$src" -o "$dst" --backgroundColor transparent
done

echo
echo "Done."

