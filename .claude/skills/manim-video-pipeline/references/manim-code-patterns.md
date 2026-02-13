# Manim Code Patterns

Manim Community Edition Scene 작성을 위한 패턴과 규칙.

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
        # ─── Beat 1: {설명} ───
        ...
        self.wait(0.5)

        # ─── Beat 2: {설명} ───
        ...
        self.wait(0.5)

        # ─── Beat 3: {설명} ───
        ...
        self.wait(self.WAIT_TAIL)
```

## 2. 타이밍 원칙

### 오디오 길이에 맞추기
- mp3 길이를 먼저 확인: `ffprobe -v error -show_entries format=duration ...`
- ±0.5~1초 오차 허용
- mp3 길이를 코드에 하드코딩하지 말 것

### 타이밍 조정 우선순위
1. `WAIT_TAIL` 조정 (가장 쉬움)
2. Beat 사이 `self.wait()` 추가/제거
3. 개별 애니메이션 `run_time` 조정

### 일반적인 타이밍
```python
self.play(FadeIn(obj), run_time=0.5)      # 빠른 등장
self.play(Transform(a, b), run_time=1.0)  # 표준 변환
self.play(Write(text), run_time=1.5)      # 텍스트 작성
self.wait(0.3)                            # 짧은 호흡
self.wait(0.8)                            # 표준 호흡
```

## 3. 레이아웃 패턴

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
