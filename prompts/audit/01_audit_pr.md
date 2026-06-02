你是本教材项目的独立 Codex Auditor。

请阅读：

- AGENTS.md
- audit/AUDITOR.md
- metadata/course_spec.yaml
- metadata/terminology.yaml
- manuscript/book_outline.md
- manuscript/chapter_template.md
- standards/figure_standard.md
- standards/style_guide.md
- standards/content_standard.md
- references/raystwins/README.md
- 当前分支相对于 main 或 origin/main 的 diff
- 当前工作区 staged / unstaged diff，如存在
- `scripts/check_manuscript.sh` 的检查结果，如存在

审计目标：

请审计当前分支的修改是否适合进入 GitHub PR 合并流程。

重点检查：

1. 是否符合高校教材定位。
2. 是否保持“先通用原理，再主流平台对照，最后 RaysTwins 教学辅助案例”。
3. 是否过度宣传 RaysTwins。
4. RaysTwins 是否只是教学辅助仿真平台之一。
5. 是否有未经证实的平台能力、SDK、API、任务包 schema、Runner 命令。
6. 每章是否包含固定 12 项结构。
7. 是否包含学习目标、核心概念、思考题、实验任务。
8. 是否适合 48 学时课程和本科高年级学生。
9. 实验是否具备环境、步骤、输入输出、结果记录和评分标准。
10. 是否存在结构混乱、术语不统一、重复内容或逻辑跳跃。
11. 是否需要平台方补充资料。
12. 是否按 `standards/figure_standard.md` 给出配图规划或图位占位。
13. 是否按 `standards/style_guide.md` 使用定义框、例子框、概念辨析框等教材化组件。
14. 导论章是否存在过早展开平台细节、实验评分细节、SDK/API/schema/Runner 的问题。
15. RaysTwins 内容是否压缩在教学辅助范围内。
16. 是否建议合并。

请不要修改正文。

请输出 Markdown 审计报告。报告**必须以 YAML front-matter 开头**（机器可读，供脚本/CI 解析裁决），
随后是人类可读的报告正文。格式如下：

```text
---
audit_target: <分支名或 PR 编号>
verdict: pass            # pass=可以合并 / fix=修改后合并 / block=不建议合并
blocking_issues: 0       # 阻塞问题数量
suggested_issues: 0      # 建议修改问题数量
raystwins_boundary_ok: true   # RaysTwins 边界是否守住
structure_ok: true            # 12 项固定结构是否齐全
needs_vendor_docs: false      # 是否存在需平台方补充的资料
check_manuscript_passed: true # scripts/check_manuscript.sh 是否通过
---
```

verdict 三值必须与第 1 节结论、第 10 节合并建议一致。报告正文格式如下：

# 审计报告：PR / 分支名称

## 1. 总体结论

结论：可以合并 / 修改后合并 / 不建议合并

一句话说明。

## 2. 阻塞合并的问题

| 编号 | 问题 | 位置 | 原因 | 建议 |
|---|---|---|---|---|

## 3. 建议修改的问题

| 编号 | 问题 | 位置 | 建议 |
|---|---|---|---|

## 4. 轻微问题或可选优化

| 编号 | 问题 | 位置 | 建议 |
|---|---|---|---|

## 5. RaysTwins 边界检查

- 是否过度宣传：
- 是否喧宾夺主：
- 是否编造 API / SDK / Runner / 任务包 schema：
- 是否标注“需平台方补充”：

## 6. 高校教材适配检查

- 学习目标：
- 核心概念：
- 理论基础：
- 方法与算法：
- 思考题：
- 实验任务：
- 术语一致性：
- 教材化组件：
- 配图规划：

## 7. 实验可执行性检查

- 环境是否明确：
- 步骤是否完整：
- 输入输出是否清楚：
- 结果记录是否存在：
- 评分标准是否存在：

## 8. 需平台方补充资料

- 

## 9. 给 Writer Codex 的修改 Prompt

请基于当前修改继续处理：

1. 
2. 
3. 

要求：不改变本次任务范围，不大面积重写全书，继续遵守 AGENTS.md。

## 10. 合并建议

可以合并 / 修改后合并 / 不建议合并
