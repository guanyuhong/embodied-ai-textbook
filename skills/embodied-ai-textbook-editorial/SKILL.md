---
name: embodied-ai-textbook-editorial
description: Use when writing, revising, auditing, or planning figures for the textbook 《具身智能导论：从数字孪生仿真到智能体实践》. Applies to chapter drafting, textbook-style polishing, chapter audit, RaysTwins boundary checks, and figure planning.
---

# Embodied AI Textbook Editorial Skill

Use this skill for this repository when working on textbook chapters, experiments, audits, or figure plans.

## Required Context

Before writing or auditing, read the relevant files:

- `AGENTS.md`
- `metadata/course_spec.yaml`
- `metadata/terminology.yaml`
- `manuscript/book_outline.md`
- `manuscript/chapter_template.md`
- `standards/figure_standard.md`
- `standards/style_guide.md`
- `standards/content_standard.md`
- `references/raystwins/README.md`
- `references/sources.yaml` when citing readings

## Writing Rules

- Use restrained higher-education textbook language.
- Preserve the 12-section chapter structure unless the user explicitly requests a different artifact.
- Add textbook components where useful: definition boxes, example boxes, concept-differentiation boxes, tables, and planned figures.
- Keep RaysTwins as a teaching-aid simulation platform, not a product manual or sole platform.
- Do not invent RaysTwins SDK/API/schema/Runner details; mark missing technical materials as `需平台方补充`.
- Keep chapter work scoped to one chapter, one lab, or one audit task.

## Figure Planning

- Prefer Mermaid source files and SVG output for conceptual diagrams.
- Use `figures/chXX/figX-Y_name.mmd` for source and `figures/chXX/figX-Y_name.svg` for export.
- Markdown figure references should start with `图 X-Y` and use a matching file path.
- Screenshots require teaching purpose and authorization.

## Audit Rules

- Check textbook tone, fixed structure, RaysTwins boundary, content boundary, source whitelist, and figure plan.
- For introductory chapters, flag platform details that should move to later chapters or labs.
- Auditor must propose changes, not rewrite manuscript text directly.
