# Manim Code Patterns

Manim Community Edition Scene 작성을 위한 패턴과 규칙.

기본 원칙:
- 현재 Scene 하나만 먼저 완성한다.
- 사용자가 debug 결과를 확인하기 전에는 뒤쪽 Scene 코드를 대량 생성하지 않는다.
- 참고 3b1b 영상이 있으면 카메라 없는 2D 연출, 오브젝트 배치, 강조 리듬을 참고하되 현재 Manim CE API로 재구현한다.
- 코드 작성의 1차 기준은 `src/scripts/{NN}_{scene_name}.txt`다.
- 기본 작업 순서는 `script -> mp3/timings.json -> scene code`다.
- 스크립트 문단 흐름보다 빠르게 화면이 넘어가면 실패로 본다.
- 화면은 스크립트를 압축하는 도구가 아니라, 스크립트의 논리를 단계별로 드러내는 도구여야 한다.
- 화면 텍스트는 최소화한다. 긴 설명은 mp3가 맡고, 화면은 구조와 관계를 보여준다.
- 우선순위는 `도형/아이콘/수식/화살표/색 변화 > 긴 문장 텍스트`다.
- 코드를 수정하면 바로 렌더해서 확인한다. 렌더 전 검토만으로 완료 처리하지 않는다.
- 아이콘은 직접 그리지 않는다. 기본값은 공용 `videos/assets/tabler-icons/` SVG 라이브러리를 `SVGMobject`로 불러오는 방식이다.
- Scene docstring과 코드 주석은 기본적으로 한국어로 작성한다.
- 주석은 `# Beat 1`처럼 빈 라벨로 끝내지 않는다. 해당 구간의 화면 의도, 스크립트 대응, 다음 전환 이유가 드러나야 한다.
- `build/audio/{NN}_{scene_name}.timings.json`이 있으면, 그 chunk 시간표를 Beat 타이밍의 출발점으로 사용한다.
- 이 timing 파일은 mux 단계가 아니라 Scene 코드 단계에서 읽어야 한다.
- 가능하면 mp3와 `.timings.json`이 준비되기 전에는 Scene 코드를 확정하지 않는다.
- 코드에 들어가기 전, 현재 Scene가 ipynb의 어디서 시작하고 끝나는지 먼저 고정한다.
- 직전 Scene 마지막 문장과 현재 Scene 첫 문장이 자연스럽게 이어지는지 확인한 뒤에만 Beat를 설계한다.

## 1. Scene 클래스 구조

```python
class Scene{NN}_{ClassName}(Scene):  # 또는 ThreeDScene
    """
    Scene {NN}: {핵심 주장}

    Visual Pivot: {시각적 전환점}
    Reference: {source}.ipynb - {관련 셀/섹션}

    Beats:
    1. {Beat 1 설명}
    2. {Beat 2 설명}
    3. {Beat 3 설명}
    """

    # 타이밍 조정 상수
    WAIT_TAIL = 1.0      # 마지막 여백
    RUN_TIME_SCALE = 1.0  # 전체 속도 조절

    def construct(self):
        # Beat 1: 스크립트의 첫 설명 단락을 처리한다.
        # 여기서는 핵심 개념만 좁게 보여주고, 동시 노출량을 제한한다.
        ...
        self.wait(0.5)

        # Beat 2: 앞선 개념을 다음 시각 구조로 넘긴다.
        # 왜 이 전환이 필요한지도 주석에서 드러나야 한다.
        ...
        self.wait(0.5)

        # Beat 3: 스크립트의 결론 또는 오해 교정 지점으로 수렴한다.
        ...
        self.wait(self.WAIT_TAIL)
```

권장 주석 패턴:
- `# Beat 1: T_i를 먼저 소개해 첫 화면의 정보량을 제한한다.`
- `# Beat 2: 같은 학생을 두 세계로 나눠 Y_{1i}, Y_{0i}를 시각화한다.`
- `# Beat 3: 한쪽만 관찰 가능하다는 점을 factual / counterfactual 대비로 정리한다.`

## 2. 타이밍 원칙

