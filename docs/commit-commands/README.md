# Commit Commands

`commit-commands` 是一个把常用 Git 提交流程封装成 Codex slash commands 的插件。

它适配了 Anthropic `commit-commands` 的核心体验：

```text
/commit
/commit-push-pr
/clean_gone
```

## 安装

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

## `/commit`

用于日常开发中快速提交当前改动。

它会让 Codex 查看工作区、diff 和最近 commit 风格，生成合适的提交信息，stage 相关文件，并创建单个 commit。

默认追加：

```text
Co-authored-by: Codex <noreply@openai.com>
```

## `/commit-push-pr`

用于功能完成后发布分支并打开 PR。

它会先读取仓库内的协作规范，识别基线分支和受保护分支。如果当前位于 `main`、`master`、`dev`、`develop` 或仓库指定的集成分支，会先创建合规的工作分支，再提交、发布并向指定集成分支打开 PR。

## `/clean_gone`

用于清理远程已删除但本地仍存在的 stale branch。

它会先更新远程分支信息，再检查标记为 `[gone]` 的本地分支。只有分支已合入仓库认可的集成分支、关联 worktree 干净且不是当前分支时，才会使用非强制删除；不满足条件的分支会保留并说明原因。

## 归因

本插件默认使用：

```text
Co-authored-by: Codex <noreply@openai.com>
```

该地址来自 `openai/codex` 仓库中的 Codex baseline git signature。

## 注意

这个插件会触发本地 Git 工作流。使用前请确认当前目录是正确仓库，并在合并 PR 前人工 review。命令不会直接向受保护分支提交或推送，也不会强制删除未合并分支或脏 worktree。
