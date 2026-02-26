---
name: manim-video-pipeline
description: |
  Manim Community Edition 기반 교육 영상 제작 파이프라인.
  ipynb/개념 문서를 Scene 구조로 설계하고, 내레이션 스크립트 작성,
  Manim 코드 생성, 오디오 싱크, 최종 합본까지 전 과정을 지원한다.

  트리거: "manim 영상", "scene 설계", "scene 구조", "스크립트 작성",
  "scene 렌더", "영상 합치기", "오디오 싱크", "debug 영상", "full video"
---

# Manim Video Pipeline

Manim CE 기반 교육 영상 제작을 위한 end-to-end 워크플로우.

## 프로젝트 구조

```text
videos/{topic}/
├── src/
│   ├── {topic}.py              # Manim Scene 클래스 모음
│   ├── scene_outline.md        # Scene 구조 설계
│   └── scripts/
│       ├── 01_{scene_name}.txt # 씬별 내레이션 스크립트
│       └── ...
└── build/
    ├── audio/
    │   ├── 01_{scene_name}.mp3 # 씬별 오디오 (TTS 생성)
    │   └── ...
    ├── render/                 # Manim 렌더 캐시/출력
    └── final/
        ├── 01_{scene_name}_debug.mp4  # 디버그용 개별 영상
        └── {topic}_full.mp4           # 최종 합본
```

## 관련 코드북 노트북

```text
book/{topic}/{topic}.ipynb
```

- 영상의 원본 콘텐츠 (개념, 수식, 코드)
- 영상 완성 후 YouTube ID를 이 노트북에 임베드

## 3Blue1Brown 참고 입력 (선택)

아래 인자를 함께 전달하면 3b1b 스타일 참조를 명시적으로 반영한다.

- `topic`: 작업 토픽명 (예: `matching`, `iv`)
- `ref_video`: 3b1b Manim 코드 경로 (예: `3b1b/videos/_2020/covid.py`)
- `ref_transcript`: 3b1b 자막 경로 (예: `3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt`)
- `ref_sentence_timings`: 문장 타이밍 경로 (예: `3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json`)

Codex 호출 예:
```bash
$manim-video-pipeline topic=iv ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json
```

Claude 호출 예:
```bash
/manim-video-pipeline topic=iv ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json
```

자연어 호출 예:

```text
iv 토픽으로 진행하고 ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json 참고해서 scene 구조 설계해줘
```

## 워크플로우 단계

### 1. Scene 구조 설계
코드북 노트북의 논리 전개를 영상에 적합한 Scene 단위로 재구성.
→ `references/scene-outline-guide.md` 참조

### 2. 스크립트 작성
Scene 구조 기반 내레이션 스크립트 생성 (한국어).
→ `references/script-writing-guide.md` 참조

### 3. 오디오 생성 (외부)
스크립트를 TTS(ElevenLabs/Piper)로 mp3 변환.
- 출력: `videos/{topic}/build/audio/{NN}_{scene_name}.mp3`

### 4. Scene 코드 작성
스크립트+오디오 길이에 맞춰 Manim Scene 클래스 구현.
→ `references/manim-code-patterns.md` 참조

### 5. 렌더 + 오디오 싱크
개별 Scene 렌더 후 오디오 합성.
→ `references/ffmpeg-recipes.md` 참조

### 6. 전체 합본
개별 debug mp4들을 순서대로 합쳐 최종 영상 생성.
→ `references/ffmpeg-recipes.md` 참조

### 7. YouTube 업로드 + 노트북 임베드
완성 영상을 YouTube에 업로드하고, `book/{topic}/{topic}.ipynb`에 임베드.

## 빠른 명령어

### Scene 렌더
```bash
cd videos/{topic} && manim -pql src/{topic}.py Scene{NN}_{ClassName}
```

### 오디오 합성
```bash
../../.claude/skills/manim-video-pipeline/scripts/mux_audio.sh {video.mp4} {audio.mp3} {output.mp4}
```

### 전체 합본
```bash
cd videos/{topic} && ../../.claude/skills/manim-video-pipeline/scripts/concat_videos.sh build/final/ build/final/{topic}_full.mp4
```

## 단계별 상세 가이드

각 단계의 상세 지침은 references/ 하위 파일 참조:

| 작업 | 참조 파일 |
|-----|----------|
| Scene 구조 설계 | `references/scene-outline-guide.md` |
| 스크립트 작성 | `references/script-writing-guide.md` |
| Manim 코드 작성 | `references/manim-code-patterns.md` |
| 렌더/합성/합본 | `references/ffmpeg-recipes.md` |
