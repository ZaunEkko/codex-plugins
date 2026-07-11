# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](../../../en/docs/commit-commands/README.md) · [繁體中文](../../../zh-TW/docs/commit-commands/README.md) · [日本語](README.md) · [한국어](../../../ko/docs/commit-commands/README.md)

`commit-commands` は [Anthropic 公式原版](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) の 3 つの slash command を Codex ネイティブ skill に適配します。

```text
$commit
$commit-push-pr
$clean-gone
```

ワークフロー手順は原版に従います。Codex 固有の差分には、ネイティブ skill 構造、明示的な意図による自動選択、`$skill-name` 呼び出し、および現在の Codex モデルと reasoning effort を動的に渡す `UserPromptSubmit` hook が含まれます。

## インストール

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

インストールまたは更新後は、`/hooks` で `commit-commands` hook を確認して trust し、新しい Codex thread を開いてください。

## 自動選択の例

- 「この変更を commit して」で `commit` を選択できます。
- 「commit、push、PR 作成をして」で `commit-push-pr` を選択できます。
- 「gone ブランチをすべて整理して」で `clean-gone` を選択できます。
- 「実装が完了した」だけでは Git の副作用を実行しません。

## `$commit`

`git status`、`git diff HEAD`、現在のブランチ、最近 10 件の commit を確認し、現在の変更を stage して 1 つの commit を作成します。

```text
Generated with [Codex](https://chatgpt.com/codex)
Model: <active-model-slug> <active-reasoning-effort>

Co-authored-by: Codex <noreply@openai.com>
```

Codex は現在のモデル slug を直接渡しますが、現行 hook schema は reasoning effort を公開しません。プラグインは hook が将来直接提供する effort、または現在の `turn_id` とモデルに一致する `transcript_path` 末尾の `turn_context` だけを使用します。CLI、project、profile、runtime override によりファイル値が古くなる可能性があるため、ユーザー設定から現在の effort を推測しません。attribution フィールドだけを抽出し、prompt はコピーも保存もせず、Python 3.11 の `tomllib` に依存しません。transcript 形式は不安定なため、失敗時は effort suffix のみ省略します。hook が trust されていない、またはモデル context がない場合は stage や commit の前に停止します。

push や PR 作成は行わず、変更がない場合は空 commit も作成しません。

## `$commit-push-pr`

現在の status、diff、branch、および対象 base との差分 commit を確認します。worktree に変更がある場合は、現在のブランチが正確に `main` のときだけ新しいブランチを作り、モデル attribution 付きの commit を 1 つ作成します。worktree が clean でも対象 base にない既存 commit がある場合は、その commit をそのまま公開します。どちらも `origin` へ push します。

skill は `gh pr create` を直接呼び出しません。完全な PR body を同梱の `scripts/create_pr_with_attribution.py` wrapper に渡します。wrapper は GitHub.com と GitHub Enterprise の PR URL を受け入れ、footer を追加し、`--body-file` で PR を作成して body を再取得し、必要なら一度修復します。最後の空でない行が次の文字列だと確認できた場合だけ URL を返します。

```text
Generated with [Codex](https://chatgpt.com/codex)
```

明示的な PR 意図が必要です。worktree の変更も対象 base にない commit もない場合、空 commit や空 PR は作成しません。`main` 以外のブランチをポリシーに合わせて自動移行する処理もありません。このフローを確実に使うには `$commit-push-pr` を明示的に呼び出してください。

GitHub CLI のインストールとログイン、および `origin` remote が必要です。

## `$clean-gone`

`git branch -v` と `git worktree list` で `[gone]` ブランチを探します。各候補について、関連する非 main worktree を `git worktree remove --force` で強制削除し、続けて `git branch -D` でブランチを強制削除します。

これは原版に合わせた破壊的な動作です。fetch、merge 検証、worktree の clean 確認、ignored ファイルの保護、統合ブランチ規則は追加しません。実行前にリポジトリ状態を確認してください。

## ローカル検証

```bash
python -m py_compile plugins/commit-commands/hooks/model_context.py
'{"hook_event_name":"UserPromptSubmit","model":"gpt-5.6-sol","effort":"xhigh"}' | python plugins/commit-commands/hooks/model_context.py
python -m unittest discover -s tests
codex plugin list
```
