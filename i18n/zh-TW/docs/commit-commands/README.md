# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](../../../en/docs/commit-commands/README.md) · [繁體中文](README.md) · [日本語](../../../ja/docs/commit-commands/README.md) · [한국어](../../../ko/docs/commit-commands/README.md)

`commit-commands` 將常用 Git 工作流程封裝成三個原生 Codex skill：

```text
$commit
$commit-push-pr
$clean-gone
```

Codex 可以依照明確的自然語言意圖自動選擇 skill；`$skill-name` 用於明確指定。僅完成實作不會自動授權提交、推送、建立 PR 或刪除分支。

## 安裝與啟用

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

安裝或更新後請開啟新的 Codex thread，讓新的 skill metadata 進入會話。

## 自動選擇範例

- 「提交這些改動」可以自動選擇 `commit`。
- 「推送目前分支並建立 PR」可以自動選擇 `commit-push-pr`。
- 「清理已合併的 gone 分支」可以自動選擇 `clean-gone`。
- 「功能已經完成」不會自行觸發 Git 副作用。

## `$commit`

讀取倉庫規範，檢查目前分支、worktree、暫存區和近期提交風格，只暫存與目前任務相關且安全的檔案，然後建立一個本地 commit。

它會略過明顯的憑證、私鑰、環境檔案、依賴目錄、建置產物、快取、日誌和機器專屬檔案。產生的提交會加入：

```text
Co-authored-by: Codex <noreply@openai.com>
```

此 skill 不會推送或建立 PR。

## `$commit-push-pr`

讀取 `AGENTS.md`、`CONTRIBUTING.md` 等倉庫規範，決定基線分支、工作分支、驗證命令和 PR 目標分支。

- 不直接向 `main`、`master`、`dev`、`develop` 或其他受保護分支提交或推送。
- 只有在可以安全保留目前改動時，才建立合規工作分支。
- 不會自行 reset、stash、rebase、force push 或略過驗證。
- 建立一個 commit、發布工作分支，並使用 GitHub CLI 開啟 PR。

此 skill 需要已安裝並登入 GitHub CLI，倉庫也需要設定 `origin` remote。

## `$clean-gone`

先執行 `git fetch --prune`，再檢查 upstream 標記為 `[gone]` 的本地分支。`[gone]` 只代表遠端參照已刪除，不代表本地提交已經合併。

只有候選分支不是目前或受保護分支、已合入倉庫認可的整合分支、關聯 worktree 可讀且乾淨，並通過 Git 非強制刪除檢查時才會刪除。其他候選項都會保留並回報原因。

## 與 Claude 原版的關係

Anthropic 原版提供手動呼叫的 slash commands。本適配保留其工作流程目標並強化安全邊界，同時改用 Codex 原生 skills，支援自然語言隱式選擇和 `$skill-name` 明確呼叫。

## 本機驗證

```bash
python -m unittest discover -s tests
codex plugin list
```
