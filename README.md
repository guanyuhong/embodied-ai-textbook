# 具身智能导论：从数字孪生仿真到智能体实践

本仓库用于编写面向高校的具身智能教材。

## 教材定位

本教材面向高校人工智能、机器人工程、自动化、智能制造、数字孪生等专业，重点讲解具身智能通用理论、系统架构、感知、规划、控制、学习、智能体、数字孪生仿真与综合项目实践。

RaysTwins 作为教学辅助仿真平台之一，用于支撑部分实验和项目实践，不作为平台培训手册。

## 主要目录

- `manuscript/`：教材正文
- `docs/`：GitHub 浏览入口，链接到正文、规范和进度看板
- `labs/`：实验指导书与代码
- `teacher/`：教学大纲、课件大纲、评分标准
- `student/`：学生项目模板
- `prompts/`：Codex 写作提示词
- `references/`：参考资料
- `outputs/`：Codex 审查报告与临时输出
- `standards/`：配图、文风与内容边界规范
- `skills/`：项目内 Codex Skill 源文件

## 协作流程

本项目采用 Writer Codex、Auditor Codex、Human Editor 与 GitHub PR 分工协作。

- Writer Codex 负责写作，允许在明确任务范围内修改正文。
- Auditor Codex 默认只读，只输出审计报告（以机读 `verdict` front-matter 开头），不直接修改正文。
- Human Editor 决定是否采纳审计意见。
- GitHub PR 作为最终合并闸门。

详细流程见 `planning/codex_editorial_workflow.md`，全局进度与阻塞见 `planning/STATUS.md`。

在 GitHub 上直接浏览教材内容，可从 `docs/README.md` 进入；第 1 章正文位于
`manuscript/chapters/ch01_intro.md`。

安装项目专用 Skill：

```bash
scripts/install_project_skill.sh
```

## 工具与自动化

- `scripts/check_manuscript.sh`：确定性检查（违禁词 Blocker / RaysTwins 边界 Warning / 章节结构）。
- `.github/workflows/manuscript-check.yml`：PR/push 上自动运行上述检查，无需密钥。
- `scripts/audit_current_branch.sh` + `scripts/audit_verdict.py`：生成并解析 Codex 审计报告。
- `references/sources.yaml`：参考来源白名单，约束引用、降低幻觉。
- `labs/common/`：平台无关的纯 Python 教学实验框架（任务包→Runner→回放→指标），
  普通机房零依赖即可跑通；RaysTwins 等真实平台作为可替换后端，细节需平台方补充。
