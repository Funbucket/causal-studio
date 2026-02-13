# Manim Video Pipeline 가이드

새로운 주제로 교육 영상을 제작하는 전체 과정에 대한 가이드입니다.

## 시나리오

**주제**: Instrumental Variables (IV)
**원본**: `iv/iv.ipynb`
**목표**: 5개 Scene으로 구성된 교육 영상 제작

---

## Phase 1: 프로젝트 초기화

### 1.1 디렉토리 구조 생성

```bash
mkdir -p iv/{scripts,audio,final}
```

### 1.2 결과 구조

```
iv/
├── iv.py              # (생성 예정) Manim Scene 클래스
├── iv.ipynb           # (기존) 원본 개념/데이터
├── scene_outline.md   # (생성 예정) Scene 구조
├── scripts/           # (생성 예정) 씬별 스크립트
├── audio/             # (TTS 후 저장) 씬별 오디오
└── final/             # (렌더 후 저장) 최종 영상
```

---

## Phase 2: Scene 구조 설계

### 2.1 사용자 요청

```
"iv.ipynb를 기반으로 scene 구조 설계해줘"
```

#### 3Blue1Brown 영상 참조 (선택)

특정 3Blue1Brown 영상의 연출/리듬을 참고하고 싶다면, video 파일과 caption을 지정할 수 있습니다:

```
"iv.ipynb를 기반으로 scene 구조 설계해줘.
연출은 videos/_2020/covid.py 참고하고,
리듬은 captions/2020/exponential-and-epidemics/english/transcript.txt 참고해줘"
```

**사용 가능한 참조 자료:**

| 유형 | 경로 패턴 | 용도 |
|-----|----------|-----|
| Video (Manim 코드) | `videos/_20XX/{topic}.py` | 애니메이션 연출, 시각적 패턴 |
| Transcript | `captions/20XX/{topic}/english/transcript.txt` | 내레이션 리듬, 문장 길이 |
| Sentence Timings | `captions/20XX/{topic}/english/sentence_timings.json` | Beat 타이밍, 호흡 패턴 |

**예시:**
```
# Bayes 정리 영상 스타일 참조
"captions/2019/bayes-theorem/english/transcript.txt 리듬으로 스크립트 작성해줘"

# 선형대수 시리즈 연출 참조
"videos/_2016/eola/chapter1.py 스타일로 수식 애니메이션 만들어줘"
```

> ⚠️ 참조 영상의 manim 코드는 구버전 API일 수 있음. 연출 아이디어만 참고하고, 실제 코드는 Manim CE 최신 문법으로 작성할 것.

### 2.2 Claude 작업

1. `iv.ipynb` 읽기
2. `references/scene-outline-guide.md` 참조
3. Scene 구조 설계 후 `scene_outline.md` 생성

### 2.3 예상 출력: `iv/scene_outline.md`

```markdown
# IV (Instrumental Variables) Scene 구조

## 영상 요약
관측되지 않는 교란 변수가 있을 때, 도구 변수를 활용해 인과 효과를 추정하는 방법

---

## Scene 01: unobserved_confounding

**핵심 주장**: 관측되지 않은 교란 변수가 있으면 매칭/회귀로도 인과 효과 추정 불가

**Expected Misconception**: 모든 교란 변수를 통제하면 되지 않나?

**Visual Pivot**: 숨겨진(점선) 교란 변수 등장

**Beats**:
1. 교육 → 소득 관계 제시
2. 능력이라는 숨겨진 변수 암시
3. 점선으로 관측 불가능함 표현

---

## Scene 02: iv_intuition

**핵심 주장**: 도구 변수는 치료에만 영향을 주고, 결과에는 치료를 통해서만 영향

**Expected Misconception**: 아무 변수나 도구 변수로 쓸 수 있다

**Visual Pivot**: IV 조건 3가지 시각화 (화살표 구조)

**Beats**:
1. 도구 변수 개념 소개 (징병 추첨)
2. IV → 치료 → 결과 경로만 존재
3. 세 가지 조건 정리

---

## Scene 03: wald_estimator

**핵심 주장**: Wald estimator는 ITT를 compliance rate로 나눈 것

**Expected Misconception**: 단순히 IV와 결과의 관계만 보면 된다

**Visual Pivot**: 분수 형태 수식 + 기하학적 해석

**Beats**:
1. Reduced form (IV → Y) 제시
2. First stage (IV → D) 제시
3. LATE = Reduced form / First stage

---

## Scene 04: late_interpretation

**핵심 주장**: LATE는 complier들의 평균 처치 효과

**Expected Misconception**: LATE는 모든 사람의 평균 효과다

**Visual Pivot**: 4가지 유형 (complier, always-taker 등) 분류

**Beats**:
1. 4가지 유형 소개
2. Complier만 효과 식별 가능함 강조
3. External validity 한계 언급

---

## Scene 05: iv_summary

**핵심 주장**: IV는 강력하지만 조건이 까다롭고 해석에 주의 필요

**Expected Misconception**: IV만 있으면 만사 OK

**Visual Pivot**: IV 조건 체크리스트 + 한계 정리

**Beats**:
1. IV 장점 요약
2. 조건 검증의 어려움
3. LATE의 한계와 적용 범위
```

