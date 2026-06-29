# commit-commands

[简体中文](../../../../docs/commit-commands/README.md) · [English](../../../en/docs/commit-commands/README.md) · [繁體中文](../../../zh-TW/docs/commit-commands/README.md) · [日本語](../../../ja/docs/commit-commands/README.md) · [한국어](README.md)

`commit-commands` 는 자주 사용하는 Git 워크플로를 세 개의 Codex 네이티브 skill 로 제공합니다.

```text
$commit
$commit-push-pr
$clean-gone
```

Codex 는 명확한 자연어 의도에 따라 skill 을 자동 선택할 수 있습니다. 특정 skill 을 명시적으로 선택하려면 `$skill-name` 을 사용합니다. 구현이 끝났다는 사실만으로 commit, push, PR 생성 또는 브랜치 삭제가 허용되지는 않습니다.

## 설치 및 활성화

```bash
codex plugin marketplace add ZaunEkko/codex-plugins
codex plugin add commit-commands@zaunekko
```

설치하거나 업데이트한 뒤에는 새 Codex thread 를 열어 새로운 skill metadata 를 불러오세요.

## 자동 선택 예시

- "이 변경을 commit 해줘"는 `commit` 을 선택할 수 있습니다.
- "현재 브랜치를 push 하고 PR 을 만들어줘"는 `commit-push-pr` 을 선택할 수 있습니다.
- "merge 된 gone 브랜치를 정리해줘"는 `clean-gone` 을 선택할 수 있습니다.
- "구현이 끝났다"는 말만으로 Git 부작용을 실행하지 않습니다.

## `$commit`

저장소 규칙, 현재 브랜치, worktree, stage 된 변경, 최근 commit 형식을 확인하고 현재 작업과 관련된 안전한 파일만 stage 한 뒤 하나의 로컬 commit 을 생성합니다.

명백한 자격 증명, 개인 키, 환경 파일, 의존성 디렉터리, 빌드 결과물, 캐시, 로그, 머신 전용 파일은 제외합니다. 생성된 commit 에는 다음 표기가 추가됩니다.

```text
Co-authored-by: Codex <noreply@openai.com>
```

이 skill 은 push 하거나 PR 을 만들지 않습니다.

## `$commit-push-pr`

`AGENTS.md`, `CONTRIBUTING.md` 같은 저장소 규칙을 읽고 기준 브랜치, 작업 브랜치, 검증 명령, PR 대상 브랜치를 결정합니다.

- `main`, `master`, `dev`, `develop` 또는 다른 보호 브랜치에 직접 commit 하거나 push 하지 않습니다.
- 현재 변경을 안전하게 보존할 수 있을 때만 규칙에 맞는 작업 브랜치를 생성합니다.
- reset, stash, rebase, force push 또는 검증 우회를 자동 실행하지 않습니다.
- 하나의 commit 을 만들고 작업 브랜치를 게시한 뒤 GitHub CLI 로 PR 을 엽니다.

이 skill 을 사용하려면 GitHub CLI 가 설치되고 로그인되어 있어야 하며 저장소에 `origin` remote 가 필요합니다.

## `$clean-gone`

`git fetch --prune` 을 실행하고 upstream 이 `[gone]` 인 로컬 브랜치를 확인합니다. `[gone]` 은 원격 참조가 삭제되었다는 뜻일 뿐 로컬 commit 이 merge 되었다는 증거는 아닙니다.

현재 또는 보호 브랜치가 아니고, 승인된 통합 브랜치에 merge 되었으며, 연결된 worktree 를 읽을 수 있고 clean 하며, Git 의 비강제 삭제 검사를 통과한 후보만 삭제합니다. 나머지 후보는 이유와 함께 보존합니다.

## Claude 원본과의 관계

Anthropic 원본은 수동으로 호출하는 slash commands 를 제공합니다. 이 적응은 워크플로 의도를 유지하고 안전 제한을 강화하면서 Codex 네이티브 skills 의 자연어 암시적 선택과 `$skill-name` 명시적 호출을 사용합니다.

## 로컬 검증

```bash
python -m unittest discover -s tests
codex plugin list
```