### 스크립트 우선 원칙
- 먼저 스크립트를 문단/문장 단위로 나눈다.
- 스크립트를 나누기 전에 scene 경계가 맞는지 먼저 본다.
- Scene 경계가 어색하면 Beat를 잘 쪼개도 전체 흐름은 계속 어색하다.
- 각 문단 또는 의미 단위마다 최소 한 번의 시각적 변화가 있어야 한다.
- 설명량이 많은 스크립트인데 화면 전환이 2-3번밖에 없으면 대체로 너무 빠른 것이다.
- "정책 예시 소개", "오해 제기", "핵심 질문 수렴"처럼 스크립트의 의미 단위마다 별도 Beat를 둔다.
- mp3가 없더라도 무성 debug render에서 자막 없이 장면 논리가 따라가야 한다.

### 오디오 길이에 맞추기
- 먼저 스크립트에서 mp3와 `.timings.json`을 만든다.
- mp3 길이를 먼저 확인: `ffprobe -v error -show_entries format=duration ...`
- ±0.5~1초 오차 허용
- mp3 길이를 코드에 하드코딩하지 말 것
- 가능하면 `build/audio/{NN}_{scene_name}.timings.json`을 읽어 chunk별 `start/end/duration`을 확인한다.
- 첫 초안은 "chunk 하나 = Beat 하나" 또는 "인접 chunk 몇 개 = Beat 하나"로 잡는다.
- 화면은 오디오보다 약간 늦게 끝나는 편이 낫다. 오디오보다 먼저 넘어가면 실패로 본다.
- code-only 영상이 mp3보다 짧은 상태에서 mux를 먼저 만들지 않는다. 먼저 Scene 코드의 `wait/run_time/Beat`를 고친다.
- 첫 문장이 도입 선언이면 빈 화면 또는 매우 단순한 화면으로 받는 선택지를 먼저 검토한다.

### 타이밍 조정 우선순위
1. `WAIT_TAIL` 조정 (가장 쉬움)
2. Beat 사이 `self.wait()` 추가/제거
3. 개별 애니메이션 `run_time` 조정
4. chunk timing에 맞춰 Beat 자체의 경계를 다시 나누기
5. 다시 렌더해서 code-only 길이를 확인한 뒤에만 mux

### 일반적인 타이밍
```python
self.play(FadeIn(obj), run_time=0.5)      # 빠른 등장
self.play(Transform(a, b), run_time=1.0)  # 표준 변환
self.play(Write(text), run_time=1.5)      # 텍스트 작성
self.wait(0.3)                            # 짧은 호흡
self.wait(0.8)                            # 표준 호흡
```

## 3. 레이아웃 패턴

### 혼잡도 제어
- 한 화면에 새 정보 블록을 너무 많이 동시에 올리지 않는다.
- 카드, 질문 리스트, 핵심 질문, 결론 문구를 모두 한 번에 보이게 두지 않는다.
- 이전 Beat 요소는 축소, 페이드, 이동 중 하나로 정리한 뒤 다음 핵심 요소를 올린다.
- debug render에서 텍스트 겹침이나 시선 분산이 보이면, 정보량이 아니라 동시 노출량을 줄인다.
- 가능하면 한 순간의 핵심 읽기 대상은 1개, 많아도 2개를 넘기지 않는다.
- 긴 문장 2개 이상, 카드 2개 이상, 보조 문구까지 동시에 띄우는 구성은 기본적으로 피한다.
- 화면에 긴 한국어 문장을 여러 줄 띄우는 대신, 짧은 라벨과 시각적 대응 관계를 사용한다.
- 설명을 위해 문장이 필요하면 3-5어절 정도의 헤드라인으로 줄이고, 나머지는 음성과 도형으로 전달한다.
- 새 Beat를 짤 때는 먼저 "화면 구획"을 정한다. 상/중/하 또는 좌/우 영역을 먼저 배정하고, 각 그룹이 어느 구획을 차지하는지 정한 뒤에만 `next_to`와 `move_to`를 쓴다.
- 같은 Beat에 남아 있는 그룹끼리 바운딩 박스가 겹치면 그 Beat 설계가 실패한 것이다. 좌표 미세조정보다 먼저 그룹 수를 줄이거나 Beat를 분리한다.
- `scale(0.9)` 같은 축소로 겨우 들어가게 만드는 방식은 최후 수단이다. 핵심은 축소가 아니라 동시 노출량 감축이다.
- 표, 패널, 수식처럼 이미 면적이 큰 요소가 있으면 추가 요소는 최대 1개만 더 둔다. 큰 요소 둘을 같은 Beat에 넣을 때는 한쪽을 축소본 또는 ghost 상태로만 유지한다.
- 위아래 분기, 좌우 분기 구조를 쓸 때는 가지 끝 오브젝트의 높이와 폭을 먼저 동일하게 맞춘다. 분기 후 `next_to`만으로 붙이다 보면 쉽게 겹친다.
- Beat 설계 체크리스트:
  1. 이 Beat가 시작될 때 화면에 남아 있는 큰 그룹은 몇 개인가
  2. 이 Beat에서 새로 추가되는 큰 그룹은 몇 개인가
  3. 합계가 2개를 넘으면 분리할 수 없는 이유가 있는가
  4. 상/중/하 또는 좌/우 구획 중 비워 두는 영역이 명확한가
  5. 다음 Beat 전에 사라질 요소가 코드상으로 명시돼 있는가