---

## Phase 3: 스크립트 작성

### 3.1 사용자 요청

```
"scene_outline.md 기반으로 스크립트 작성해줘"
```

### 3.2 Claude 작업

1. `scene_outline.md` 읽기
2. `references/script-writing-guide.md` 참조
3. 씬별 스크립트 파일 생성

### 3.3 예상 출력

#### `iv/scripts/01_unobserved_confounding.txt`
```
교육을 더 받으면 소득이 올라갈까요?
단순히 비교하면 그래 보이지만,
여기엔 숨겨진 변수가 있습니다.
능력이 높은 사람이 교육도 더 받고, 소득도 높죠.
이런 변수를 관측할 수 없다면 어떻게 할까요?
```

#### `iv/scripts/02_iv_intuition.txt`
```
도구 변수를 사용합니다.
베트남전 징병 추첨 번호를 예로 들어볼게요.
추첨 번호는 군 복무에 영향을 주지만,
소득에는 군 복무를 통해서만 영향을 줍니다.
이게 도구 변수의 핵심 아이디어예요.
```

#### `iv/scripts/03_wald_estimator.txt`
```
이제 효과를 계산해봅시다.
추첨 번호와 소득의 관계를 reduced form이라 하고,
추첨 번호와 군 복무의 관계를 first stage라 해요.
둘을 나누면 LATE를 얻습니다.
```

#### `iv/scripts/04_late_interpretation.txt`
```
LATE가 누구의 효과일까요?
사람들은 네 유형으로 나뉩니다.
추첨과 상관없이 복무하는 사람, 안 하는 사람,
그리고 추첨 결과에 따라 결정이 바뀌는 사람.
LATE는 이 마지막 그룹의 효과입니다.
```

#### `iv/scripts/05_iv_summary.txt`
```
정리해볼게요.
도구 변수는 숨겨진 교란이 있을 때 유용해요.
하지만 세 가지 조건을 만족해야 하고,
추정치는 일부 집단에만 적용됩니다.
도구의 타당성을 항상 검토하세요.
```

---

## Phase 4: 오디오 생성 (외부 작업)

### 4.1 TTS 생성

ElevenLabs 또는 Piper로 각 스크립트를 mp3로 변환:

```
iv/audio/
├── 01_unobserved_confounding.mp3  (18.5s)
├── 02_iv_intuition.mp3            (22.3s)
├── 03_wald_estimator.mp3          (19.8s)
├── 04_late_interpretation.mp3     (24.1s)
└── 05_iv_summary.mp3              (20.2s)
```

### 4.2 오디오 길이 확인

```bash
for f in iv/audio/*.mp3; do
  echo -n "$f: "
  ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f"
done
```

---

## Phase 5: Scene 코드 작성

### 5.1 사용자 요청

```
"scene 01 코드 작성해줘"
```

### 5.2 Claude 작업

1. `scripts/01_*.txt` 스크립트 읽기
2. `audio/01_*.mp3` 길이 확인 (18.5s)
3. `references/manim-code-patterns.md` 참조
4. Scene 클래스 작성

### 5.3 예상 출력: `iv/iv.py` (Scene 01)

