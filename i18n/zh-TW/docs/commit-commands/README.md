# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](../../../en/docs/commit-commands/README.md) · [繁體中文](README.md) · [日本語](../../../ja/docs/commit-commands/README.md) · [한국어](../../../ko/docs/commit-commands/README.md)

`commit-commands` 將 [Anthropic 官方原版](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) 的三個 slash command 適配為 Codex 原生 skill：

```text
$commit
$commit-push-pr
$clean-gone
```

工作流程步驟以原版為準。Codex 差異包括原生 skill 結構、明確意圖的自動選擇、`$skill-name` 入口，以及透過 `UserPromptSubmit` hook 動態提供目前 Codex 模型與思考強度。

## 安裝

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

安裝或更新後，請先在 `/hooks` 中審查並信任 `commit-commands` hook，再開啟新的 Codex thread。

## 自動選擇範例

- 「提交這些改動」可以選擇 `commit`。
- 「提交、推送並建立 PR」可以選擇 `commit-push-pr`。
- 「清理所有 gone 分支」可以選擇 `clean-gone`。
- 「功能已完成」不會自行觸發 Git 副作用。

## `$commit`

檢查 `git status`、`git diff HEAD`、目前分支與最近十筆提交，暫存目前改動並建立一個 commit，加入：

```text
Generated with [Codex](https://chatgpt.com/codex)
Model: <active-model-slug> <active-reasoning-effort>

Co-authored-by: Codex <noreply@openai.com>
```

Codex 會直接提供目前模型 slug，但現行 hook schema 不提供思考強度。插件會以目前 `turn_id` 與模型精確比對 `transcript_path` 尾端的 `turn_context`；若失敗，只有使用者設定指向相同模型時才回退到 `model_reasoning_effort`。解析器只提取 attribution 欄位，不複製或保存 prompt。因 transcript 格式並不穩定，失敗時只省略強度後綴；hook 未受信任或模型 context 缺失時，skill 才會在 stage 或 commit 前停止。

不會推送、建立 PR 或在沒有改動時建立空 commit。

## `$commit-push-pr`

檢查目前狀態、diff 與分支。只有目前分支恰好是 `main` 時才建立新分支，接著建立一個 commit、推送到 `origin`，並以 `gh pr create` 建立 PR。

此 skill 需要明確的 PR 意圖。與原版一樣，它不支援沒有新 commit 也發布 PR，也不會為 `main` 以外的不合規分支自動建立替代分支。

需要已安裝並登入 GitHub CLI，倉庫也必須有 `origin` remote。

## `$clean-gone`

使用 `git branch -v` 與 `git worktree list` 尋找 `[gone]` 分支。每個候選項都會先以 `git worktree remove --force` 強制移除關聯的非主 worktree，再以 `git branch -D` 強制刪除分支。

這是與原版一致的破壞性行為：不會 fetch、驗證 merge、檢查 worktree 是否乾淨、保護 ignored 檔案或套用整合分支規則。執行前請先檢查倉庫狀態。

## 本機驗證

```bash
python -m py_compile plugins/commit-commands/hooks/model_context.py
'{"hook_event_name":"UserPromptSubmit","model":"gpt-5.6-sol","effort":"xhigh"}' | python plugins/commit-commands/hooks/model_context.py
python -m unittest discover -s tests
codex plugin list
```
