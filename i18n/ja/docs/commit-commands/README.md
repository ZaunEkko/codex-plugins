# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](../../../en/docs/commit-commands/README.md) · [繁體中文](../../../zh-TW/docs/commit-commands/README.md) · [日本語](README.md) · [한국어](../../../ko/docs/commit-commands/README.md)

`commit-commands` は、よく使う Git ワークフローを 3 つの Codex ネイティブ skill として提供します。

```text
$commit
$commit-push-pr
$clean-gone
```

Codex は明確な自然言語の意図から skill を自動選択できます。特定の skill を明示的に指定する場合は `$skill-name` を使います。実装が完了しただけでは、commit、push、PR 作成、ブランチ削除は許可されません。

## インストールと有効化

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

インストールまたは更新後は、新しい Codex thread を開いて skill metadata を読み込んでください。

## 自動選択の例

- 「この変更を commit して」で `commit` を選択できます。
- 「ブランチを push して PR を作成して」で `commit-push-pr` を選択できます。
- 「merge 済みの gone ブランチを整理して」で `clean-gone` を選択できます。
- 「実装が完了した」だけでは Git の副作用を実行しません。

## `$commit`

リポジトリ規約、現在のブランチ、worktree、ステージ済み変更、最近の commit 形式を確認し、現在の作業に関係する安全なファイルだけをステージして 1 つのローカル commit を作成します。

明らかな認証情報、秘密鍵、環境ファイル、依存関係ディレクトリ、ビルド成果物、キャッシュ、ログ、マシン固有ファイルは除外します。生成された commit には次の表記が追加されます。

```text
Co-authored-by: Codex <noreply@openai.com>
```

この skill は push や PR 作成を行いません。

## `$commit-push-pr`

`AGENTS.md` や `CONTRIBUTING.md` などの規約を読み、基点ブランチ、作業ブランチ、検証コマンド、PR の対象ブランチを決定します。

- `main`、`master`、`dev`、`develop`、その他の保護ブランチへ直接 commit や push を行いません。
- 現在の変更を安全に保持できる場合だけ、規約に合う作業ブランチを作成します。
- reset、stash、rebase、force push、検証の回避を自動実行しません。
- 1 つの commit を作成し、作業ブランチを公開して GitHub CLI で PR を開きます。
- ユーザーが PR の作成または開始を明示的に依頼した場合、または完全な commit-push-PR フローを明示的に依頼した場合だけ選択されます。「commit して push」や「ブランチを公開」だけでは PR 作成を許可しません。

この skill には、インストール済みかつログイン済みの GitHub CLI と `origin` remote が必要です。

## `$clean-gone`

`git fetch --prune` を実行し、upstream が `[gone]` のローカルブランチを確認します。`[gone]` はリモート参照の削除だけを示し、ローカル commit の merge を保証しません。

関連 worktree は、`git status --short --ignored=matching` が tracked、untracked、ignored のパスを一つも報告しない場合だけ削除します。ブランチの非強制削除は、merge 証明に使った統合 ref と `HEAD` が一致する worktree からだけ実行し、その worktree がない場合や Git が拒否した場合は理由とともに候補を保持します。

## Claude 原版との関係

Anthropic 原版は手動で呼び出す slash commands を提供します。この適配はワークフローの意図を維持して安全制約を強化し、Codex ネイティブ skills による自然言語の暗黙選択と `$skill-name` の明示呼び出しに変更しています。

## ローカル検証

```bash
python -m unittest discover -s tests
codex plugin list
```
