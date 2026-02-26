# Manim Video Pipeline

`manim-video-pipeline` 스킬을 사용해 영상 제작 파이프라인을 수행한다.

## 호출 형식

```bash
/manim-video-pipeline topic=<topic> [ref_video=<path>] [ref_transcript=<path>] [ref_sentence_timings=<path>]
```

예시:

```bash
/manim-video-pipeline topic=matching ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json
```

자연어 예시:

```text
matching 토픽으로 진행하고 ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json 참고해서 scene 구조 설계해줘
```

## 실행 규칙

1. `.claude/skills/manim-video-pipeline/SKILL.md`를 먼저 읽는다.
2. 필요한 `references/`만 선택해서 읽는다.
3. 가능한 경우 `scripts/`를 우선 사용한다.
4. `ref_video`, `ref_transcript`, `ref_sentence_timings`가 주어지면 해당 파일을 우선 참조한다.
5. 출력 경로는 아래 규칙을 따른다.

```text
videos/{topic}/src/
videos/{topic}/build/audio/
videos/{topic}/build/render/
videos/{topic}/build/final/
```
