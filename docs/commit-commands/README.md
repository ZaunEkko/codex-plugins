# commit-commands

[简体中文](README.md) · [English](../../i18n/en/docs/commit-commands/README.md) · [繁體中文](../../i18n/zh-TW/docs/commit-commands/README.md) · [日本語](../../i18n/ja/docs/commit-commands/README.md) · [한국어](../../i18n/ko/docs/commit-commands/README.md)

`commit-commands` 把常用 Git 工作流封装成三个原生 Codex skill：

```text
$commit
$commit-push-pr
$clean-gone
```

Codex 可以根据明确的自然语言意图自动选择 skill；`$skill-name` 用于显式强制调用。仅仅完成实现不会自动授权提交、推送、创建 PR 或删除分支。

## 安装与启用

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

安装或更新后请新开 Codex thread，使新的 skill 元数据进入会话。

## 自动选择示例

- “提交这些改动”可以自动选择 `commit`。
- “推送当前分支并创建 PR”可以自动选择 `commit-push-pr`。
- “清理已经合并的 gone 分支”可以自动选择 `clean-gone`。
- “功能已经完成”不会自行触发任何 Git 副作用。

## `$commit`

检查仓库规范、当前分支、工作区、暂存区和近期提交风格，只暂存与当前任务相关且安全的文件，然后创建一个本地 commit。

它会跳过明显的凭据、私钥、环境文件、依赖目录、构建产物、缓存、日志和机器专属文件。生成的提交会追加：

```text
Co-authored-by: Codex <noreply@openai.com>
```

该 skill 不会推送或创建 PR。

## `$commit-push-pr`

读取 `AGENTS.md`、`CONTRIBUTING.md` 等仓库规范，确定基线分支、工作分支名称、验证命令和 PR 目标分支。

- 不直接向 `main`、`master`、`dev`、`develop` 或仓库指定的受保护分支提交或推送。
- 当前分支不合规时，只在能够安全保留改动的情况下创建合规工作分支。
- 不会自行 reset、stash、rebase、force push 或绕过验证。
- 创建一个 commit、发布工作分支，并使用 GitHub CLI 打开 PR。
- 只有用户明确要求创建或打开 PR，或明确要求完整 commit-push-PR 流程时才会触发；仅“提交并推送”或“发布分支”不代表允许创建 PR。

该 skill 需要已经安装并登录 GitHub CLI，仓库还需要配置 `origin` remote。

## `$clean-gone`

先运行 `git fetch --prune`，再检查 upstream 标记为 `[gone]` 的本地分支。`[gone]` 只表示远程引用已删除，不代表本地提交已经合并。

只有候选分支不是当前或受保护分支、已经合入仓库认可的集成分支，并且关联 worktree 的 `git status --short --ignored=matching` 没有报告 tracked、untracked 或 ignored 路径时，才会移除 worktree。

分支删除必须从 `HEAD` 等于上述已验证集成 ref 的 worktree 执行非强制 `git branch -d`。缺少该 worktree 或 Git 拒绝删除时，会保留候选项并报告原因，不会改用无关的当前分支或强制删除。

## 与 Claude 原版的关系

Anthropic 原版提供手动调用的 slash commands。本适配保留其工作流目标并强化安全边界，同时改用 Codex 原生 skills，以支持自然语言隐式选择和 `$skill-name` 显式调用。

## 本地验证

```bash
python -m unittest discover -s tests
codex plugin list
```