- 위 체크리스트에서 하나라도 `아니오`면, 좌표 조정 전에 Beat를 다시 설계한다.

### 렌더 후 QA
- 렌더 후 반드시 결과를 보고 아래를 점검한다.
- 텍스트가 물리적으로 겹치지 않는가
- 한 화면에서 어디를 읽어야 할지 즉시 보이는가
- 같은 시간에 읽어야 할 문장 수가 과도하지 않은가
- 화면 요소가 3개 이상 동시에 서로 경쟁하고 있지 않은가
- 지저분하면 내용을 줄이는 게 아니라 동시 노출량을 줄인다
- 방금 수정한 코드가 실제로 반영된 최신 `preview/code` 영상이 생성되었는가
- 수식의 첨자, 아이콘, 박스 외곽선이 서로 닿거나 겹치지 않는가
- 요소가 안 겹쳐도 간격이 너무 좁아 하나의 덩어리처럼 보이지 않는가
- 이전 Beat 잔상이 다음 Beat 핵심 요소와 영역을 두고 경쟁하지 않는가

권장 순서:
1. 먼저 지울 요소를 정한다.
2. 남길 요소를 1-2개 핵심 덩어리로 묶는다.
3. 그 다음에만 위치를 조정한다.
4. 마지막에만 크기를 조정한다.

과밀 Scene 재작성 순서:
1. 현재 화면에서 반드시 살아야 하는 정보 한 줄로 요약
2. 그 정보를 전달하는 데 필요 없는 요소 전부 제거
3. 남은 요소가 2개를 넘으면 Beat 분리
4. 이전 Beat 잔상이 남아 있으면 조기 FadeOut
5. 그 뒤에만 위치와 크기 미세조정

### 화면 영역
```python
# 상단/하단
title.to_edge(UP)
formula.to_edge(DOWN)

# 좌우 분할
left_group.to_edge(LEFT, buff=1)
right_group.to_edge(RIGHT, buff=1)

# 코너
label.to_corner(UR)
note.to_corner(DL)
```

### 정렬
```python
# 수직 정렬
VGroup(a, b, c).arrange(DOWN, buff=0.5)

# 수평 정렬
HGroup(a, b, c).arrange(RIGHT, buff=0.3)

# 중앙 정렬
group.move_to(ORIGIN)
group.next_to(reference, DOWN, buff=0.5)
```

## 4. 색상 규칙

```python
# 강조
HIGHLIGHT = YELLOW
POSITIVE = GREEN
NEGATIVE = RED
NEUTRAL = BLUE

# 데이터 시각화
TREATMENT = "#4CAF50"  # 초록
CONTROL = "#2196F3"    # 파랑
EFFECT = "#FF9800"     # 주황
```

