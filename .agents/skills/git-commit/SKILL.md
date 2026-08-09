---
name: git-commit
description: 按项目 Git 提交规范分析变更、拆分逻辑提交、生成和检查 Conventional Commits message。用户要求创建 commit、编写 commit message、检查提交规范或整理待提交变更时使用。
---

# Git Commit

以仓库根目录的 `AGENTS.md` 为唯一规范来源，本 Skill 只负责执行提交准备流程。

## 工作流程

1. 确认当前目录是 Git 仓库，检查分支、工作区状态、未暂存差异和已暂存差异；具体命令以 `AGENTS.md` 为准。
2. 分析变更目的、影响模块和文件范围，识别密钥、Token、`.env` 等敏感文件。
3. 评估变更是否需要按逻辑拆分，并列出拆分方案。
4. 按 `AGENTS.md` 生成和检查 commit message。
5. 按 `AGENTS.md` 执行提交前检查，并运行相关测试或构建；如果 Ruff 只报告格式问题，自动执行 formatter，复查差异后重新检查。
6. 提交前展示拟提交文件、message、检查结果和风险，等待用户明确授权。
7. 获得授权后才执行 commit；完成后核验状态并报告 commit hash、摘要和验证结果。

## 异常处理

- 不猜测 Git 状态；不是 Git 仓库、没有变更或状态无法确认时，明确说明原因。
- 需要高风险 Git 操作时，遵守 `AGENTS.md` 的授权边界并先征得用户同意。
- 只自动修复纯格式问题；发现可能影响业务语义的 lint 问题时，先报告并等待确认。