```python
from manim import *

class Scene01_UnobservedConfounding(Scene):
    """
    Scene 01: 관측되지 않은 교란 변수

    Visual Pivot: 숨겨진(점선) 교란 변수 등장
    Reference: iv.ipynb - "Unobserved Confounding" 섹션

    Beats:
    1. 교육 → 소득 관계 제시
    2. 능력이라는 숨겨진 변수 암시
    3. 점선으로 관측 불가능함 표현
    """

    WAIT_TAIL = 2.0
    RUN_TIME_SCALE = 1.0

    def construct(self):
        # ─── Beat 1: 교육 → 소득 관계 ───
        edu = Text("교육", font_size=36)
        income = Text("소득", font_size=36)
        edu.move_to(LEFT * 2)
        income.move_to(RIGHT * 2)

        arrow = Arrow(edu.get_right(), income.get_left(), buff=0.3)
        question = Text("?", font_size=48, color=YELLOW)
        question.next_to(arrow, UP)

        self.play(FadeIn(edu), FadeIn(income))
        self.play(Create(arrow), FadeIn(question))
        self.wait(0.8)

        # ─── Beat 2: 숨겨진 변수 암시 ───
        ability = Text("능력", font_size=32, color=RED)
        ability.move_to(UP * 2)

        self.play(FadeIn(ability, shift=DOWN))
        self.wait(0.5)

        # ─── Beat 3: 점선 연결 (관측 불가) ───
        dashed_to_edu = DashedLine(
            ability.get_bottom(), edu.get_top(),
            color=RED, dash_length=0.1
        )
        dashed_to_income = DashedLine(
            ability.get_bottom(), income.get_top(),
            color=RED, dash_length=0.1
        )

        self.play(Create(dashed_to_edu), Create(dashed_to_income))

        hidden_label = Text("관측 불가", font_size=24, color=RED)
        hidden_label.next_to(ability, RIGHT)
        self.play(FadeIn(hidden_label))

        self.wait(self.WAIT_TAIL)
```

### 5.4 반복

Scene 02 ~ 05도 동일한 과정으로 작성.

---

## Phase 6: 렌더 + 오디오 싱크

### 6.1 사용자 요청

```
"scene 01 렌더하고 오디오 붙여줘"
```

### 6.2 Claude 작업

1. Manim 렌더

```bash
cd iv && manim -pql iv.py Scene01_UnobservedConfounding
```

2. 렌더된 파일 찾기

```bash
.claude/skills/manim-video-pipeline/scripts/find_latest_render.sh media/videos Scene01
# → media/videos/iv/480p15/Scene01_UnobservedConfounding.mp4
```

3. 길이 비교

```bash
# Video: 16.2s, Audio: 18.5s → 영상이 짧음
```

4. 코드 조정 (WAIT_TAIL 증가)

```python
WAIT_TAIL = 4.3  # 2.0 → 4.3
```

5. 재렌더 후 오디오 합성

```bash
.claude/skills/manim-video-pipeline/scripts/mux_audio.sh \
  media/videos/iv/480p15/Scene01_UnobservedConfounding.mp4 \
  audio/01_unobserved_confounding.mp3 \
  final/01_unobserved_confounding_debug.mp4
```

### 6.3 결과

```
iv/final/01_unobserved_confounding_debug.mp4 (18.5s)
```

---

## Phase 7: 전체 합본

### 7.1 사용자 요청

```
"전체 영상 합쳐줘"
```

### 7.2 Claude 작업

1. 개별 영상 확인

```bash
ls iv/final/*_debug.mp4
# 01_unobserved_confounding_debug.mp4
# 02_iv_intuition_debug.mp4
# 03_wald_estimator_debug.mp4
# 04_late_interpretation_debug.mp4
# 05_iv_summary_debug.mp4
```

2. 합본 생성

```bash
cd iv && ../.claude/skills/manim-video-pipeline/scripts/concat_videos.sh \
  final/ final/iv_full.mp4
```

3. 검증

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 iv/final/iv_full.mp4
# → 104.9s (약 1분 45초)
```

### 7.3 최종 결과

```
iv/final/iv_full.mp4 (104.9s)
```

---

## 전체 워크플로우 요약

| Phase | 사용자 요청 | Claude 참조 | 출력 |
|-------|-----------|------------|------|
| 1 | (초기화) | - | 디렉토리 구조 |
| 2 | "scene 구조 설계해줘" | `scene-outline-guide.md` | `scene_outline.md` |
| 3 | "스크립트 작성해줘" | `script-writing-guide.md` | `scripts/*.txt` |
| 4 | (외부) TTS | - | `audio/*.mp3` |
| 5 | "scene N 코드 작성해줘" | `manim-code-patterns.md` | `{topic}.py` |
| 6 | "scene N 렌더+오디오" | `ffmpeg-recipes.md` | `final/*_debug.mp4` |
| 7 | "전체 합쳐줘" | `ffmpeg-recipes.md` | `final/{topic}_full.mp4` |

---

## 트러블슈팅

### 영상/오디오 길이 불일치

```
Video: 16.2s, Audio: 18.5s (차이: 2.3s)
```

**해결**: `WAIT_TAIL` 증가 또는 Beat 사이 `self.wait()` 추가

### 해상도/프레임레이트 불일치로 합본 실패

```bash
# 재인코딩 옵션 사용
concat_videos.sh final/ final/iv_full.mp4 --reencode
```

### 특정 Scene만 재렌더

```bash
manim -pql iv.py Scene03_WaldEstimator
# 이후 mux_audio.sh로 다시 합성
```
