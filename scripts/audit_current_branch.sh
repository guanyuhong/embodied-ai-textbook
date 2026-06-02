#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
SAFE_BRANCH="$(printf '%s' "$BRANCH" | tr '/ ' '__')"
OUT_DIR="outputs/audits"
mkdir -p "$OUT_DIR"

BASE_REF="${1:-}"
if [[ -z "$BASE_REF" ]]; then
  if git rev-parse --verify origin/main >/dev/null 2>&1; then
    BASE_REF="origin/main"
  elif git rev-parse --verify main >/dev/null 2>&1; then
    BASE_REF="main"
  else
    BASE_REF="$(git rev-list --max-parents=0 HEAD | tail -n 1)"
  fi
fi

DIFF_FILE="$OUT_DIR/${SAFE_BRANCH}.diff.patch"
STAGED_FILE="$OUT_DIR/${SAFE_BRANCH}.staged.patch"
WORKTREE_FILE="$OUT_DIR/${SAFE_BRANCH}.worktree.patch"
CHECK_LOG="$OUT_DIR/${SAFE_BRANCH}_check.log"
REPORT_FILE="$OUT_DIR/${SAFE_BRANCH}_audit.md"

echo "Generating diff against ${BASE_REF}..."
git diff "${BASE_REF}...HEAD" > "$DIFF_FILE"
git diff --cached > "$STAGED_FILE"
git diff > "$WORKTREE_FILE"

echo "Running manuscript checks..."
set +e
scripts/check_manuscript.sh > "$CHECK_LOG" 2>&1
CHECK_STATUS=$?
set -e

PROMPT="$(cat <<EOF
你是本教材项目的独立 Codex Auditor。

请阅读：
- AGENTS.md
- audit/AUDITOR.md
- metadata/course_spec.yaml
- metadata/terminology.yaml
- manuscript/book_outline.md
- manuscript/chapter_template.md
- references/raystwins/README.md
- ${DIFF_FILE}
- ${STAGED_FILE}
- ${WORKTREE_FILE}
- ${CHECK_LOG}

当前分支：${BRANCH}
对比基准：${BASE_REF}
脚本检查退出码：${CHECK_STATUS}

请审计当前分支相对于基准分支以及当前工作区的修改。

重点检查：
1. 是否符合高校教材定位；
2. 是否过度宣传 RaysTwins；
3. RaysTwins 是否只是教学辅助仿真平台；
4. 是否有未经证实的平台能力、SDK、API、任务包 schema、Runner 命令；
5. 是否每章包含固定 12 项结构；
6. 是否适合 48 学时课程；
7. 是否需要平台方补充资料；
8. 是否存在结构混乱、术语不统一、重复内容；
9. 是否建议合并。

请不要修改正文。
请按照 prompts/audit/01_audit_pr.md 中的报告格式输出 Markdown 审计报告。
EOF
)"

if ! command -v codex >/dev/null 2>&1; then
  {
    echo "# 审计报告：${BRANCH}"
    echo
    echo "未找到 codex 命令，无法自动生成审计报告。"
    echo
    echo "已生成以下输入文件："
    echo
    echo "- ${DIFF_FILE}"
    echo "- ${STAGED_FILE}"
    echo "- ${WORKTREE_FILE}"
    echo "- ${CHECK_LOG}"
    echo
    echo "请安装或配置 Codex CLI 后重新运行："
    echo
    echo '```bash'
    echo "scripts/audit_current_branch.sh ${BASE_REF}"
    echo '```'
  } > "$REPORT_FILE"
  echo "Codex CLI not found. Stub report generated:"
  echo "$REPORT_FILE"
  exit 1
fi

SANDBOX="${CODEX_AUDIT_SANDBOX:-read-only}"
echo "Running Codex Auditor with sandbox: ${SANDBOX}"
codex exec --sandbox "$SANDBOX" "$PROMPT" > "$REPORT_FILE"

echo "Audit report generated:"
echo "$REPORT_FILE"

