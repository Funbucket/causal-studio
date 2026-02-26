# Causal Studio

인과추론 교육용 코드북과 Manim 영상 제작을 함께 운영하는 저장소입니다.

## 핵심 구조

```text
causal_video/
├── book/                              # Jupyter Book 소스
│   ├── myst.yml
│   ├── intro.md
│   └── matching/
│       ├── matching.ipynb
│       └── assets/
├── videos/                            # 영상 제작 워크스페이스
│   └── matching/
│       ├── src/
│       │   ├── matching.py
│       │   ├── scene_outline.md
│       │   └── scripts/
│       └── build/
│           ├── audio/
│           ├── render/
│           └── final/
├── .claude/skills/                    # Claude 스킬 원본
├── .codex/skills/                     # Codex REPO 스코프 스킬
├── prompts/design/                    # 설계 문서/프롬프트 아카이브
├── .github/workflows/deploy-book.yml  # Book 배포 워크플로우
└── requirements.txt
```

## 빠른 시작

### 1) 의존성 설치

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) 로컬 Book 서버 실행

Codex 기준:

```bash
$book-serve
```

Claude 기준:

```bash
/book-serve
```

자연어 대안:
- Codex: `book 로컬 서버 실행해줘`
- Claude: `book 로컬 서버 실행해줘`

직접 실행:

```bash
cd book
source ../.venv/bin/activate
jupyter-book start --port 3000
```

### 3) Book 빌드

```bash
cd book
source ../.venv/bin/activate
jupyter-book build --html
open _build/html/index.html
```

## 영상 제작 (Skill-First)

직접 쉘 명령보다 `manim-video-pipeline` 스킬 호출을 기본으로 사용합니다.

Codex 기준:
```bash
$manim-video-pipeline
```

Claude 기준:

```bash
/manim-video-pipeline
```

자연어 대안:
- Codex: `manim 영상 파이프라인 진행해줘`
- Claude: `manim 영상 파이프라인 진행해줘`

자연어 + 인자 대안:
- Codex: `matching 토픽으로 진행하고 ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json 참고해서 scene 구조 설계해줘`
- Claude: `matching 토픽으로 진행하고 ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json 참고해서 scene 구조 설계해줘`

3b1b 참고 인자 포함:

Codex 기준:
```bash
$manim-video-pipeline topic=matching ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json
```

Claude 기준:
```bash
/manim-video-pipeline topic=matching ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json
```

## 사용 스킬

| 스킬 | 용도 |
|---|---|
| `book-serve` | Jupyter Book 로컬 서버 실행 |
| `git-commit` | 변경 분석 및 커밋 |
| `git-pr` | PR 생성 워크플로우 |
| `manim-video-pipeline` | scene 설계, 스크립트 작성, 렌더/합성/합본 |
| `pip-install` | `.venv` 설치 + `requirements.txt` 동기화 |

## 참고

- 설계/가이드 문서는 `prompts/design/`에 보관되어 있습니다.
- `3b1b/`, `videos/*/build/`, `book/_build/`는 로컬 참조/산출물 영역입니다.

## 라이선스

MIT
