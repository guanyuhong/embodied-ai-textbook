你是本教材项目的 Writer Codex。

请先阅读：

- AGENTS.md
- metadata/course_spec.yaml
- metadata/terminology.yaml
- manuscript/book_outline.md
- manuscript/chapter_template.md
- standards/figure_standard.md
- standards/style_guide.md
- standards/content_standard.md
- references/raystwins/README.md

任务：

请按人工指定的章节编号和章节标题，扩写一个章节初稿。

写作要求：

1. 使用高校教材口吻，准确、清晰、克制。
2. 严格采用 `manuscript/chapter_template.md` 的 12 项结构。
3. 先讲通用原理，再讲主流平台对照，最后讲 RaysTwins 教学辅助案例。
4. RaysTwins 内容控制在教学辅助案例范围内，不写成产品手册。
5. 不编造 RaysTwins SDK、API、任务包 schema、Runner 命令。
6. 涉及缺失的平台资料时，标注“需平台方补充”。
7. 每章至少包含 3 个核心概念、3 道思考题和 1 个实验任务。
8. 不大面积改写其他章节或规划文件。
9. "拓展阅读"引用的来源必须来自 `references/sources.yaml`；不在白名单的来源先登记再引用。
10. 按 `standards/style_guide.md` 使用定义框、例子框、概念辨析框；按 `standards/figure_standard.md` 规划配图。
11. 导论章和概念章按 `standards/content_standard.md` 控制平台细节，不提前展开 SDK/API/schema/Runner。
12. 在章节文件**末尾**追加一段写作自检（HTML 注释，不计入正文、不在成书中显示），
    供 Auditor 复核，减少重复全查。格式如下：

```text
<!-- writer-selfcheck
chapter: chXX
template_sections_complete: true        # 12 项结构是否齐全
raystwins_within_1_2_pages: true        # RaysTwins 案例是否控制在 1-2 页
no_fabricated_platform_details: true    # 是否未编造 SDK/API/schema/Runner
figures_planned:                        # 本章配图规划，列出图号、图题、路径
  - 图 X-1 <图题> -> figures/chXX/figX-1_name.svg
style_boxes_used:                       # 定义/例/概念辨析等教材化组件
  - 定义 X-1 <标题>
content_boundary_ok: true               # 是否符合 standards/content_standard.md 的章节边界
vendor_todo:                            # 本章"需平台方补充"清单
  - <逐条列出>
human_confirm:                          # 需人工确认的事实
  - <逐条列出>
sources_cited:                          # 引用来源 id，均来自 references/sources.yaml
  - <id>
-->
```

输出位置：

`manuscript/chapters/chXX_title.md`

完成后请运行：

```bash
scripts/check_manuscript.sh
```

并在回复中说明修改了哪些文件，提醒人工检查 `git diff`。同时更新 `planning/STATUS.md` 中对应行的状态。
