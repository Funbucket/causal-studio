---
name: video-assets-setup
description: Set up local-only video reference assets for this repo by cloning or updating 3Blue1Brown source files and Tabler Icons into ignored paths. Use when a new machine clones the repo, when 3b1b references are missing, or when videos/assets/tabler-icons is absent.
---

# Video Assets Setup

이 저장소의 영상 제작은 git에 포함하지 않는 로컬 참조 자산에 의존한다.

준비 대상:
- `3b1b/`
- `videos/assets/tabler-icons/`

사용 저장소:
- 3Blue1Brown videos: `https://github.com/3b1b/videos.git`
- Tabler Icons: `https://github.com/tabler/tabler-icons.git`

기본 원칙:
- 두 경로는 로컬 전용이다.
- 새 환경에서는 먼저 이 스킬로 자산을 준비한 뒤 `manim-video-pipeline`을 사용한다.
- 이미 디렉터리가 있으면 clone 대신 `git pull --ff-only`로 갱신한다.

## 실행

```bash
bash .codex/skills/video-assets-setup/scripts/setup_video_assets.sh
```

## 결과

- `3b1b/` 에 3Blue1Brown 참조 코드가 준비된다.
- `videos/assets/tabler-icons/` 에 공용 SVG 아이콘 라이브러리가 준비된다.

## 확인

```bash
test -f 3b1b/videos/_2020/covid.py
test -f videos/assets/tabler-icons/icons/outline/device-tablet.svg
```

두 파일이 있으면 정상이다.
