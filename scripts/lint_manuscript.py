#!/usr/bin/env python3
"""教材稿件确定性检查器。

职责：
  1. Blocker（致命，退出码 1）：营销绝对化表述、平台绑定表述。
  2. Warning（提示，默认不致命）：RaysTwins 技术细节断言、缺少"需平台方补充"标注、
     RaysTwins 教学辅助案例篇幅超限、配图图号/路径/图注格式问题。
  3. 章节结构：仅对 manuscript/chapters/*.md 校验 12 项固定结构是否齐全、按序、非空壳。

设计取舍：
  - 用精确词组而非单字，避免"唯一解/唯一性约束/最强连通分量"等正常用法被误伤。
  - Warning 与 Blocker 严格分档，退出码语义清晰，便于在 CI 中作为闸门。
  - 纯标准库，无需密钥与三方依赖，可直接在 GitHub Actions 上运行。

退出码：
  0  通过（可能含 warning，非严格模式）
  1  存在 blocker，或严格模式下存在 warning
  2  调用方式错误
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Iterable

# ---- 可配置阈值 ----
RAYSTWINS_SECTION_HEADING = "RaysTwins 教学辅助案例"
RAYSTWINS_MAX_LINES = int(os.environ.get("RAYSTWINS_MAX_LINES", "110"))  # ~1-2 页非空行
VENDOR_PLACEHOLDER = "需平台方补充"

# ---- 章节固定结构（按出现顺序）----
REQUIRED_HEADINGS = [
    "本章导读",
    "学习目标",
    "关键问题",
    "核心概念",
    "理论基础",
    "方法与算法",
    "平台与工具",
    "RaysTwins 教学辅助案例",
    "本章小结",
    "思考题",
    "实验任务",
    "拓展阅读",
]

# ---- Blocker：营销绝对化 / 平台绑定（精确词组）----
BLOCKER_PATTERNS = [
    (r"全球领先", "营销化绝对表述"),
    (r"颠覆性", "营销化绝对表述"),
    (r"唯一选择", "平台绑定/绝对表述"),
    (r"RaysTwins\s*是\s*唯一", "平台绑定/绝对表述"),
    (r"业界最强|最强(平台|仿真|方案|引擎)", "营销化绝对表述"),
    (r"完全基于\s*RaysTwins", "单一平台绑定"),
    (r"替代所有(主流)?(仿真平台)?", "夸大替代性表述"),
    (r"本教材.{0,6}基于\s*RaysTwins", "单一平台绑定"),
]

# ---- Warning：RaysTwins 技术细节断言（断言式动词 + 技术名词）----
# 仅在"断言具体能力/接口/命令"时提示，普通定位性描述不触发。
RAYSTWINS_TECH_TERMS = r"(SDK|API|REST|Runner|schema|任务包格式|命令行|CLI|接口|字段)"
RAYSTWINS_ASSERT_VERBS = r"(支持|提供|包括|采用|调用|是|为|定义为|格式为|命令为|通过)"
WARNING_TECH_ASSERTION = re.compile(
    r"RaysTwins[^。\n]{0,40}" + RAYSTWINS_TECH_TERMS + r"[^。\n]{0,12}" + RAYSTWINS_ASSERT_VERBS
)
# 形似具体命令调用：raystwins 后接 ASCII 子命令/参数（避免把"RaysTwins 作为…"中文误判）。
WARNING_COMMAND_LIKE = re.compile(r"raystwins\s+[a-z][a-z0-9_-]*", re.IGNORECASE)

# ---- Warning：配图格式轻检查 ----
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
FIGURE_ALT_RE = re.compile(r"^图\s+(\d+)-(\d+)\s+\S")
FIGURE_PATH_RE = re.compile(
    r"(?:^|/|\.\./)figures/ch(\d{2})/fig(\d+)-(\d+)_[a-z0-9_]+\.(svg|png|jpg|jpeg|pdf)$",
    re.IGNORECASE,
)


@dataclass
class Finding:
    severity: str  # "blocker" | "warning"
    path: str
    line: int
    message: str


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, severity: str, path: str, line: int, message: str) -> None:
        self.findings.append(Finding(severity, path, line, message))

    @property
    def blockers(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "blocker"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]


def iter_markdown_files(targets: Iterable[str]) -> list[str]:
    files: list[str] = []
    for target in targets:
        if not os.path.exists(target):
            continue
        if os.path.isfile(target):
            if target.endswith(".md"):
                files.append(target)
            continue
        for root, _dirs, names in os.walk(target):
            for name in sorted(names):
                if name.endswith(".md"):
                    files.append(os.path.join(root, name))
    return sorted(set(files))


def read_lines(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read().splitlines()


def check_words(path: str, lines: list[str], report: Report) -> None:
    has_vendor_placeholder = any(VENDOR_PLACEHOLDER in line for line in lines)
    tech_mentioned = False

    for idx, line in enumerate(lines, start=1):
        for pattern, label in BLOCKER_PATTERNS:
            if re.search(pattern, line):
                report.add("blocker", path, idx, f"{label}：命中 /{pattern}/")

        if WARNING_TECH_ASSERTION.search(line) and VENDOR_PLACEHOLDER not in line:
            tech_mentioned = True
            report.add(
                "warning",
                path,
                idx,
                "疑似断言 RaysTwins 具体技术细节，请核对来源或补'需平台方补充'。",
            )
        if WARNING_COMMAND_LIKE.search(line):
            tech_mentioned = True
            report.add(
                "warning",
                path,
                idx,
                "疑似出现 RaysTwins 具体命令，若无官方资料请改为'需平台方补充'。",
            )

    if tech_mentioned and not has_vendor_placeholder:
        report.add(
            "warning",
            path,
            0,
            "本文件涉及 RaysTwins 技术细节，但全文未出现'需平台方补充'标注。",
            )


def check_figures(path: str, lines: list[str], report: Report) -> None:
    in_code_fence = False
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        for match in IMAGE_RE.finditer(line):
            alt = match.group(1).strip()
            image_path = match.group(2).strip()
            is_local_figure = "figures/" in image_path or "figures\\" in image_path
            looks_numbered = alt.startswith("图 ")
            if not (is_local_figure or looks_numbered):
                continue

            alt_match = FIGURE_ALT_RE.match(alt)
            if not alt_match:
                report.add(
                    "warning",
                    path,
                    idx,
                    "配图 alt 文本应以'图 X-Y 图题'开头。",
                )
                continue

            fig_chapter = int(alt_match.group(1))
            fig_index = int(alt_match.group(2))

            path_match = FIGURE_PATH_RE.search(image_path)
            if not path_match:
                report.add(
                    "warning",
                    path,
                    idx,
                    "配图路径应符合 figures/chXX/figX-Y_name.svg|png|jpg|jpeg|pdf。",
                )
            else:
                path_ch_dir = int(path_match.group(1))
                path_fig_chapter = int(path_match.group(2))
                path_fig_index = int(path_match.group(3))
                if (path_ch_dir, path_fig_chapter, path_fig_index) != (
                    fig_chapter,
                    fig_chapter,
                    fig_index,
                ):
                    report.add(
                        "warning",
                        path,
                        idx,
                        "配图 alt 图号与文件路径章节/序号不一致。",
                    )

            caption = _next_non_empty_line(lines, idx)
            if caption is None or not caption.startswith(f"图 {fig_chapter}-{fig_index} "):
                report.add(
                    "warning",
                    path,
                    idx,
                    "配图后应紧跟以相同图号开头的图注。",
                )


def _next_non_empty_line(lines: list[str], current_line_no: int) -> str | None:
    for line in lines[current_line_no:]:
        stripped = line.strip()
        if stripped:
            return stripped
    return None


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


def parse_headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """返回 [(line_no, level, text), ...]。"""
    headings: list[tuple[int, int, str]] = []
    in_code_fence = False
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((idx, len(match.group(1)), match.group(2)))
    return headings


def section_content_lines(
    lines: list[str], headings: list[tuple[int, int, str]], heading_index: int
) -> list[str]:
    """取某标题到下一个同级或更高级标题之间的内容行。"""
    start_line, level, _text = headings[heading_index]
    end_line = len(lines) + 1
    for nxt_line, nxt_level, _ in headings[heading_index + 1 :]:
        if nxt_level <= level:
            end_line = nxt_line
            break
    return lines[start_line:end_line - 1]


def check_structure(path: str, lines: list[str], report: Report) -> None:
    headings = parse_headings(lines)
    heading_texts = [text for _ln, _lvl, text in headings]

    last_pos = -1
    ordered = True
    for required in REQUIRED_HEADINGS:
        found_at = None
        for pos, text in enumerate(heading_texts):
            if required in text:
                found_at = pos
                break
        if found_at is None:
            report.add("blocker", path, 0, f"缺少固定结构标题：'{required}'")
            continue
        if found_at < last_pos:
            ordered = False
        last_pos = max(last_pos, found_at)

        content = section_content_lines(lines, headings, found_at)
        non_empty = [c for c in content if c.strip() and not HEADING_RE.match(c)]
        if not non_empty:
            report.add("blocker", path, headings[found_at][0], f"结构标题为空壳：'{required}'")

    if not ordered:
        report.add("warning", path, 0, "固定结构标题出现顺序与模板不一致，请核对。")

    for pos, text in enumerate(heading_texts):
        if RAYSTWINS_SECTION_HEADING in text:
            content = section_content_lines(lines, headings, pos)
            non_empty = [c for c in content if c.strip()]
            if len(non_empty) > RAYSTWINS_MAX_LINES:
                report.add(
                    "warning",
                    path,
                    headings[pos][0],
                    f"RaysTwins 教学辅助案例篇幅偏长（{len(non_empty)} 非空行 > {RAYSTWINS_MAX_LINES}），"
                    "应控制在 1-2 页，避免喧宾夺主。",
                )
            break


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="教材稿件确定性检查器")
    parser.add_argument("targets", nargs="*", help="待检查文件或目录")
    parser.add_argument("--strict", action="store_true", help="将 warning 视为失败")
    parser.add_argument(
        "--chapters-dir",
        default="manuscript/chapters",
        help="需做结构校验的章节目录",
    )
    args = parser.parse_args(argv)

    if not args.targets:
        print("用法：lint_manuscript.py <文件或目录> [...] [--strict]", file=sys.stderr)
        return 2

    if os.environ.get("LINT_STRICT") == "1":
        args.strict = True

    report = Report()
    all_files = iter_markdown_files(args.targets)

    for path in all_files:
        lines = read_lines(path)
        check_words(path, lines, report)
        check_figures(path, lines, report)

    chapter_files = iter_markdown_files([args.chapters_dir])
    if not chapter_files:
        print(f"提示：{args.chapters_dir} 下暂无章节草稿，跳过结构检查。")
    for path in chapter_files:
        lines = read_lines(path)
        check_structure(path, lines, report)

    _print_report(report, args.strict)

    if report.blockers:
        return 1
    if args.strict and report.warnings:
        return 1
    return 0


def _print_report(report: Report, strict: bool) -> None:
    def fmt(f: Finding) -> str:
        loc = f"{f.path}:{f.line}" if f.line else f.path
        return f"  {loc}  {f.message}"

    print("== Blocker（致命，必须修复）==")
    if report.blockers:
        for f in report.blockers:
            print(fmt(f))
    else:
        print("  OK")

    print()
    print("== Warning（建议复核）==")
    if report.warnings:
        for f in report.warnings:
            print(fmt(f))
    else:
        print("  OK")

    print()
    print(
        f"汇总：{len(report.blockers)} blocker, {len(report.warnings)} warning"
        + ("（严格模式：warning 也将判失败）" if strict else "")
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