## 5. 텍스트 패턴

### 수식
```python
formula = MathTex(r"E[Y_1 - Y_0]")
formula_colored = MathTex(r"E[Y_1", r"-", r"Y_0]")
formula_colored[0].set_color(GREEN)
formula_colored[2].set_color(RED)
```

### 짧은 라벨 + 관계선
```python
left = Circle(radius=0.35, color=BLUE)
right = Circle(radius=0.35, color=GREEN)
arrow = Arrow(left.get_right(), right.get_left(), buff=0.15)
label = MathTex(r"\to").scale(1.2)
```

### 공용 SVG 아이콘
```python
from pathlib import Path

ICON_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
icon = SVGMobject(str(ICON_DIR / "device-tablet.svg"))
icon.set_stroke(color=TEAL_D, width=2.6)
icon.set_fill(opacity=0)
```

### 한글 텍스트
```python
text = Text("효과 추정", font="NanumGothic")
# 또는 시스템 기본 폰트 사용
text = Text("효과 추정")
```

### 하이라이트 박스
```python
box = SurroundingRectangle(target, color=YELLOW, buff=0.1)
self.play(Create(box))
```

## 6. 애니메이션 패턴

### 순차 등장
```python
for item in items:
    self.play(FadeIn(item, shift=UP*0.2), run_time=0.3)
```

### 동시 변환
```python
self.play(
    Transform(a, a_new),
    Transform(b, b_new),
    run_time=1.0
)
```

### 강조 효과
```python
self.play(Indicate(target))
self.play(Flash(target, color=YELLOW))
self.play(Circumscribe(target))
```

### 페이드 전환
```python
self.play(FadeOut(old_group), FadeIn(new_group))
```

## 7. 3D Scene 패턴 (ThreeDScene)

```python
class Scene{NN}(ThreeDScene):
    def construct(self):
        # 카메라 초기 설정
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)

        # 3D 축
        axes = ThreeDAxes(
            x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3],
            x_length=6, y_length=6, z_length=6
        )

        # 카메라 이동
        self.move_camera(phi=60*DEGREES, theta=-30*DEGREES, run_time=2)

        # 회전
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        # HUD 요소 (화면 고정)
        self.add_fixed_in_frame_mobjects(label)
```

## 8. 데이터 시각화 패턴

### 표 (Table)
```python
table = Table(
    [["A", "B"], ["1", "2"]],
    col_labels=[Text("X"), Text("Y")],
    include_outer_lines=True
)
```

### 막대 그래프
```python
chart = BarChart(
    values=[3, 5, 2],
    bar_names=["A", "B", "C"],
    y_range=[0, 6, 1]
)
```

### 좌표평면 + 점
```python
axes = Axes(x_range=[0, 10], y_range=[0, 10])
dot = Dot(axes.c2p(5, 7), color=RED)
```

## 9. 주석 규칙

```python
# ─── Beat 1: {Beat 이름} ───
# 설명이 필요한 복잡한 로직만 주석
# 명확한 코드는 주석 불필요

# 타이밍 관련
self.wait(0.5)  # 강조 후 호흡
```

코드 상단 또는 Scene docstring에 아래를 적는 것을 기본값으로 한다.
- 어떤 script 파일을 기준으로 구현했는지
- script의 어떤 문단/의미 단위를 Beat 1, Beat 2, Beat 3에 대응시켰는지

## 10. 렌더 명령어

### 저화질 미리보기
```bash
manim -pql {file}.py Scene{NN}_{Name}
```

### 고화질 렌더
```bash
manim -pqh {file}.py Scene{NN}_{Name}
```

### 특정 Scene만
```bash
manim -pql {file}.py Scene03_RegressionPartitions
```

## 11. 흔한 실수

| 실수 | 해결 |
|-----|------|
| 텍스트/수식 겹침 | `buff` 값 조정, `next_to()` 사용 |
| 애니메이션 너무 빠름 | `run_time` 증가 |
| 3D에서 레이블 회전 | `add_fixed_in_frame_mobjects()` |
| 한글 깨짐 | 시스템 한글 폰트 지정 |
