# Git Commit 规范

## 提交格式

使用 Conventional Commits：

```text
<type>(<scope>): <subject>
```

常用 `type`：`feat`、`fix`、`docs`、`refactor`、`test`、`chore`、`build`、`ci`、`revert`。

- `type` 使用英文；`scope` 使用稳定的模块名称，不明确时省略。
- `subject` 简洁表达变更，不超过 72 个字符，不以句号结尾。
- 一个 commit 只完成一个逻辑变更，避免混入无关格式化或临时文件。
- `body` 用中文说明变更原因、实现方式和影响；没有必要时可以省略。
- 破坏性变更在 `type` 后加 `!`，或在 footer 中使用 `BREAKING CHANGE:`。

示例：

```text
feat(user): 增加用户注册接口
fix(order): 修复重复创建订单问题
docs(api): 补充接口使用说明
```

## 提交前检查

提交前检查以下内容：

1. `git status`、`git diff` 和 `git diff --cached`。
2. `git diff --check` 是否存在空白字符错误。
3. 相关测试或构建是否通过。
4. 是否误提交 `.env`、密钥、Token、证书或本地生成文件。

## Git 操作边界

- 未经用户明确授权，不执行 `git commit`、`git rebase`、`git reset` 或 force push。
- 发现一个变更包含多个独立目的时，先提出拆分方案。
- 提交完成后报告 commit hash、变更摘要和验证结果。
