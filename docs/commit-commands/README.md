# commit-commands

[简体中文](README.md) · [English](../../i18n/en/docs/commit-commands/README.md) · [繁體中文](../../i18n/zh-TW/docs/commit-commands/README.md) · [日本語](../../i18n/ja/docs/commit-commands/README.md) · [한국어](../../i18n/ko/docs/commit-commands/README.md)

`commit-commands` 将 [Anthropic 官方原版](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) 的三个 slash command 适配为原生 Codex skill：

```text
$commit
$commit-push-pr
$clean-gone
```

工作流步骤以原版为准。Codex 适配差异包括原生 skill 结构、明确意图的自动选择、`$skill-name` 显式入口，以及通过 `UserPromptSubmit` hook 为提交动态加入当前 Codex 模型与思考强度。

## 安装与启用

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

安装或更新后请在 `/hooks` 中审查并信任 `commit-commands` hook，再新开 Codex thread，使新的 skill 和 hook 元数据进入会话。

## 自动选择示例

- “提交这些改动”可以自动选择 `commit`。
- “提交这些改动、推送并创建 PR”可以自动选择 `commit-push-pr`。
- “清理所有 gone 分支”可以自动选择 `clean-gone`。
- “功能已经完成”不会自行触发任何 Git 副作用。

## `$commit`

检查 `git status`、`git diff HEAD`、当前分支和最近十条提交，暂存当前改动并创建一个 commit。生成的提交会追加：

```text
Generated with [Codex](https://chatgpt.com/codex)
Model: <active-model-slug> <active-reasoning-effort>

Co-authored-by: Codex <noreply@openai.com>
```

Codex 会把当前模型 slug 直接传给 command hook，但当前 schema 不提供思考强度。插件只接受 hook 未来可能直接提供的 effort，或用当前 `turn_id` 与模型精确匹配 `transcript_path` 尾部的 `turn_context`；它不会从用户配置猜测当前 effort，因为 CLI、项目、profile 与运行时覆盖可能让文件值过期。解析器只提取 attribution 字段，不复制或保存 prompt 内容，也不依赖 Python 3.11 才提供的 `tomllib`。由于 transcript 格式并非稳定接口，解析失败时会省略强度后缀；hook 未信任、模型上下文缺失或模型不可用时，skill 才会在暂存和提交前停止。

该 skill 不会推送或创建 PR；没有改动时也不会创建空提交。

## `$commit-push-pr`

检查当前状态、diff、分支以及相对目标 base 的提交。工作区有改动时，只有当前分支恰好是 `main` 才创建新分支，然后创建一个带模型 attribution 的 commit；工作区干净但当前分支已有目标 base 之外的提交时，会直接发布这些已有提交。两条路径都会推送到 `origin`。

skill 不会直接调用 `gh pr create`，而是把完整 PR 正文交给内置 `scripts/create_pr_with_attribution.py` wrapper。wrapper 支持 GitHub.com 与 GitHub Enterprise PR URL，会追加尾注、通过 `--body-file` 创建 PR、反读正文，并在缺失时修复一次；只有最后一个非空行验证通过才返回 PR URL：

```text
Generated with [Codex](https://chatgpt.com/codex)
```

该 skill 只在用户明确要求 PR 时触发。没有工作区改动且当前分支相对目标 base 也没有提交时，它不会创建空 commit 或空 PR；也不会因为其他分支名称不符合仓库策略而自动迁移分支。需要确定使用此工作流时，可以显式调用 `$commit-push-pr`。

需要已安装并登录 GitHub CLI，仓库还需要配置 `origin` remote。

## `$clean-gone`

使用 `git branch -v` 和 `git worktree list` 查找标记为 `[gone]` 的分支。对每个候选项，先使用 `git worktree remove --force` 强制移除关联的非主 worktree，再使用 `git branch -D` 强制删除分支。

这是与原版一致的破坏性行为：不会自动 fetch，不验证是否已合并，不检查 worktree 是否干净，也不保护 ignored 文件或集成分支。调用前必须自行确认仓库状态。

## 本地验证

```bash
python -m py_compile plugins/commit-commands/hooks/model_context.py
'{"hook_event_name":"UserPromptSubmit","model":"gpt-5.6-sol","effort":"xhigh"}' | python plugins/commit-commands/hooks/model_context.py
python -m unittest discover -s tests
codex plugin list
```
