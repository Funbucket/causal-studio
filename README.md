# Animated Causality

3Blue1Brown-style animated explanations of causal inference.

## 프로젝트 구조

```
causal_video/
├── .claude/skills/          # Claude Code 스킬
│   ├── commit-planner/      # 커밋 계획 작성
│   ├── skill-creator/       # 스킬 생성 가이드
│   └── manim-video-pipeline/ # Manim 영상 제작 파이프라인
├── docs/                    # 문서
│   └── generate-video-guide.md
├── matching/                # Matching Estimator 영상
│   ├── matching.py          # Manim Scene 코드
│   ├── matching.ipynb       # 원본 개념/데이터
│   ├── scene_outline.md     # Scene 구조 설계
│   └── scripts/             # 내레이션 스크립트
├── videos/                  # (별도 clone) 3Blue1Brown Manim 코드
└── captions/                # (별도 clone) 3Blue1Brown 캡션
```

## 시작하기

### 1. 저장소 클론

```bash
git clone https://github.com/Funbucket/animated-causality.git
cd animated-causality
```

### 2. 참조 자료 설정 (선택)

3Blue1Brown 영상의 연출/리듬을 참고하려면, 아래 저장소를 클론하세요:

```bash
# Manim 코드 (연출 참고용)
git clone https://github.com/3b1b/videos.git

# 캡션/트랜스크립트 (리듬 참고용)
git clone https://github.com/3b1b/captions.git
```

> ⚠️ 참조 영상의 manim 코드는 구버전 API입니다. 연출 아이디어만 참고하고, 실제 코드는 Manim CE 최신 문법으로 작성하세요.

### 3. 의존성 설치

```bash
# Manim Community Edition
pip install manim

# FFmpeg (영상 합성용)
brew install ffmpeg  # macOS
```

## 영상 제작 워크플로우

자세한 가이드는 [docs/generate-video-guide.md](docs/generate-video-guide.md) 참조.

### 빠른 시작

```bash
# 1. 프로젝트 디렉토리 생성
mkdir -p {topic}/{scripts,audio,final}

# 2. Scene 구조 설계
# Claude: "{topic}.ipynb 기반으로 scene 구조 설계해줘"

# 3. 스크립트 작성
# Claude: "scene_outline.md 기반으로 스크립트 작성해줘"

# 4. 오디오 생성 (TTS)
# ElevenLabs 또는 Piper로 scripts/*.txt → audio/*.mp3

# 5. Scene 코드 작성 & 렌더
# Claude: "scene 01 코드 작성해줘"
manim -pql {topic}.py Scene01_{Name}

# 6. 오디오 합성
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest output.mp4

# 7. 전체 합본
# Claude: "전체 영상 합쳐줘"
```

## Claude Code 스킬

이 프로젝트는 Claude Code 스킬을 활용합니다:

| 스킬 | 트리거 | 용도 |
|-----|--------|-----|
| `manim-video-pipeline` | "scene 설계", "스크립트 작성", "렌더" | 영상 제작 전 과정 |
| `commit-planner` | "커밋 계획" | git 변경사항 정리 |

## 완성된 영상

### Matching Estimator
- **주제**: 매칭을 통한 인과 효과 추정
- **Scene 수**: 10개
- **총 길이**: 약 3분 16초

## 라이선스

MIT License
