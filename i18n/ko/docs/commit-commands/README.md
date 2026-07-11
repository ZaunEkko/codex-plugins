# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](../../../en/docs/commit-commands/README.md) · [繁體中文](../../../zh-TW/docs/commit-commands/README.md) · [日本語](../../../ja/docs/commit-commands/README.md) · [한국어](README.md)

`commit-commands` 는 [Anthropic 공식 원본](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) 의 세 slash command 를 Codex 네이티브 skill 로 적용합니다.

```text
$commit
$commit-push-pr
$clean-gone
```

워크플로 단계는 원본을 따릅니다. Codex 전용 차이에는 네이티브 skill 구조, 명확한 의도에 따른 자동 선택, `$skill-name` 호출, 현재 Codex 모델과 reasoning effort 를 동적으로 제공하는 `UserPromptSubmit` hook 이 포함됩니다.

## 설치

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

설치 또는 업데이트 후 `/hooks` 에서 `commit-commands` hook 을 검토하고 trust 한 다음 새 Codex thread 를 여세요.

## 자동 선택 예시

- "이 변경을 commit 해줘"는 `commit` 을 선택할 수 있습니다.
- "commit, push 하고 PR 을 만들어줘"는 `commit-push-pr` 을 선택할 수 있습니다.
- "gone 브랜치를 모두 정리해줘"는 `clean-gone` 을 선택할 수 있습니다.
- "구현이 끝났다"는 말만으로 Git 부작용을 실행하지 않습니다.

## `$commit`

`git status`, `git diff HEAD`, 현재 브랜치, 최근 commit 10개를 확인하고 현재 변경을 stage 한 뒤 하나의 commit 을 만듭니다.

```text
Generated with [Codex](https://chatgpt.com/codex)
Model: <active-model-slug> <active-reasoning-effort>

Co-authored-by: Codex <noreply@openai.com>
```

Codex 는 현재 모델 slug 를 직접 전달하지만 현행 hook schema 는 reasoning effort 를 제공하지 않습니다. 플러그인은 hook 이 향후 직접 제공하는 effort 또는 현재 `turn_id` 와 모델이 정확히 일치하는 `transcript_path` 끝의 `turn_context` 만 사용합니다. CLI, project, profile, runtime override 로 파일 값이 오래될 수 있으므로 사용자 설정에서 현재 effort 를 추정하지 않습니다. attribution 필드만 추출하며 prompt 를 복사하거나 저장하지 않고 Python 3.11 의 `tomllib` 에 의존하지 않습니다. transcript 형식이 안정적이지 않으므로 실패하면 effort suffix 만 생략합니다. hook 이 trust 되지 않았거나 모델 context 가 없으면 stage 또는 commit 전에 중지합니다.

push 또는 PR 생성을 하지 않으며 변경이 없으면 빈 commit 도 만들지 않습니다.

## `$commit-push-pr`

현재 status, diff, branch 와 대상 base 대비 commit 을 확인합니다. worktree 에 변경이 있으면 현재 브랜치가 정확히 `main` 일 때만 새 브랜치를 만들고 모델 attribution 이 포함된 commit 하나를 생성합니다. worktree 가 clean 이더라도 대상 base 에 없는 기존 commit 이 있으면 해당 commit 을 그대로 게시합니다. 두 경로 모두 `origin` 에 push 합니다.

skill 은 `gh pr create` 를 직접 호출하지 않습니다. 전체 PR body 를 번들 `scripts/create_pr_with_attribution.py` wrapper 에 전달합니다. wrapper 는 footer 를 추가하고 `--body-file` 로 PR 을 만든 뒤 body 를 다시 읽으며, 필요하면 한 번 수정합니다. 마지막 비어 있지 않은 줄이 정확히 다음과 같을 때만 URL 을 반환합니다.

```text
Generated with [Codex](https://chatgpt.com/codex)
```

명시적인 PR 의도가 필요합니다. worktree 변경도 대상 base 에 없는 commit 도 없으면 빈 commit 이나 빈 PR 을 만들지 않습니다. `main` 이외의 브랜치를 정책에 맞춰 자동 전환하지도 않습니다. 이 흐름을 확실히 사용하려면 `$commit-push-pr` 를 명시적으로 호출하세요.

GitHub CLI 설치와 로그인, 그리고 `origin` remote 가 필요합니다.

## `$clean-gone`

`git branch -v` 와 `git worktree list` 로 `[gone]` 브랜치를 찾습니다. 각 후보의 연결된 non-main worktree 를 `git worktree remove --force` 로 강제 제거하고 `git branch -D` 로 브랜치를 강제 삭제합니다.

이는 원본과 일치하는 파괴적 동작입니다. fetch, merge 검증, worktree clean 확인, ignored 파일 보호, 통합 브랜치 규칙을 추가하지 않습니다. 실행 전에 저장소 상태를 확인하세요.

## 로컬 검증

```bash
python -m py_compile plugins/commit-commands/hooks/model_context.py
'{"hook_event_name":"UserPromptSubmit","model":"gpt-5.6-sol","effort":"xhigh"}' | python plugins/commit-commands/hooks/model_context.py
python -m unittest discover -s tests
codex plugin list
```
