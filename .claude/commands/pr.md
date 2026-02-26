---
description: Pull Request 생성 (auto assign 포함)
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Bash(git push:*), Bash(gh pr:*)
---

현재 브랜치의 변경사항을 분석하고 Pull Request를 생성하세요.

## 작업 순서

1. `git status`로 커밋되지 않은 변경사항 확인
2. `git branch --show-current`로 현재 브랜치 확인
3. `git log main..HEAD --oneline`으로 PR에 포함될 커밋 확인
4. `git diff main...HEAD`로 전체 변경사항 분석
5. 리모트에 푸시되지 않았다면 `git push -u origin <branch>` 실행
6. PR 제목과 본문 작성 후 생성

## PR 생성 명령어

```bash
gh pr create --title "제목" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points>

## Test plan
- [ ] 테스트 항목 1
- [ ] 테스트 항목 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" --assignee @me
```

## PR 제목 규칙

커밋 메시지와 동일한 prefix 사용:
- `feat: 새로운 기능 설명`
- `fix: 버그 수정 설명`
- `docs: 문서 수정 설명`
- `refactor: 리팩토링 설명`
- `chore: 기타 작업 설명`

## 주의사항

- 커밋되지 않은 변경사항이 있으면 먼저 커밋 안내
- base 브랜치는 기본적으로 `main` 사용
- `--assignee @me`로 자동 할당
- PR 생성 후 URL 반환
