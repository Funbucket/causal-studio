from manim import *

class ParadoxOfComparison(Scene):
    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # 데이터 정의 (notebook 기반)
        # ═══════════════════════════════════════════════════════════════
        # 남성 6명: 5명 treated (days=5), 1명 control (days=8)
        # 여성 4명: 2명 treated (days=2), 2명 control (days=4)

        data = [
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 0, "days": 8},
            {"sex": "W", "drug": 1, "days": 2},
            {"sex": "W", "drug": 0, "days": 4},
            {"sex": "W", "drug": 1, "days": 2},
            {"sex": "W", "drug": 0, "days": 4},
        ]

        # ═══════════════════════════════════════════════════════════════
        # Beat 1: 데이터 등장 (0 - 2.5초)
        # "약이 입원 기간을 줄여주는지 알아봅시다."
        # ═══════════════════════════════════════════════════════════════

        # 제목
        title = Text("약물 효과 분석", font_size=36)
        title.to_edge(UP, buff=0.5)

        # 환자 아이콘 (원으로 표현)
        patients = VGroup()

        for i, d in enumerate(data):
            # 원 생성
            circle = Circle(radius=0.25)
            if d["drug"] == 1:
                circle.set_fill(BLUE, opacity=0.8)
                circle.set_stroke(BLUE_E, width=2)
            else:
                circle.set_fill(GRAY, opacity=0.5)
                circle.set_stroke(GRAY_B, width=2)

            # 성별 라벨
            sex_label = Text(d["sex"], font_size=16, color=WHITE)
            sex_label.move_to(circle)

            # 입원 일수
            days_label = Text(str(d["days"]), font_size=14, color=YELLOW)
            days_label.next_to(circle, DOWN, buff=0.1)

            patient = VGroup(circle, sex_label, days_label)
            patients.add(patient)

        # 2행으로 배치: 상단 treated, 하단 control
        treated_patients = VGroup(*[patients[i] for i, d in enumerate(data) if d["drug"] == 1])
        control_patients = VGroup(*[patients[i] for i, d in enumerate(data) if d["drug"] == 0])

        treated_patients.arrange(RIGHT, buff=0.4)
        control_patients.arrange(RIGHT, buff=0.4)

        all_patients = VGroup(treated_patients, control_patients)
        all_patients.arrange(DOWN, buff=0.8)
        all_patients.move_to(ORIGIN).shift(UP * 0.3)

        # 그룹 라벨
        treated_label = Text("Treated (약 복용)", font_size=20, color=BLUE)
        treated_label.next_to(treated_patients, LEFT, buff=0.5)

        control_label = Text("Control (미복용)", font_size=20, color=GRAY)
        control_label.next_to(control_patients, LEFT, buff=0.5)

        # 애니메이션: 제목 → 데이터
        self.play(Write(title), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.5) for p in patients], lag_ratio=0.08),
            run_time=1.2
        )
        self.play(
            FadeIn(treated_label, shift=RIGHT * 0.2),
            FadeIn(control_label, shift=RIGHT * 0.2),
            run_time=0.5
        )

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: 평균 비교 (2.5 - 5.5초)
        # "단순히 평균을 비교하면,"
        # ═══════════════════════════════════════════════════════════════

        # 평균 계산 표시
        # Treated 평균: (5+5+5+5+5+2+2)/7 = 29/7 ≈ 4.14
        # Control 평균: (8+4+4)/3 = 16/3 ≈ 5.33

        treated_mean = 29/7  # ≈ 4.14
        control_mean = 16/3  # ≈ 5.33

        # 평균 값 표시
        treated_avg_text = MathTex(r"\bar{Y}_1 = ", f"{treated_mean:.2f}", font_size=32)
        treated_avg_text.set_color_by_tex(r"\bar{Y}_1", BLUE)
        treated_avg_text.next_to(treated_patients, RIGHT, buff=0.8)

        control_avg_text = MathTex(r"\bar{Y}_0 = ", f"{control_mean:.2f}", font_size=32)
        control_avg_text.set_color_by_tex(r"\bar{Y}_0", GRAY)
        control_avg_text.next_to(control_patients, RIGHT, buff=0.8)

        self.play(
            Write(treated_avg_text),
            Write(control_avg_text),
            run_time=1.0
        )

        # 차이 계산
        diff_value = treated_mean - control_mean  # ≈ -1.19

        diff_formula = MathTex(
            r"\bar{Y}_1 - \bar{Y}_0", r"=", f"{diff_value:.2f}",
            font_size=40
        )
        diff_formula.to_edge(DOWN, buff=1.2)

        self.play(Write(diff_formula[:2]), run_time=0.8)
        self.wait(0.2)

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 결과 강조 (5.5 - 7.5초)
        # "치료받은 환자가 하루 정도 빨리 퇴원했네요."
        # ═══════════════════════════════════════════════════════════════

        # -1.19 강조 (Visual Pivot) - 약이 효과있어 보임
        result_box = SurroundingRectangle(diff_formula[2], color=GREEN, buff=0.15)

        self.play(
            Write(diff_formula[2]),
            run_time=0.5
        )
        self.play(
            Create(result_box),
            diff_formula[2].animate.set_color(GREEN),
            run_time=0.5
        )

        # 화살표와 설명 - 약이 도움이 되는 것처럼 보임
        arrow_down = Arrow(
            diff_formula.get_right() + RIGHT * 0.3,
            diff_formula.get_right() + RIGHT * 0.3 + DOWN * 0.8,
            color=GREEN,
            stroke_width=4
        )
        better_text = Text("하루 빨리 퇴원!", font_size=24, color=GREEN)
        better_text.next_to(arrow_down, RIGHT, buff=0.2)

        self.play(
            GrowArrow(arrow_down),
            FadeIn(better_text, shift=DOWN * 0.2),
            run_time=0.8
        )

        self.wait(0.2)

        # ═══════════════════════════════════════════════════════════════
        # Beat 4: 질문 제기 (7.5 - 9.4초)
        # "그런데 이게 약의 진짜 효과일까요?"
        # ═══════════════════════════════════════════════════════════════

        # 질문 텍스트
        question = Text("진짜 효과일까?", font_size=48, color=YELLOW)
        question.move_to(ORIGIN).shift(DOWN * 0.5)

        # diff_formula와 result_box를 그룹으로 묶어 함께 이동
        formula_group = VGroup(diff_formula, result_box)

        # 기존 요소 페이드 아웃 후 질문 강조
        self.play(
            FadeOut(title),
            FadeOut(all_patients),
            FadeOut(treated_label),
            FadeOut(control_label),
            FadeOut(treated_avg_text),
            FadeOut(control_avg_text),
            formula_group.animate.move_to(UP * 1.5),
            FadeOut(arrow_down),
            FadeOut(better_text),
            run_time=0.8
        )

        self.play(
            Write(question),
            question.animate.scale(1.1),
            run_time=0.6
        )

        # 물음표 강조
        question_mark = Text("?", font_size=72, color=RED)
        question_mark.next_to(question, RIGHT, buff=0.3)

        self.play(
            FadeIn(question_mark, scale=2),
            run_time=0.4
        )

        # 마무리 정적 구간 (MP3 ~9.4초에 맞춤)
        self.wait(1.0)


class ConfoundingRevealed(Scene):
    """
    Scene 02: Confounding Revealed
    - 핵심 주장: 제3의 변수(교란)가 처리와 결과 모두에 영향을 주면 단순 비교는 편향된다
    - Visual Pivot: 진짜 효과(남성 -3, 여성 -2)가 등장하며 방향이 뒤집힘
    - MP3 길이: ~10.7초
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: 남/여 분리 (0 - 3초)
        # "사실 남성과 여성을 따로 보면,"
        # ═══════════════════════════════════════════════════════════════

        # 남성 그룹 박스
        male_box = RoundedRectangle(
            width=3.5, height=2.2, corner_radius=0.2,
            color=BLUE_D, fill_opacity=0.1
        )
        male_box.shift(LEFT * 2.5 + UP * 0.5)
        male_label = Text("남성 (M)", font_size=24, color=BLUE)
        male_label.next_to(male_box, UP, buff=0.15)

        # 여성 그룹 박스
        female_box = RoundedRectangle(
            width=3.5, height=2.2, corner_radius=0.2,
            color=PINK, fill_opacity=0.1
        )
        female_box.shift(RIGHT * 2.5 + UP * 0.5)
        female_label = Text("여성 (W)", font_size=24, color=PINK)
        female_label.next_to(female_box, UP, buff=0.15)

        # 남성 데이터: treated 5명 (days=5), control 1명 (days=8)
        male_treated = VGroup()
        for _ in range(5):
            dot = Dot(radius=0.12, color=BLUE)
            male_treated.add(dot)
        male_treated.arrange(RIGHT, buff=0.15)
        male_treated_label = Text("T: 5일", font_size=18, color=BLUE)

        male_control = Dot(radius=0.12, color=GRAY)
        male_control_label = Text("C: 8일", font_size=18, color=GRAY)

        male_treated_group = VGroup(male_treated, male_treated_label).arrange(DOWN, buff=0.1)
        male_control_group = VGroup(male_control, male_control_label).arrange(DOWN, buff=0.1)
        male_data = VGroup(male_treated_group, male_control_group).arrange(DOWN, buff=0.3)
        male_data.move_to(male_box)

        # 여성 데이터: treated 2명 (days=2), control 2명 (days=4)
        female_treated = VGroup(Dot(radius=0.12, color=BLUE), Dot(radius=0.12, color=BLUE))
        female_treated.arrange(RIGHT, buff=0.15)
        female_treated_label = Text("T: 2일", font_size=18, color=BLUE)

        female_control = VGroup(Dot(radius=0.12, color=GRAY), Dot(radius=0.12, color=GRAY))
        female_control.arrange(RIGHT, buff=0.15)
        female_control_label = Text("C: 4일", font_size=18, color=GRAY)

        female_treated_group = VGroup(female_treated, female_treated_label).arrange(DOWN, buff=0.1)
        female_control_group = VGroup(female_control, female_control_label).arrange(DOWN, buff=0.1)
        female_data = VGroup(female_treated_group, female_control_group).arrange(DOWN, buff=0.3)
        female_data.move_to(female_box)

        # 애니메이션: 박스와 데이터 등장
        self.play(
            Create(male_box), Create(female_box),
            Write(male_label), Write(female_label),
            run_time=0.8
        )
        self.play(
            FadeIn(male_data, shift=DOWN * 0.2),
            FadeIn(female_data, shift=DOWN * 0.2),
            run_time=0.8
        )
        self.wait(0.4)

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: 셀별 효과 (3 - 6초)
        # "둘 다 약을 먹으면 입원 기간이 줄어듭니다."
        # ═══════════════════════════════════════════════════════════════

        # 남성 효과: 5 - 8 = -3
        male_effect_label = Text("효과 = ", font_size=24)
        male_effect_value = Text("-3", font_size=28, color=GREEN, weight=BOLD)
        male_effect = VGroup(male_effect_label, male_effect_value).arrange(RIGHT, buff=0.1)
        male_effect.next_to(male_box, DOWN, buff=0.3)

        # 여성 효과: 2 - 4 = -2
        female_effect_label = Text("효과 = ", font_size=24)
        female_effect_value = Text("-2", font_size=28, color=GREEN, weight=BOLD)
        female_effect = VGroup(female_effect_label, female_effect_value).arrange(RIGHT, buff=0.1)
        female_effect.next_to(female_box, DOWN, buff=0.3)

        # 효과 강조 박스
        male_effect_box = SurroundingRectangle(male_effect_value, color=GREEN, buff=0.1)
        female_effect_box = SurroundingRectangle(female_effect_value, color=GREEN, buff=0.1)

        self.play(
            Write(male_effect),
            Write(female_effect),
            run_time=0.8
        )
        self.play(
            Create(male_effect_box),
            Create(female_effect_box),
            run_time=0.5
        )

        # "둘 다 감소!" 강조
        decrease_text = Text("둘 다 감소!", font_size=28, color=GREEN)
        decrease_text.to_edge(DOWN, buff=0.8)

        self.play(Write(decrease_text), run_time=0.6)
        self.wait(0.6)

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 진짜 ATE 계산 (6 - 8.5초)
        # "성별이라는 교란 변수가"
        # ═══════════════════════════════════════════════════════════════

        # 기존 요소들 페이드아웃 (겹침 방지)
        upper_group = VGroup(
            male_box, female_box, male_label, female_label,
            male_data, female_data
        )
        effect_group = VGroup(
            male_effect, female_effect, male_effect_box, female_effect_box
        )

        self.play(
            FadeOut(decrease_text),
            FadeOut(upper_group),
            effect_group.animate.scale(0.8).to_edge(UP, buff=0.5),
            run_time=0.8
        )

        # ATE 계산 공식
        ate_formula = MathTex(
            r"\text{ATE} = ",
            r"\frac{(-3) \times 6 + (-2) \times 4}{10}",
            r"= -2.6",
            font_size=36
        )
        ate_formula.move_to(UP * 0.5)
        ate_formula[2].set_color(YELLOW)

        self.play(Write(ate_formula[:2]), run_time=1.0)
        self.play(Write(ate_formula[2]), run_time=0.5)

        # -2.6 강조
        ate_box = SurroundingRectangle(ate_formula[2], color=YELLOW, buff=0.12)
        self.play(Create(ate_box), run_time=0.4)

        self.wait(0.3)

        # ═══════════════════════════════════════════════════════════════
        # Beat 4: Confounding 다이어그램 (8.5 - 10.7초)
        # "처리와 결과 모두에 영향을 준 것입니다."
        # ═══════════════════════════════════════════════════════════════

        # 기존 효과 표시 페이드아웃, 공식은 위로
        ate_group = VGroup(ate_formula, ate_box)
        self.play(
            FadeOut(effect_group),
            ate_group.animate.to_edge(UP, buff=0.8),
            run_time=0.5
        )

        # Confounding 다이어그램
        # 성별 (X) → 처리 (T), 성별 (X) → 결과 (Y)
        sex_node = Circle(radius=0.4, color=ORANGE, fill_opacity=0.3)
        sex_text = Text("성별", font_size=20)
        sex_text.move_to(sex_node)
        sex_group = VGroup(sex_node, sex_text)
        sex_group.move_to(DOWN * 0.5 + LEFT * 2.5)

        treat_node = Circle(radius=0.4, color=BLUE, fill_opacity=0.3)
        treat_text = Text("처리", font_size=20)
        treat_text.move_to(treat_node)
        treat_group = VGroup(treat_node, treat_text)
        treat_group.move_to(DOWN * 0.5)

        outcome_node = Circle(radius=0.4, color=GREEN, fill_opacity=0.3)
        outcome_text = Text("결과", font_size=20)
        outcome_text.move_to(outcome_node)
        outcome_group = VGroup(outcome_node, outcome_text)
        outcome_group.move_to(DOWN * 0.5 + RIGHT * 2.5)

        # 화살표
        arrow_sex_treat = Arrow(
            sex_node.get_right(), treat_node.get_left(),
            color=ORANGE, buff=0.1, stroke_width=3
        )
        arrow_sex_outcome = CurvedArrow(
            sex_node.get_top() + UP * 0.1,
            outcome_node.get_top() + UP * 0.1,
            color=ORANGE, angle=-TAU/4
        )
        arrow_treat_outcome = Arrow(
            treat_node.get_right(), outcome_node.get_left(),
            color=WHITE, buff=0.1, stroke_width=3
        )

        # Confounding 라벨
        confound_label = Text("Confounding", font_size=28, color=ORANGE)
        confound_label.next_to(arrow_sex_outcome, UP, buff=0.1)

        # 다이어그램 등장
        self.play(
            FadeIn(sex_group),
            FadeIn(treat_group),
            FadeIn(outcome_group),
            run_time=0.6
        )
        self.play(
            GrowArrow(arrow_sex_treat),
            GrowArrow(arrow_treat_outcome),
            run_time=0.5
        )
        self.play(
            Create(arrow_sex_outcome),
            Write(confound_label),
            run_time=0.6
        )

        # 마무리 정적 구간 (MP3 ~10.7초에 맞춤)
        self.wait(0.8)


class RegressionPartitions(Scene):
    """
    Scene 03: Regression Partitions
    - 핵심 주장: 회귀분석은 데이터를 공변량 셀로 분할하여 각 셀 내에서 효과를 추정한다
    - Visual Pivot: 하나의 테이블이 두 개의 셀(남/여)로 시각적으로 분리됨
    - MP3 길이: ~10.5초
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: 질문 제기 + 전체 데이터 (0 - 2.5초)
        # "그럼 교란을 어떻게 통제할까요?"
        # ═══════════════════════════════════════════════════════════════

        # 질문 텍스트
        question = Text("교란을 어떻게 통제할까요?", font_size=36, color=YELLOW)
        question.to_edge(UP, buff=0.6)

        # 전체 데이터 테이블 (10명)
        data = [
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 1, "days": 5},
            {"sex": "M", "drug": 0, "days": 8},
            {"sex": "W", "drug": 1, "days": 2},
            {"sex": "W", "drug": 0, "days": 4},
            {"sex": "W", "drug": 1, "days": 2},
            {"sex": "W", "drug": 0, "days": 4},
        ]

        # 환자 아이콘 생성
        patients = VGroup()
        for d in data:
            circle = Circle(radius=0.22)
            if d["drug"] == 1:
                circle.set_fill(BLUE, opacity=0.8)
                circle.set_stroke(BLUE_E, width=2)
            else:
                circle.set_fill(GRAY, opacity=0.5)
                circle.set_stroke(GRAY_B, width=2)

            label = Text(d["sex"], font_size=14, color=WHITE)
            label.move_to(circle)
            patient = VGroup(circle, label)
            patients.add(patient)

        patients.arrange_in_grid(rows=2, cols=5, buff=0.3)
        patients.move_to(ORIGIN)

        # 애니메이션
        self.play(Write(question), run_time=1.0)
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.5) for p in patients], lag_ratio=0.05),
            run_time=1.2
        )
        self.wait(0.8)

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: 남/여 분리 (2.5 - 5.5초)
        # "회귀분석은 데이터를 성별로 나눈 뒤,"
        # ═══════════════════════════════════════════════════════════════

        # Regression 라벨
        regression_label = Text("Regression", font_size=28, color=GREEN)
        regression_label.next_to(question, DOWN, buff=0.3)

        self.play(
            FadeOut(question),
            Write(regression_label),
            run_time=0.6
        )

        # 남성/여성 분리
        male_patients = VGroup(*[patients[i] for i in range(6)])
        female_patients = VGroup(*[patients[i] for i in range(6, 10)])

        # 남성 박스
        male_box = RoundedRectangle(width=3.8, height=2.5, corner_radius=0.15, color=BLUE_D)
        male_box.shift(LEFT * 2.8)
        male_title = Text("남성 (M)", font_size=22, color=BLUE)
        male_title.next_to(male_box, UP, buff=0.1)

        # 여성 박스
        female_box = RoundedRectangle(width=3.8, height=2.5, corner_radius=0.15, color=PINK)
        female_box.shift(RIGHT * 2.8)
        female_title = Text("여성 (W)", font_size=22, color=PINK)
        female_title.next_to(female_box, UP, buff=0.1)

        # 분리 애니메이션
        self.play(
            Create(male_box), Create(female_box),
            Write(male_title), Write(female_title),
            run_time=0.6
        )

        # 환자들 이동
        male_target = male_box.get_center()
        female_target = female_box.get_center()

        male_patients.generate_target()
        male_patients.target.arrange_in_grid(rows=2, cols=3, buff=0.25)
        male_patients.target.move_to(male_target)

        female_patients.generate_target()
        female_patients.target.arrange_in_grid(rows=2, cols=2, buff=0.25)
        female_patients.target.move_to(female_target)

        self.play(
            MoveToTarget(male_patients),
            MoveToTarget(female_patients),
            run_time=1.2
        )
        self.wait(0.8)

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 각 셀 내 비교 (5.5 - 8초)
        # "각 그룹 안에서 처리 효과를 계산합니다."
        # ═══════════════════════════════════════════════════════════════

        # 남성 그룹 내 비교: T=5, C=8
        male_compare = MathTex(r"5 - 8", font_size=28)
        male_compare.next_to(male_box, DOWN, buff=0.2)

        # 여성 그룹 내 비교: T=2, C=4
        female_compare = MathTex(r"2 - 4", font_size=28)
        female_compare.next_to(female_box, DOWN, buff=0.2)

        self.play(
            Write(male_compare),
            Write(female_compare),
            run_time=0.8
        )
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════════════
        # Beat 4: 효과 표시 (8 - 10.5초)
        # "남성은 마이너스 3, 여성은 마이너스 2."
        # ═══════════════════════════════════════════════════════════════

        # 효과 계산 결과
        male_effect = MathTex(r"= -3", font_size=32, color=GREEN)
        male_effect.next_to(male_compare, RIGHT, buff=0.1)

        female_effect = MathTex(r"= -2", font_size=32, color=GREEN)
        female_effect.next_to(female_compare, RIGHT, buff=0.1)

        self.play(
            Write(male_effect),
            Write(female_effect),
            run_time=0.6
        )

        # 효과 강조 박스
        male_effect_box = SurroundingRectangle(
            VGroup(male_compare, male_effect), color=GREEN, buff=0.1
        )
        female_effect_box = SurroundingRectangle(
            VGroup(female_compare, female_effect), color=GREEN, buff=0.1
        )

        self.play(
            Create(male_effect_box),
            Create(female_effect_box),
            run_time=0.5
        )

        # 결론 텍스트
        conclusion = Text("각 셀 내에서 효과 계산!", font_size=24, color=GREEN)
        conclusion.to_edge(DOWN, buff=0.5)

        self.play(Write(conclusion), run_time=0.6)

        # 마무리 정적 구간 (MP3 ~10.5초에 맞춤)
        self.wait(1.2)


class VarianceWeighting(Scene):
    """
    Scene 04: Variance Weighting
    - 핵심 주장: 회귀는 단순 평균이 아닌 "처리 분산" 비례 가중치로 셀별 효과를 결합한다
    - Visual Pivot: 분산 수치(0.139 vs 0.25)가 등장하고 회귀 계수가 여성 쪽으로 끌림
    - MP3 길이: ~12.38초
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: 그룹별 효과 표시 (0 - 3초)
        # "이제 그룹별 효과를 하나로 합쳐야 합니다."
        # ═══════════════════════════════════════════════════════════════

        # 남성/여성 효과 박스
        male_box = RoundedRectangle(
            width=3, height=2, corner_radius=0.15,
            color=BLUE_D, fill_opacity=0.1
        )
        male_box.shift(LEFT * 2.5)
        male_title = Text("남성 (M)", font_size=22, color=BLUE)
        male_title.next_to(male_box, UP, buff=0.15)

        male_effect = MathTex(r"-3", font_size=48, color=GREEN)
        male_effect.move_to(male_box)

        female_box = RoundedRectangle(
            width=3, height=2, corner_radius=0.15,
            color=PINK, fill_opacity=0.1
        )
        female_box.shift(RIGHT * 2.5)
        female_title = Text("여성 (W)", font_size=22, color=PINK)
        female_title.next_to(female_box, UP, buff=0.15)

        female_effect = MathTex(r"-2", font_size=48, color=GREEN)
        female_effect.move_to(female_box)

        # 애니메이션
        self.play(
            Create(male_box), Create(female_box),
            Write(male_title), Write(female_title),
            run_time=0.8
        )
        self.play(
            Write(male_effect),
            Write(female_effect),
            run_time=0.8
        )

        # "합치기" 화살표
        combine_arrow = Arrow(
            male_box.get_right() + RIGHT * 0.2 + DOWN * 0.5,
            female_box.get_left() + LEFT * 0.2 + DOWN * 0.5,
            color=YELLOW, stroke_width=4, buff=0
        ).shift(DOWN * 0.8)

        question_text = Text("어떻게 합칠까?", font_size=24, color=YELLOW)
        question_text.next_to(combine_arrow, DOWN, buff=0.2)

        self.play(
            GrowArrow(combine_arrow),
            Write(question_text),
            run_time=0.8
        )
        self.wait(0.6)

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: 단순 평균이 아님 (3 - 6.5초)
        # "그런데 회귀는 단순 평균을 쓰지 않아요."
        # ═══════════════════════════════════════════════════════════════

        # 페이드 아웃
        self.play(
            FadeOut(combine_arrow),
            FadeOut(question_text),
            run_time=0.4
        )

        # 단순 평균 표시 (취소선)
        simple_avg = MathTex(
            r"\frac{(-3) + (-2)}{2} = -2.5",
            font_size=36
        )
        simple_avg.to_edge(DOWN, buff=1.5)

        simple_label = Text("단순 평균?", font_size=20, color=GRAY)
        simple_label.next_to(simple_avg, UP, buff=0.2)

        self.play(
            Write(simple_label),
            Write(simple_avg),
            run_time=1.0
        )
        self.wait(0.3)

        # 취소선 (X 표시)
        cross_line1 = Line(
            simple_avg.get_corner(DL) + LEFT * 0.1 + DOWN * 0.1,
            simple_avg.get_corner(UR) + RIGHT * 0.1 + UP * 0.1,
            color=RED, stroke_width=4
        )
        cross_line2 = Line(
            simple_avg.get_corner(UL) + LEFT * 0.1 + UP * 0.1,
            simple_avg.get_corner(DR) + RIGHT * 0.1 + DOWN * 0.1,
            color=RED, stroke_width=4
        )

        not_text = Text("NO!", font_size=28, color=RED, weight=BOLD)
        not_text.next_to(simple_avg, RIGHT, buff=0.5)

        self.play(
            Create(cross_line1),
            Create(cross_line2),
            FadeIn(not_text, scale=1.5),
            run_time=0.6
        )
        self.wait(0.6)

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 분산 가중치 (6.5 - 9.5초)
        # "처리 변수의 분산이 큰 그룹에 더 큰 가중치를 줍니다."
        # ═══════════════════════════════════════════════════════════════

        # 단순 평균 페이드 아웃
        self.play(
            FadeOut(simple_avg),
            FadeOut(simple_label),
            FadeOut(cross_line1),
            FadeOut(cross_line2),
            FadeOut(not_text),
            run_time=0.5
        )

        # 분산 표시 (Visual Pivot)
        male_var = MathTex(r"\text{Var}(T) = 0.139", font_size=28, color=BLUE_C)
        male_var.next_to(male_box, DOWN, buff=0.3)

        female_var = MathTex(r"\text{Var}(T) = 0.25", font_size=28, color=PINK)
        female_var.next_to(female_box, DOWN, buff=0.3)

        self.play(
            Write(male_var),
            Write(female_var),
            run_time=0.8
        )

        # 분산 강조 (여성이 더 큼)
        female_var_box = SurroundingRectangle(female_var, color=YELLOW, buff=0.1)

        bigger_text = Text("더 큰 가중치!", font_size=22, color=YELLOW)
        bigger_text.next_to(female_var_box, DOWN, buff=0.15)

        self.play(
            Create(female_var_box),
            Write(bigger_text),
            run_time=0.6
        )

        # 화살표: 여성 쪽으로 당겨짐
        pull_arrow = Arrow(
            ORIGIN + DOWN * 2,
            RIGHT * 1.5 + DOWN * 2,
            color=YELLOW, stroke_width=5
        )

        self.play(
            GrowArrow(pull_arrow),
            run_time=0.6
        )
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════════════
        # Beat 4: 최종 계수 (9.5 - 12.4초)
        # "그래서 회귀 계수는 마이너스 2.57이 됩니다."
        # ═══════════════════════════════════════════════════════════════

        # 기존 요소 정리
        self.play(
            FadeOut(pull_arrow),
            FadeOut(bigger_text),
            FadeOut(female_var_box),
            run_time=0.4
        )

        # 결과 공식
        result_formula = MathTex(
            r"\beta_{\text{drug}} = ",
            r"-2.57",
            font_size=44
        )
        result_formula.to_edge(DOWN, buff=1.2)
        result_formula[1].set_color(YELLOW)

        self.play(
            Write(result_formula),
            run_time=0.8
        )

        # -2.57이 -2에 더 가까움을 시각화
        result_box = SurroundingRectangle(result_formula[1], color=YELLOW, buff=0.12)

        # 비교 화살표: -2.57 → -2 (여성 쪽)
        compare_arrow = Arrow(
            result_formula[1].get_top(),
            female_effect.get_bottom(),
            color=YELLOW, stroke_width=3, buff=0.15
        )

        closer_text = Text("-2에 더 가까움", font_size=20, color=YELLOW)
        closer_text.next_to(compare_arrow, LEFT, buff=0.15)

        self.play(
            Create(result_box),
            run_time=0.4
        )
        self.play(
            GrowArrow(compare_arrow),
            Write(closer_text),
            run_time=0.6
        )

        # 마무리 정적 구간 (MP3 ~12.4초에 맞춤)
        self.wait(1.4)


class SubclassificationFormula(Scene):
    """
    Scene 05: Subclassification Formula
    - 핵심 주장: 층화 추정량은 셀별 효과를 "표본 크기" 비례로 가중평균한다
    - Visual Style: Scene 03/04와 동일 (박스, 환자 아이콘, 화살표)
    - MP3 길이: ~12.77초
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: 다른 방법 제안 (0 - 3초)
        # "Regression 말고 다른 방법도 있어요."
        # ═══════════════════════════════════════════════════════════════

        # 남성/여성 박스 (Scene 03/04와 동일한 시각적 연속성)
        male_box = RoundedRectangle(
            width=2.8, height=1.8, corner_radius=0.15,
            color=BLUE_D, fill_opacity=0.1
        )
        male_box.shift(LEFT * 2.8 + UP * 1)
        male_title = Text("남성", font_size=20, color=BLUE)
        male_title.next_to(male_box, UP, buff=0.1)

        # 남성 환자 아이콘 (6명: 5 treated, 1 control)
        male_patients = VGroup()
        for i in range(6):
            dot = Circle(radius=0.12)
            if i < 5:
                dot.set_fill(BLUE, opacity=0.8)
                dot.set_stroke(BLUE_E, width=1)
            else:
                dot.set_fill(GRAY, opacity=0.5)
                dot.set_stroke(GRAY_B, width=1)
            male_patients.add(dot)
        male_patients.arrange_in_grid(rows=2, cols=3, buff=0.15)
        male_patients.move_to(male_box)

        female_box = RoundedRectangle(
            width=2.8, height=1.8, corner_radius=0.15,
            color=PINK, fill_opacity=0.1
        )
        female_box.shift(RIGHT * 2.8 + UP * 1)
        female_title = Text("여성", font_size=20, color=PINK)
        female_title.next_to(female_box, UP, buff=0.1)

        # 여성 환자 아이콘 (4명: 2 treated, 2 control)
        female_patients = VGroup()
        for i in range(4):
            dot = Circle(radius=0.12)
            if i < 2:
                dot.set_fill(BLUE, opacity=0.8)
                dot.set_stroke(BLUE_E, width=1)
            else:
                dot.set_fill(GRAY, opacity=0.5)
                dot.set_stroke(GRAY_B, width=1)
            female_patients.add(dot)
        female_patients.arrange_in_grid(rows=2, cols=2, buff=0.15)
        female_patients.move_to(female_box)

        # 효과 라벨
        male_effect = MathTex(r"-3", font_size=32, color=GREEN)
        male_effect.next_to(male_box, DOWN, buff=0.15)
        male_n = Text("n=6", font_size=16, color=GRAY)
        male_n.next_to(male_effect, DOWN, buff=0.05)

        female_effect = MathTex(r"-2", font_size=32, color=GREEN)
        female_effect.next_to(female_box, DOWN, buff=0.15)
        female_n = Text("n=4", font_size=16, color=GRAY)
        female_n.next_to(female_effect, DOWN, buff=0.05)

        # 애니메이션
        self.play(
            Create(male_box), Create(female_box),
            Write(male_title), Write(female_title),
            run_time=0.6
        )
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.5) for p in male_patients], lag_ratio=0.05),
            LaggedStart(*[FadeIn(p, scale=0.5) for p in female_patients], lag_ratio=0.05),
            run_time=0.6
        )
        self.play(
            Write(male_effect), Write(female_effect),
            FadeIn(male_n), FadeIn(female_n),
            run_time=0.8
        )
        self.wait(0.8)

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: 표본 크기 가중 평균 (3 - 6.5초)
        # "셀별 효과를 표본 크기로 평균내면 어떨까요?"
        # ═══════════════════════════════════════════════════════════════

        # 화살표: 각 그룹에서 중앙으로
        center_point = DOWN * 1.5

        arrow_male = Arrow(
            male_effect.get_bottom() + DOWN * 0.3,
            center_point + LEFT * 0.8,
            color=BLUE, stroke_width=3, buff=0.1
        )
        arrow_female = Arrow(
            female_effect.get_bottom() + DOWN * 0.3,
            center_point + RIGHT * 0.8,
            color=PINK, stroke_width=3, buff=0.1
        )

        # 가중치 라벨
        weight_male = MathTex(r"\times \frac{6}{10}", font_size=24, color=BLUE)
        weight_male.next_to(arrow_male, LEFT, buff=0.1)

        weight_female = MathTex(r"\times \frac{4}{10}", font_size=24, color=PINK)
        weight_female.next_to(arrow_female, RIGHT, buff=0.1)

        self.play(
            GrowArrow(arrow_male),
            GrowArrow(arrow_female),
            run_time=0.6
        )
        self.play(
            Write(weight_male),
            Write(weight_female),
            run_time=0.8
        )
        self.wait(0.8)

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 결과 (6.5 - 9.5초)
        # "그러면 마이너스 2.6, 우리가 계산한 진짜 ATE가 나옵니다."
        # ═══════════════════════════════════════════════════════════════

        # 결과 박스
        result = MathTex(r"-2.6", font_size=48, color=GREEN)
        result.move_to(center_point + DOWN * 0.3)

        result_box = SurroundingRectangle(result, color=GREEN, buff=0.15)

        self.play(
            Write(result),
            run_time=0.8
        )
        self.play(
            Create(result_box),
            run_time=0.4
        )

        # 진짜 ATE 라벨
        true_ate = Text("진짜 ATE!", font_size=24, color=GREEN)
        true_ate.next_to(result_box, RIGHT, buff=0.2)

        self.play(Write(true_ate), run_time=0.6)
        self.wait(1.8)  # 결과가 화면에 더 오래 보이도록 대기 시간 증가

        # ═══════════════════════════════════════════════════════════════
        # Beat 4: 한계 제시 (9.5 - 12.8초)
        # "하지만 특성이 많아지면 한계가 있어요."
        # ═══════════════════════════════════════════════════════════════

        # 모든 요소 페이드 아웃
        all_elements = VGroup(
            male_box, female_box, male_title, female_title,
            male_patients, female_patients,
            male_effect, female_effect, male_n, female_n,
            arrow_male, arrow_female, weight_male, weight_female,
            result, result_box, true_ate
        )

        self.play(
            FadeOut(all_elements),
            run_time=0.5
        )

        # 한계 메시지
        limitation = Text("하지만 특성이 많아지면...", font_size=32, color=YELLOW)
        limitation.to_edge(UP, buff=0.8)

        self.play(Write(limitation), run_time=0.6)

        # 셀 격자 시각화 (1D → 2D → 고차원)
        def make_grid(rows, cols, cell_size=0.3):
            grid = VGroup()
            for i in range(rows):
                for j in range(cols):
                    cell = Square(side_length=cell_size, color=BLUE, fill_opacity=0.3, stroke_width=1)
                    cell.move_to(RIGHT * j * (cell_size + 0.05) + DOWN * i * (cell_size + 0.05))
                    grid.add(cell)
            grid.center()
            return grid

        # 1D: 5개 셀
        grid_1d = make_grid(1, 5, 0.4)
        grid_1d.move_to(LEFT * 3)
        label_1d = Text("5개 셀", font_size=18, color=WHITE)
        label_1d.next_to(grid_1d, DOWN, buff=0.2)

        self.play(FadeIn(grid_1d), Write(label_1d), run_time=0.5)

        # 2D: 5x5 = 25개 셀
        grid_2d = make_grid(5, 5, 0.2)
        grid_2d.move_to(ORIGIN)
        label_2d = Text("25개 셀", font_size=18, color=WHITE)
        label_2d.next_to(grid_2d, DOWN, buff=0.2)

        arrow_1 = Arrow(grid_1d.get_right(), grid_2d.get_left(), color=YELLOW, buff=0.2)

        self.play(GrowArrow(arrow_1), run_time=0.3)
        self.play(FadeIn(grid_2d), Write(label_2d), run_time=0.5)

        # 고차원: 숫자로 표현
        explosion = MathTex(r"5^{10} = 9,765,625", font_size=32, color=RED)
        explosion.move_to(RIGHT * 3)

        arrow_2 = Arrow(grid_2d.get_right(), explosion.get_left(), color=YELLOW, buff=0.2)

        self.play(GrowArrow(arrow_2), run_time=0.4)
        self.play(Write(explosion), run_time=0.8)

        # 마무리
        self.wait(1.4)


class MatchingIntuition(Scene):
    """
    Scene 06: Matching Intuition
    - 핵심 주장: 매칭은 각 처리 단위에 유사한 대조 단위("쌍둥이")를 찾아 비교한다
    - Visual Pivot: 개별 단위 사이에 연결선이 그려지며 "쌍 찾기" 직관 전달
    - MP3 길이: ~12.8초
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # Beat 1: Matching 개념 소개 (0 - 3초)
        # "그래서 다른 접근법이 있어요. Matching입니다."
        # ═══════════════════════════════════════════════════════════════

        # 제목
        title = Text("Matching", font_size=48, color=YELLOW, weight=BOLD)
        title.to_edge(UP, buff=0.6)

        subtitle = Text("비슷한 사람끼리 짝 짓기", font_size=24, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.2)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(subtitle), run_time=0.6)
        self.wait(1.6)

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: 짝 짓기 직관 (3 - 6초)
        # "셀을 나누는 대신, 비슷한 사람끼리 직접 짝을 짓는 거예요."
        # ═══════════════════════════════════════════════════════════════

        # 제목 축소
        self.play(
            title.animate.scale(0.6).to_corner(UL, buff=0.3),
            FadeOut(subtitle),
            run_time=0.5
        )

        # 연수생(Treated) vs 비연수생(Control) 그룹
        # 간단한 예시: 4명씩
        treated_group = VGroup()
        control_group = VGroup()

        # Treated (연수생) - 젊은 나이들
        treated_ages = [28, 25, 29, 23]
        for i, age in enumerate(treated_ages):
            person = VGroup()
            circle = Circle(radius=0.25, color=BLUE, fill_opacity=0.7, stroke_width=2)
            age_label = Text(str(age), font_size=16, color=WHITE)
            age_label.move_to(circle)
            person.add(circle, age_label)
            treated_group.add(person)

        treated_group.arrange(DOWN, buff=0.4)
        treated_group.shift(LEFT * 3)

        treated_title = Text("연수생", font_size=22, color=BLUE)
        treated_title.next_to(treated_group, UP, buff=0.3)

        # Control (비연수생) - 나이가 많음
        control_ages = [43, 28, 33, 25]
        for i, age in enumerate(control_ages):
            person = VGroup()
            circle = Circle(radius=0.25, color=GRAY, fill_opacity=0.5, stroke_width=2)
            age_label = Text(str(age), font_size=16, color=WHITE)
            age_label.move_to(circle)
            person.add(circle, age_label)
            control_group.add(person)

        control_group.arrange(DOWN, buff=0.4)
        control_group.shift(RIGHT * 3)

        control_title = Text("비연수생", font_size=22, color=GRAY)
        control_title.next_to(control_group, UP, buff=0.3)

        # 그룹 등장
        self.play(
            FadeIn(treated_group, shift=RIGHT * 0.3),
            FadeIn(control_group, shift=LEFT * 0.3),
            Write(treated_title), Write(control_title),
            run_time=0.8
        )
        self.wait(1.2)

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 연수 프로그램 예시 - 단순 비교 (6 - 9초)
        # "연수 프로그램 예시로 보면,"
        # ═══════════════════════════════════════════════════════════════

        # 단순 비교 결과
        simple_result = VGroup()
        simple_label = Text("단순 비교", font_size=20, color=GRAY)
        simple_value = MathTex(r"-4297", font_size=40, color=RED)
        simple_unit = Text("달러", font_size=18, color=GRAY)
        simple_value.next_to(simple_label, DOWN, buff=0.15)
        simple_unit.next_to(simple_value, RIGHT, buff=0.1)
        simple_result.add(simple_label, simple_value, simple_unit)
        simple_result.move_to(DOWN * 2.5)

        question = Text("연수가 해롭다?", font_size=22, color=RED)
        question.next_to(simple_result, DOWN, buff=0.2)

        self.play(Write(simple_label), run_time=0.4)
        self.play(Write(simple_value), FadeIn(simple_unit), run_time=0.6)
        self.play(Write(question), run_time=0.5)
        self.wait(0.8)

        # ═══════════════════════════════════════════════════════════════
        # Beat 4: 나이 매칭 + 결과 반전 (9 - 12.8초)
        # "같은 나이끼리 비교했더니 결과가 완전히 달라졌어요."
        # ═══════════════════════════════════════════════════════════════

        # 질문 페이드아웃
        self.play(FadeOut(question), run_time=0.3)

        # 매칭 연결선 (같은 나이끼리)
        match_lines = VGroup()

        # 28 -> 28 (정확히 매칭)
        line1 = Line(
            treated_group[0].get_right(),
            control_group[1].get_left(),
            color=YELLOW, stroke_width=3
        )
        match_lines.add(line1)

        # 25 -> 25 (정확히 매칭)
        line2 = Line(
            treated_group[1].get_right(),
            control_group[3].get_left(),
            color=YELLOW, stroke_width=3
        )
        match_lines.add(line2)

        # 29 -> 28 (가장 가까운)
        line3 = Line(
            treated_group[2].get_right(),
            control_group[1].get_left(),
            color=YELLOW, stroke_width=2, stroke_opacity=0.6
        )
        match_lines.add(line3)

        # 23 -> 25 (가장 가까운)
        line4 = Line(
            treated_group[3].get_right(),
            control_group[3].get_left(),
            color=YELLOW, stroke_width=2, stroke_opacity=0.6
        )
        match_lines.add(line4)

        # 매칭 라벨
        match_label = Text("나이로 매칭", font_size=24, color=YELLOW)
        match_label.move_to(UP * 0.3)

        self.play(Write(match_label), run_time=0.4)
        self.play(
            LaggedStart(*[Create(line) for line in match_lines], lag_ratio=0.12),
            run_time=0.8
        )

        # 매칭 후 결과: -4297 → +2458 변환
        new_value = MathTex(r"+2458", font_size=40, color=GREEN)
        new_value.move_to(simple_value.get_center())

        new_label = Text("매칭 후", font_size=20, color=GREEN)
        new_label.move_to(simple_label.get_center())

        self.play(
            Transform(simple_value, new_value),
            Transform(simple_label, new_label),
            FadeOut(simple_unit),
            run_time=0.8
        )

        # 결과 강조 박스
        result_box = SurroundingRectangle(simple_value, color=GREEN, buff=0.12)
        self.play(Create(result_box), run_time=0.5)

        # 마무리
        self.wait(2.2)


class KNNMatching(Scene):
    """
    Scene 07: KNN Matching
    - 핵심 주장: 다변량 매칭은 스케일링된 특성 공간에서 최근접 이웃을 찾는다
    - Visual Pivot: 2D 산점도에서 각 treated → nearest control로 선이 연결됨
    - 노트북 참조: medicine_impact_recovery 데이터, 단순비교 +16.9일, KNN매칭 -0.9954일
    - MP3 길이: ~47초 (14줄 스크립트)
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # 타이밍 조정용 상수
        # ═══════════════════════════════════════════════════════════════
        WAIT_TAIL = 0.5        # 오디오-영상 길이 불일치 시 먼저 조정
        RUN_TIME_SCALE = 1.0   # 전체 애니메이션 템포 미세조정용

        # ═══════════════════════════════════════════════════════════════
        # Beat 1: 다변량 문제 제기 + 약물 데이터 소개 (0 - 14초)
        # 1. "나이 하나로 매칭하는 건 쉬웠어요."
        # 2. "그런데 특성이 여러 개면 어떻게 할까요?"
        # 3. "다시 약물 데이터로 돌아가볼게요."
        # 4. "중증도, 나이, 성별. 세 가지 교란 변수가 있어요."
        # ═══════════════════════════════════════════════════════════════

        # 1D 숫자선 (나이) - Scene 06에서 이어지는 느낌
        line_1d = NumberLine(
            x_range=[20, 50, 10],
            length=4,
            include_numbers=True,
            font_size=20
        )
        line_1d.shift(UP * 1)
        label_1d = Text("나이", font_size=20, color=BLUE)
        label_1d.next_to(line_1d, LEFT, buff=0.3)

        # 1D 점들
        dots_1d = VGroup()
        for x in [25, 28, 32]:
            dot = Dot(line_1d.n2p(x), color=BLUE, radius=0.08)
            dots_1d.add(dot)
        for x in [27, 35, 45]:
            dot = Dot(line_1d.n2p(x), color=GRAY, radius=0.08)
            dots_1d.add(dot)

        self.play(Create(line_1d), Write(label_1d), run_time=1.0 * RUN_TIME_SCALE)
        self.play(FadeIn(dots_1d), run_time=0.8 * RUN_TIME_SCALE)
        self.wait(1.5)  # Line 1: "나이 하나로 매칭하는 건 쉬웠어요."

        # "특성이 여러 개면?" 질문
        question = Text("특성이 여러 개면?", font_size=28, color=YELLOW)
        question.to_edge(UP, buff=0.5)

        self.play(Write(question), run_time=0.8 * RUN_TIME_SCALE)
        self.wait(2.0)  # Line 2: "그런데 특성이 여러 개면 어떻게 할까요?"

        # 1D 요소 페이드아웃 + 약물 데이터 소개
        self.play(
            FadeOut(line_1d), FadeOut(label_1d), FadeOut(dots_1d),
            question.animate.scale(0.7).to_corner(UL, buff=0.3),
            run_time=0.8 * RUN_TIME_SCALE
        )

        # 약물 데이터 특성 소개
        data_title = Text("약물 데이터", font_size=32, color=YELLOW)
        data_title.to_edge(UP, buff=0.5)

        # 세 가지 교란 변수 박스
        confounders = VGroup()
        confounder_names = ["중증도", "나이", "성별"]
        confounder_colors = [RED, BLUE, PINK]
        for i, (name, color) in enumerate(zip(confounder_names, confounder_colors)):
            box = RoundedRectangle(
                width=2.2, height=1.2, corner_radius=0.1,
                color=color, fill_opacity=0.2
            )
            label = Text(name, font_size=24, color=color)
            label.move_to(box)
            group = VGroup(box, label)
            confounders.add(group)

        confounders.arrange(RIGHT, buff=0.4)
        confounders.move_to(ORIGIN)

        self.play(Write(data_title), run_time=0.8 * RUN_TIME_SCALE)
        self.wait(1.5)  # Line 3: "다시 약물 데이터로 돌아가볼게요."
        self.play(
            LaggedStart(*[FadeIn(c, scale=0.8) for c in confounders], lag_ratio=0.2),
            run_time=1.2 * RUN_TIME_SCALE
        )
        self.wait(2.5)  # Line 4: "중증도, 나이, 성별. 세 가지 교란 변수가 있어요."

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: 단순 비교 결과 + 교란 설명 (14 - 26초)
        # 5. "교란변수를 통제하지 않고, 약 먹은 사람과 안 먹은 사람의 평균 회복일을 비교하면요."
        # 6. "플러스 17일. 약을 먹으면 회복이 더 오래 걸린다고 나오네요."
        # 7. "이건 교란 때문이에요. 더 아픈 사람이 약을 먹으니까요."
        # ═══════════════════════════════════════════════════════════════

        # 단순 비교 수식 (Visual: 어떻게 계산되는지 보여줌)
        simple_formula = MathTex(
            r"E[Y|T=1] - E[Y|T=0]",
            font_size=32, color=GRAY
        )
        simple_formula.next_to(confounders, DOWN, buff=0.4)

        self.play(Write(simple_formula), run_time=0.8 * RUN_TIME_SCALE)
        self.wait(2.0)  # Line 5: "교란변수를 통제하지 않고..."

        # 단순 비교 결과
        simple_result = MathTex(r"= +17", font_size=48, color=RED)
        simple_result.next_to(simple_formula, RIGHT, buff=0.2)
        simple_unit = Text("일", font_size=24, color=RED)
        simple_unit.next_to(simple_result, RIGHT, buff=0.1)

        harmful_text = Text("약을 먹으면 회복이 더 오래 걸린다?", font_size=22, color=RED)
        harmful_text.next_to(simple_formula, DOWN, buff=0.5)

        self.play(
            Write(simple_result),
            Write(simple_unit),
            run_time=0.8 * RUN_TIME_SCALE
        )
        self.play(Write(harmful_text), run_time=0.8 * RUN_TIME_SCALE)
        self.wait(2.5)  # Line 6: "플러스 17일. 약을 먹으면 회복이 더 오래 걸린다고 나오네요."

        # 교란 설명
        confound_explanation = Text("교란 때문! 더 아픈 사람이 약을 먹으니까", font_size=22, color=YELLOW)
        confound_explanation.next_to(harmful_text, DOWN, buff=0.3)

        self.play(Write(confound_explanation), run_time=1.0 * RUN_TIME_SCALE)
        self.wait(2.0)  # Line 7: "이건 교란 때문이에요. 더 아픈 사람이 약을 먹으니까요."

        # 전환
        self.play(
            FadeOut(confounders),
            FadeOut(simple_formula),
            FadeOut(simple_result), FadeOut(simple_unit),
            FadeOut(harmful_text), FadeOut(confound_explanation),
            FadeOut(data_title),
            FadeOut(question),
            run_time=0.8 * RUN_TIME_SCALE
        )

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 거리 측정 + 스케일링의 중요성 (26 - 40초)
        # 8. "비슷한 사람끼리 비교하려면, 거리를 측정해야 해요."
        # 9. "이때 스케일링이 중요합니다."
        # 10. "나이는 20에서 60, 중증도는 0에서 1."
        # 11. "단위가 다르면 나이가 거리를 지배해버려요."
        # 12. "표준화하면 모든 특성이 공평해집니다."
        # ═══════════════════════════════════════════════════════════════

        # 거리 측정 도입
        distance_title = Text("비슷한 사람끼리 비교하려면?", font_size=28, color=YELLOW)
        distance_title.to_edge(UP, buff=0.5)

        distance_text = Text("→ 거리를 측정!", font_size=24, color=WHITE)
        distance_text.next_to(distance_title, DOWN, buff=0.3)

        self.play(Write(distance_title), run_time=0.8 * RUN_TIME_SCALE)
        self.play(Write(distance_text), run_time=0.6 * RUN_TIME_SCALE)
        self.wait(2.0)  # Line 8: "비슷한 사람끼리 비교하려면, 거리를 측정해야 해요."

        # 스케일링 강조
        scaling_title = Text("스케일링이 중요!", font_size=32, color=GREEN)
        scaling_title.move_to(distance_title.get_center())

        self.play(
            Transform(distance_title, scaling_title),
            FadeOut(distance_text),
            run_time=0.8 * RUN_TIME_SCALE
        )
        self.wait(1.5)  # Line 9: "이때 스케일링이 중요합니다."

        # 스케일 비교 시각화
        # 나이 막대
        age_bar = Rectangle(width=5, height=0.5, color=BLUE, fill_opacity=0.5)
        age_bar.shift(UP * 0.3 + LEFT * 0.5)
        age_label = Text("나이: 20 ~ 60", font_size=20, color=BLUE)
        age_label.next_to(age_bar, LEFT, buff=0.3)
        age_range = Text("40 단위", font_size=16, color=BLUE)
        age_range.next_to(age_bar, RIGHT, buff=0.2)

        # 중증도 막대 (작음)
        severity_bar = Rectangle(width=0.5, height=0.5, color=RED, fill_opacity=0.5)
        severity_bar.shift(DOWN * 0.7 + LEFT * 2.75)
        severity_label = Text("중증도: 0 ~ 1", font_size=20, color=RED)
        severity_label.next_to(severity_bar, LEFT, buff=0.3)
        severity_range = Text("1 단위", font_size=16, color=RED)
        severity_range.next_to(severity_bar, RIGHT, buff=0.2)

        self.play(
            Create(age_bar), Write(age_label), Write(age_range),
            run_time=1.0 * RUN_TIME_SCALE
        )
        self.play(
            Create(severity_bar), Write(severity_label), Write(severity_range),
            run_time=1.0 * RUN_TIME_SCALE
        )
        self.wait(2.0)  # Line 10: "나이는 20에서 60, 중증도는 0에서 1."

        # 경고 메시지
        warning = Text("→ 나이가 거리를 지배!", font_size=24, color=RED)
        warning.next_to(severity_bar, DOWN, buff=0.5)

        self.play(Write(warning), run_time=0.8 * RUN_TIME_SCALE)
        self.wait(2.0)  # Line 11: "단위가 다르면 나이가 거리를 지배해버려요."

        # 표준화 후
        standardize_text = Text("표준화 → 모든 특성이 공평!", font_size=24, color=GREEN)
        standardize_text.next_to(warning, DOWN, buff=0.3)

        # 막대 크기 변환 (같아짐)
        new_age_bar = Rectangle(width=2, height=0.5, color=BLUE, fill_opacity=0.5)
        new_age_bar.move_to(age_bar.get_center())

        new_severity_bar = Rectangle(width=2, height=0.5, color=RED, fill_opacity=0.5)
        new_severity_bar.move_to(severity_bar.get_center() + RIGHT * 0.75)

        self.play(Write(standardize_text), run_time=0.8 * RUN_TIME_SCALE)
        self.play(
            Transform(age_bar, new_age_bar),
            Transform(severity_bar, new_severity_bar),
            FadeOut(age_range), FadeOut(severity_range),
            run_time=1.2 * RUN_TIME_SCALE
        )
        self.wait(2.0)  # Line 12: "표준화하면 모든 특성이 공평해집니다."

        # ═══════════════════════════════════════════════════════════════
        # Beat 4: KNN 매칭 결과 (40 - 47초)
        # 13. "K=1 최근접 이웃으로 매칭하면, 마이너스 1일."
        # 14. "방향이 완전히 바뀌었어요!"
        # ═══════════════════════════════════════════════════════════════

        # 이전 요소 정리
        self.play(
            FadeOut(distance_title),
            FadeOut(age_bar), FadeOut(severity_bar),
            FadeOut(age_label), FadeOut(severity_label),
            FadeOut(warning), FadeOut(standardize_text),
            run_time=0.8 * RUN_TIME_SCALE
        )

        # 2D 산점도
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": False, "include_numbers": True, "font_size": 18},
        )
        axes.shift(LEFT * 1.5)

        x_label = Text("나이 (표준화)", font_size=16, color=WHITE)
        x_label.next_to(axes.x_axis, DOWN, buff=0.1)
        y_label = Text("중증도 (표준화)", font_size=16, color=WHITE)
        y_label.next_to(axes.y_axis, LEFT, buff=0.1)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.8 * RUN_TIME_SCALE)

        # 점들
        treated_points = [(2, 3), (3, 7), (5, 5), (7, 8)]
        control_points = [(3, 2), (4, 6), (6, 4), (8, 7)]

        treated_dots = VGroup()
        for x, y in treated_points:
            dot = Dot(axes.c2p(x, y), color=BLUE, radius=0.12)
            treated_dots.add(dot)

        control_dots = VGroup()
        for x, y in control_points:
            dot = Dot(axes.c2p(x, y), color=GRAY, radius=0.12)
            control_dots.add(dot)

        self.play(FadeIn(treated_dots), FadeIn(control_dots), run_time=0.6 * RUN_TIME_SCALE)

        # KNN 매칭선
        knn_label = Text("K=1 최근접 이웃", font_size=24, color=YELLOW)
        knn_label.to_edge(UP, buff=0.5)

        self.play(Write(knn_label), run_time=0.6 * RUN_TIME_SCALE)

        match_lines = VGroup()
        for i in range(4):
            line = Line(
                treated_dots[i].get_center(),
                control_dots[i].get_center(),
                color=YELLOW, stroke_width=2
            )
            match_lines.add(line)

        self.play(
            LaggedStart(*[Create(line) for line in match_lines], lag_ratio=0.15),
            run_time=1.0 * RUN_TIME_SCALE
        )

        # 결과 표시
        result_box = RoundedRectangle(
            width=3.5, height=1.8, corner_radius=0.15,
            color=GREEN, fill_opacity=0.1
        )
        result_box.to_edge(RIGHT, buff=0.5)

        result_label = Text("매칭 후", font_size=20, color=GREEN)
        result_label.next_to(result_box, UP, buff=0.1)

        result_value = MathTex(r"-1", font_size=56, color=GREEN)
        result_value.move_to(result_box)

        result_unit = Text("일", font_size=24, color=GREEN)
        result_unit.next_to(result_value, RIGHT, buff=0.1)

        self.play(
            Create(result_box), Write(result_label),
            run_time=0.6 * RUN_TIME_SCALE
        )
        self.play(Write(result_value), Write(result_unit), run_time=0.6 * RUN_TIME_SCALE)
        self.wait(1.0)  # Line 13: "K=1 최근접 이웃으로 매칭하면, 마이너스 1일."

        # 방향 반전 강조
        direction_change = Text("방향이 완전히 바뀌었어요!", font_size=24, color=YELLOW)
        direction_change.next_to(result_box, DOWN, buff=0.2)

        highlight = SurroundingRectangle(result_value, color=YELLOW, buff=0.1)

        self.play(
            Write(direction_change),
            Create(highlight),
            run_time=0.8 * RUN_TIME_SCALE
        )

        # 마무리 (WAIT_TAIL 조정 가능)
        self.wait(WAIT_TAIL)  # Line 14: "방향이 완전히 바뀌었어요!" + 여유


class MatchingBias(Scene):
    """
    Scene 08: Matching Bias (3Blue1Brown Style)
    - 핵심 주장: 불완전 매칭은 체계적 편향을 만들며, 회귀로 보정할 수 있다
    - Visual Pivot: 2D 산점도 + 수식 중심, 보정 전(-1) vs 보정 후(-7) 극적 변화
    - MP3 길이: ~24.89초 (9줄 스크립트)
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # 타이밍 조정용 상수
        # ═══════════════════════════════════════════════════════════════
        WAIT_TAIL = 2.4  # 영상-오디오 동기화용 (24.89초 타겟)
        RUN_TIME_SCALE = 1.0

        # ═══════════════════════════════════════════════════════════════
        # Beat 1: 2D 산점도로 매칭 문제 시각화 (0 - 8초)
        # 1. "그런데 문제가 있어요."
        # 2. "완벽하게 같은 사람은 없잖아요."
        # 3. "매칭된 쌍도 약간의 차이가 있어요."
        # ═══════════════════════════════════════════════════════════════

        # 2D 좌표계 (3Blue1Brown 스타일)
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=4,
            axis_config={"color": GREY_B, "stroke_width": 2},
            tips=False,
        )
        axes.shift(LEFT * 1.5 + DOWN * 0.3)

        x_label = MathTex("X_1", font_size=24, color=GREY_A)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = MathTex("X_2", font_size=24, color=GREY_A)
        y_label.next_to(axes.y_axis, UP, buff=0.1)

        # 처리군 점들 (파란색)
        np.random.seed(42)
        treated_coords = [(2, 3), (4, 7), (6, 5), (8, 8), (3, 6)]
        treated_dots = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE, radius=0.12)
            for x, y in treated_coords
        ])

        # 대조군 점들 (회색)
        control_coords = [(2.5, 2.5), (4.5, 6.5), (5.5, 5.5), (7.5, 7.5), (3.5, 5.5)]
        control_dots = VGroup(*[
            Dot(axes.c2p(x, y), color=GREY, radius=0.12)
            for x, y in control_coords
        ])

        # 매칭 연결선
        match_lines = VGroup(*[
            Line(
                axes.c2p(*treated_coords[i]),
                axes.c2p(*control_coords[i]),
                color=YELLOW_A,
                stroke_width=2,
                stroke_opacity=0.7
            )
            for i in range(5)
        ])

        # 범례
        legend = VGroup()
        t_dot = Dot(color=BLUE, radius=0.08)
        t_text = MathTex(r"T=1", font_size=20, color=BLUE)
        t_text.next_to(t_dot, RIGHT, buff=0.1)
        c_dot = Dot(color=GREY, radius=0.08)
        c_text = MathTex(r"T=0", font_size=20, color=GREY)
        c_text.next_to(c_dot, RIGHT, buff=0.1)
        legend.add(VGroup(t_dot, t_text), VGroup(c_dot, c_text))
        legend.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        legend.to_corner(UR, buff=0.5)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.0 * RUN_TIME_SCALE)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in treated_dots], lag_ratio=0.08),
            LaggedStart(*[FadeIn(d, scale=0.5) for d in control_dots], lag_ratio=0.08),
            FadeIn(legend),
            run_time=1.2 * RUN_TIME_SCALE
        )
        self.wait(1.2)  # Line 1: "그런데 문제가 있어요."

        # 매칭 연결
        self.play(
            LaggedStart(*[Create(line) for line in match_lines], lag_ratio=0.1),
            run_time=1.0 * RUN_TIME_SCALE
        )
        self.wait(1.2)  # Line 2: "완벽하게 같은 사람은 없잖아요."

        # X_i ≈ X_j 수식 (핵심!)
        approx_formula = MathTex(
            r"X_i", r"\approx", r"X_j", r"\quad (d > 0)",
            font_size=36
        )
        approx_formula[0].set_color(BLUE)
        approx_formula[2].set_color(GREY)
        approx_formula[3].set_color(YELLOW)
        approx_formula.to_edge(UP, buff=0.5)

        self.play(Write(approx_formula), run_time=1.0 * RUN_TIME_SCALE)
        self.wait(1.3)  # Line 3: "매칭된 쌍도 약간의 차이가 있어요."

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: 편향 수식 등장 (8 - 13초)
        # 4. "이 작은 차이들이 쌓이면 편향이 생깁니다."
        # ═══════════════════════════════════════════════════════════════

        # 산점도를 왼쪽으로 축소 이동
        scatter_group = VGroup(axes, x_label, y_label, treated_dots, control_dots, match_lines, legend)

        self.play(
            scatter_group.animate.scale(0.6).to_edge(LEFT, buff=0.3),
            approx_formula.animate.scale(0.8).to_corner(UL, buff=0.3),
            run_time=0.8 * RUN_TIME_SCALE
        )

        # 편향 수식 (핵심 수학!)
        bias_formula = MathTex(
            r"\text{Bias} = \frac{1}{N_1} \sum_{i} \left[ \mu_0(X_i) - \mu_0(X_j) \right]",
            font_size=32
        )
        bias_formula.move_to(RIGHT * 2 + UP * 1)

        # 편향 시각적 강조
        bias_box = SurroundingRectangle(bias_formula, color=RED, buff=0.15, stroke_width=2)

        self.play(Write(bias_formula), run_time=1.2 * RUN_TIME_SCALE)
        self.play(Create(bias_box), run_time=0.5 * RUN_TIME_SCALE)
        self.wait(1.8)  # Line 4: "이 작은 차이들이 쌓이면 편향이 생깁니다."

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 회귀 보정 + 결과 비교 (13 - 25초)
        # 5. "다행히 회귀로 보정할 수 있어요."
        # 6. "대조군만으로 회귀 모델을 만들고,"
        # 7. "매칭 쌍의 예측값 차이를 빼주면 됩니다."
        # 8. "보정 전 마이너스 1일, 보정 후 마이너스 7일."
        # 9. "같은 매칭인데 결과가 꽤 다르죠?"
        # ═══════════════════════════════════════════════════════════════

        # 보정 전 추정량 (naive)
        naive_estimator = MathTex(
            r"\hat{\tau}_{\text{naive}}", r"=", r"\frac{1}{N_1} \sum_{i} (Y_i - Y_j)",
            font_size=28
        )
        naive_estimator.move_to(RIGHT * 2 + DOWN * 0.3)

        self.play(
            bias_box.animate.set_color(GREY_D),
            Write(naive_estimator),
            run_time=1.0 * RUN_TIME_SCALE
        )
        self.wait(1.2)  # Line 5: "다행히 회귀로 보정할 수 있어요."

        # 보정된 추정량으로 Transform
        corrected_estimator = MathTex(
            r"\hat{\tau}_{\text{adj}}", r"=", r"\frac{1}{N_1} \sum_{i} \left[ (Y_i - Y_j) - (\hat{\mu}_0(X_i) - \hat{\mu}_0(X_j)) \right]",
            font_size=24
        )
        corrected_estimator.move_to(RIGHT * 2 + DOWN * 0.3)

        self.wait(1.2)  # Line 6: "대조군만으로 회귀 모델을 만들고,"

        self.play(
            TransformMatchingTex(naive_estimator, corrected_estimator),
            run_time=1.2 * RUN_TIME_SCALE
        )

        corrected_box = SurroundingRectangle(corrected_estimator, color=GREEN, buff=0.1, stroke_width=2)
        self.play(Create(corrected_box), run_time=0.5 * RUN_TIME_SCALE)
        self.wait(1.2)  # Line 7: "매칭 쌍의 예측값 차이를 빼주면 됩니다."

        # 결과값을 수식 아래에 자연스럽게 표시
        result_before = MathTex(r"\hat{\tau}_{\text{naive}}", r"=", r"-1", font_size=32)
        result_before[0].set_color(RED)
        result_before[2].set_color(RED)

        result_after = MathTex(r"\hat{\tau}_{\text{adj}}", r"=", r"-7", font_size=32)
        result_after[0].set_color(GREEN)
        result_after[2].set_color(GREEN)

        # 결과를 수식 아래 좌우로 배치
        results_group = VGroup(result_before, result_after)
        results_group.arrange(RIGHT, buff=1.5)
        results_group.next_to(corrected_box, DOWN, buff=0.5)

        # 화살표
        result_arrow = Arrow(
            result_before.get_right() + RIGHT * 0.2,
            result_after.get_left() + LEFT * 0.2,
            color=YELLOW, stroke_width=4, buff=0.1
        )

        self.play(Write(result_before), run_time=0.6 * RUN_TIME_SCALE)
        self.play(GrowArrow(result_arrow), run_time=0.4 * RUN_TIME_SCALE)
        self.play(Write(result_after), run_time=0.6 * RUN_TIME_SCALE)
        self.wait(1.5)  # Line 8: "보정 전 마이너스 1일, 보정 후 마이너스 7일."

        # 7배 차이 강조
        multiplier = MathTex(r"\times 7", font_size=36, color=YELLOW)
        multiplier.next_to(result_arrow, DOWN, buff=0.25)

        self.play(
            Write(multiplier),
            result_after[2].animate.set_color(YELLOW),
            Flash(result_after[2], color=YELLOW, line_length=0.2, num_lines=8),
            run_time=0.8 * RUN_TIME_SCALE
        )

        self.wait(WAIT_TAIL)  # Line 9: "같은 매칭인데 결과가 꽤 다르죠?"


class CurseOfDimensionality(ThreeDScene):
    """
    Scene 09: Curse of Dimensionality (3×3×3 큐브 시각화)
    - 핵심 주장: 차원이 증가하면 데이터 공간이 기하급수적으로 희소해진다
    - Visual Pivot: 1D(3셀) → 2D(9셀) → 3D(27셀 큐브) + 지수 폭발
    - 스크립트 8줄
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # 타이밍 조정용 상수
        # ═══════════════════════════════════════════════════════════════
        WAIT_TAIL = 4.0  # 30.33초 오디오에 맞춤
        RUN_TIME_SCALE = 1.0

        np.random.seed(42)

        # ═══════════════════════════════════════════════════════════════
        # Beat 1: 1D (3셀) → 2D (9셀) (0 - 12초)
        # Line 1: "그럼 특성을 더 많이 통제하면 매칭이 좋아질까요?"
        # Line 2: "나이를 3구간으로 나누면, 셀이 3개예요."
        # Line 3: "소득도 3구간이면? 삼 곱하기 삼, 9개."
        # ═══════════════════════════════════════════════════════════════

        self.wait(2.0)  # Line 1

        # --- 1D: X축 3구간 ---
        x_axis = Arrow(LEFT * 3, RIGHT * 3, color=BLUE, stroke_width=3, buff=0)
        x_label = Text("나이", font_size=24, color=BLUE)
        x_label.next_to(x_axis, RIGHT, buff=0.2)

        # 3구간 구분선
        cell_width = 2.0
        ticks_1d = VGroup()
        for i in range(4):
            pos = -3 + i * cell_width
            tick = Line(UP * 0.2, DOWN * 0.2, color=BLUE, stroke_width=2)
            tick.move_to([pos, 0, 0])
            ticks_1d.add(tick)

        # 셀 배경 (3개)
        cells_1d = VGroup()
        cell_colors = [BLUE_E, BLUE_D, BLUE_C]
        for i in range(3):
            cell = Rectangle(width=cell_width, height=0.5, fill_opacity=0.3, color=cell_colors[i], stroke_width=0)
            cell.move_to([-2 + i * cell_width, 0, 0])
            cells_1d.add(cell)

        # 데이터 점 (1D)
        dots_1d = VGroup()
        dot_x_positions = [-2.3, -1.5, 0.2, 0.8, 1.5, 2.2]
        for i, x in enumerate(dot_x_positions):
            color = BLUE if i < 3 else RED
            dot = Dot([x, 0, 0], color=color, radius=0.12)
            dots_1d.add(dot)

        label_1d = Text("1D: 3 cells", font_size=36, color=WHITE)
        label_1d.to_edge(UP, buff=0.5)

        formula_1d = MathTex(r"3^1 = 3", font_size=40, color=BLUE)
        formula_1d.to_edge(DOWN, buff=0.7)

        self.play(GrowArrow(x_axis), Write(x_label), run_time=0.6 * RUN_TIME_SCALE)
        self.play(
            Create(ticks_1d),
            LaggedStart(*[FadeIn(c) for c in cells_1d], lag_ratio=0.1),
            run_time=0.5 * RUN_TIME_SCALE
        )
        self.play(
            Write(label_1d),
            LaggedStart(*[GrowFromCenter(d) for d in dots_1d], lag_ratio=0.08),
            run_time=0.7 * RUN_TIME_SCALE
        )
        self.play(Write(formula_1d), run_time=0.5 * RUN_TIME_SCALE)
        self.wait(1.8)  # Line 2: "나이를 3구간으로 나누면, 셀이 3개예요."

        # --- 2D 전환: 3×3 그리드 ---
        y_axis = Arrow(DOWN * 2.5, UP * 2.5, color=GREEN, stroke_width=3, buff=0)
        y_axis.move_to([-3, 0, 0])
        y_label = Text("소득", font_size=24, color=GREEN)
        y_label.next_to(y_axis, UP, buff=0.2)

        # 3×3 그리드 셀
        cells_2d = VGroup()
        for i in range(3):
            for j in range(3):
                cell = Rectangle(
                    width=cell_width, height=cell_width * 0.8,
                    fill_opacity=0.15, color=WHITE, stroke_width=1, stroke_color=GREY
                )
                cell.move_to([-2 + i * cell_width, -1.6 + j * cell_width * 0.8, 0])
                cells_2d.add(cell)

        # 2D 데이터 점 위치
        dot_2d_positions = [
            (-2.3, -1.2), (-1.5, 0.5), (0.2, 1.0),
            (0.8, -0.8), (1.5, 0.2), (2.2, 1.3)
        ]
        dots_2d = VGroup()
        for i, (x, y) in enumerate(dot_2d_positions):
            color = BLUE if i < 3 else RED
            dot = Dot([x, y, 0], color=color, radius=0.1)
            dots_2d.add(dot)

        label_2d = Text("2D: 9 cells", font_size=36, color=WHITE)
        label_2d.to_edge(UP, buff=0.5)

        formula_2d = MathTex(r"3^2 = 9", font_size=40, color=GREEN)
        formula_2d.to_edge(DOWN, buff=0.7)

        # 전환 애니메이션
        self.play(
            GrowArrow(y_axis), Write(y_label),
            FadeOut(cells_1d), FadeOut(ticks_1d),
            ReplacementTransform(label_1d, label_2d),
            ReplacementTransform(formula_1d, formula_2d),
            run_time=0.7 * RUN_TIME_SCALE
        )
        self.play(
            LaggedStart(*[FadeIn(c) for c in cells_2d], lag_ratio=0.03),
            run_time=0.6 * RUN_TIME_SCALE
        )
        # 점들이 2D로 퍼짐
        self.play(
            *[dots_1d[i].animate.move_to([dot_2d_positions[i][0], dot_2d_positions[i][1], 0])
              for i in range(len(dots_1d))],
            run_time=0.8 * RUN_TIME_SCALE
        )
        self.wait(2.2)  # Line 3: "소득도 3구간이면? 삼 곱하기 삼, 9개."

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: 3D (27셀 큐브) + 지수 폭발 (12 - 20초)
        # Line 4: "직업까지 3구간이면? 삼의 3승, 27개."
        # Line 5: "특성이 늘어날수록 셀은 폭발해요. 5개면 243개, 10개면 6만 개!"
        # ═══════════════════════════════════════════════════════════════

        # 2D 요소 정리
        self.play(
            FadeOut(x_axis), FadeOut(x_label),
            FadeOut(y_axis), FadeOut(y_label),
            FadeOut(cells_2d), FadeOut(dots_1d),
            FadeOut(label_2d), FadeOut(formula_2d),
            run_time=0.4 * RUN_TIME_SCALE
        )

        # 3D 카메라 설정
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        # 3×3×3 큐브 생성 (27개 작은 큐브)
        cube_size = 1.0
        cube_group = VGroup()

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # 작은 큐브 위치
                    pos = np.array([
                        (i - 1) * cube_size,
                        (j - 1) * cube_size,
                        (k - 1) * cube_size
                    ])
                    # 반투명 큐브
                    small_cube = Cube(side_length=cube_size * 0.95)
                    small_cube.set_fill(BLUE, opacity=0.08)
                    small_cube.set_stroke(BLUE_D, width=0.5, opacity=0.4)
                    small_cube.move_to(pos)
                    cube_group.add(small_cube)

        # 큐브 외곽 (강조)
        outer_cube = Cube(side_length=cube_size * 3)
        outer_cube.set_fill(opacity=0)
        outer_cube.set_stroke(WHITE, width=2)

        # 축 라벨
        x_lab_3d = Text("나이", font_size=18, color=BLUE)
        x_lab_3d.move_to([2.2, 0, 0])
        y_lab_3d = Text("소득", font_size=18, color=GREEN)
        y_lab_3d.move_to([0, 2.2, 0])
        z_lab_3d = Text("직업", font_size=18, color=RED)
        z_lab_3d.move_to([0, 0, 2.2])

        label_3d = Text("3D: 27 cells", font_size=36, color=WHITE)
        label_3d.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(label_3d)

        formula_3d = MathTex(r"3^3 = 27", font_size=40, color=YELLOW)
        formula_3d.to_edge(DOWN, buff=0.7)
        self.add_fixed_in_frame_mobjects(formula_3d)

        # 3D 등장 + 카메라 회전
        self.play(
            Write(label_3d),
            LaggedStart(*[FadeIn(c) for c in cube_group], lag_ratio=0.01),
            Create(outer_cube),
            run_time=0.8 * RUN_TIME_SCALE
        )
        self.play(Write(formula_3d), run_time=0.4 * RUN_TIME_SCALE)

        # 카메라를 3D 뷰로 회전
        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, run_time=1.0 * RUN_TIME_SCALE)

        self.play(
            Write(x_lab_3d), Write(y_lab_3d), Write(z_lab_3d),
            run_time=0.5 * RUN_TIME_SCALE
        )

        self.wait(1.5)  # Line 4: "직업까지 3구간이면? 삼의 3승, 27개."

        # 카메라 천천히 회전
        self.begin_ambient_camera_rotation(rate=0.08)

        # 지수 폭발 표시 (왼쪽에)
        exp_formulas = [
            (r"3^3", "27"),
            (r"3^5", "243"),
            (r"3^{10}", "59049"),
        ]

        exp_display = VGroup()
        for i, (base, result) in enumerate(exp_formulas):
            formula = MathTex(f"{base} = {result}", font_size=32)
            if i == 2:
                formula.set_color(RED)
            exp_display.add(formula)

        exp_display.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        exp_display.to_edge(LEFT, buff=0.6).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(exp_display)

        self.play(
            LaggedStart(*[Write(f) for f in exp_display], lag_ratio=0.4),
            run_time=2.0 * RUN_TIME_SCALE
        )

        # 6만 개 강조
        approx = Text("≈ 6만 개!", font_size=32, color=RED)
        approx.next_to(exp_display[2], RIGHT, buff=0.3)
        self.add_fixed_in_frame_mobjects(approx)

        self.play(
            Write(approx),
            Flash(exp_display[2], color=RED, line_length=0.2, num_lines=8),
            run_time=0.6 * RUN_TIME_SCALE
        )

        self.wait(1.5)  # Line 5: "특성이 늘어날수록 셀은 폭발해요..."

        self.stop_ambient_camera_rotation()

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 희소성 + 매칭 실패 (20 - 29초)
        # Line 6: "데이터는 한정되어 있는데 셀은 폭발적으로 늘어나요."
        # Line 7: "빈 셀이 많아지면 짝을 찾기 어려워집니다."
        # Line 8: "이걸 차원의 저주라고 해요."
        # ═══════════════════════════════════════════════════════════════

        # 일부 셀에만 데이터 점 표시 (희소성)
        sparse_dots = VGroup()
        dot_positions_3d = [
            (-1, -1, -1), (0, 1, 0), (1, 0, 1),  # 처리군 (파랑)
            (-1, 1, 1), (1, -1, 0), (0, 0, -1)   # 대조군 (빨강)
        ]
        for i, pos in enumerate(dot_positions_3d):
            color = BLUE if i < 3 else RED
            dot = Sphere(radius=0.12, color=color)
            dot.move_to(np.array(pos) * cube_size)
            dot.set_opacity(0.9)
            sparse_dots.add(dot)

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in sparse_dots], lag_ratio=0.1),
            run_time=0.7 * RUN_TIME_SCALE
        )

        # 빈 셀 강조 메시지
        sparse_msg = Text("27셀 중 6셀만 채워짐 (22%)", font_size=24, color=YELLOW)
        sparse_msg.to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(sparse_msg)

        self.play(Write(sparse_msg), run_time=0.5 * RUN_TIME_SCALE)
        self.wait(1.8)  # Line 6

        # 매칭 실패 - 점들 사이 연결선
        distance_lines = VGroup()
        line_pairs = [(0, 3), (1, 4), (2, 5)]
        for t_idx, c_idx in line_pairs:
            line = DashedLine(
                sparse_dots[t_idx].get_center(),
                sparse_dots[c_idx].get_center(),
                color=YELLOW, stroke_width=2, dash_length=0.15
            )
            distance_lines.add(line)

        match_fail = Text("짝이 너무 멀다!", font_size=26, color=YELLOW)
        match_fail.next_to(sparse_msg, UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(match_fail)

        self.play(
            *[sparse_dots[i].animate.set_color(YELLOW) for i in [0, 1, 2]],
            LaggedStart(*[Create(line) for line in distance_lines], lag_ratio=0.2),
            run_time=0.8 * RUN_TIME_SCALE
        )
        self.play(Write(match_fail), run_time=0.4 * RUN_TIME_SCALE)
        self.wait(1.5)  # Line 7

        # 차원의 저주 타이틀
        self.play(
            FadeOut(cube_group), FadeOut(outer_cube),
            FadeOut(x_lab_3d), FadeOut(y_lab_3d), FadeOut(z_lab_3d),
            FadeOut(sparse_dots), FadeOut(distance_lines),
            FadeOut(label_3d), FadeOut(formula_3d),
            FadeOut(exp_display), FadeOut(approx),
            FadeOut(sparse_msg), FadeOut(match_fail),
            run_time=0.5 * RUN_TIME_SCALE
        )

        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        curse = Text("차원의 저주", font_size=72, color=RED)
        self.add_fixed_in_frame_mobjects(curse)

        self.play(Write(curse), run_time=1.0 * RUN_TIME_SCALE)

        self.wait(WAIT_TAIL)  # Line 8: "이걸 차원의 저주라고 해요."


class RegressionVsMatching(Scene):
    """
    Scene 10: Regression vs Matching (Summary)
    - 핵심 주장: Regression과 Matching은 각각 장단점이 있으며, 상황에 맞게 선택해야 한다
    - Visual Pivot: 좌우 분할 비교 + 장단점 체크리스트
    - matching.ipynb: "matching is a non-parametric estimator... more flexible than linear regression"
                      "linear regression performs some sort of dimensionality reduction"
    - MP3 길이: ~25.68초 (9줄 스크립트)
    """

    def construct(self):
        # ═══════════════════════════════════════════════════════════════
        # 타이밍 조정용 상수
        # ═══════════════════════════════════════════════════════════════
        WAIT_TAIL = 2.5  # 25.68초 오디오에 맞춤
        RUN_TIME_SCALE = 1.0

        # ═══════════════════════════════════════════════════════════════
        # Beat 1: Regression 특성 (0 - 9초)
        # 1. "정리해볼게요."
        # 2. "Regression은 선형을 가정해요."
        # 3. "모든 데이터를 활용해 전체적인 관계를 추정하죠."
        # ═══════════════════════════════════════════════════════════════

        title = Text("정리", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.6 * RUN_TIME_SCALE)
        self.wait(1.5)  # Line 1

        # Regression 영역 (왼쪽)
        reg_box = RoundedRectangle(
            width=5.5, height=4.5, corner_radius=0.2,
            color=BLUE, fill_opacity=0.1, stroke_width=2
        )
        reg_box.to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)

        reg_title = Text("Regression", font_size=36, color=BLUE)
        reg_title.next_to(reg_box, UP, buff=0.2)

        # 간단한 산점도 + 회귀선
        reg_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=2.5, y_length=2,
            axis_config={"include_tip": False, "color": GREY_B, "stroke_width": 1.5},
        )
        reg_axes.move_to(reg_box.get_center() + UP * 0.5)

        # 데이터 점들
        np.random.seed(10)
        reg_dots = VGroup(*[
            Dot(reg_axes.c2p(x, 0.8*x + np.random.uniform(-0.5, 0.5)), color=GREY, radius=0.06)
            for x in [0.5, 1.2, 2, 2.8, 3.5, 4.2]
        ])

        # 회귀선
        reg_line = reg_axes.plot(lambda x: 0.8*x, x_range=[0, 5], color=BLUE, stroke_width=3)

        # "선형 가정" 레이블
        linear_label = Text("선형 가정", font_size=24, color=BLUE)
        linear_label.next_to(reg_axes, DOWN, buff=0.3)

        self.play(
            FadeIn(reg_box), Write(reg_title),
            run_time=0.5 * RUN_TIME_SCALE
        )
        self.play(
            Create(reg_axes),
            LaggedStart(*[GrowFromCenter(d) for d in reg_dots], lag_ratio=0.05),
            run_time=0.6 * RUN_TIME_SCALE
        )
        self.play(Create(reg_line), run_time=0.5 * RUN_TIME_SCALE)
        self.play(Write(linear_label), run_time=0.4 * RUN_TIME_SCALE)
        self.wait(2.0)  # Line 2

        # "모든 데이터" 강조
        all_data_label = Text("모든 데이터 활용", font_size=22, color=YELLOW)
        all_data_label.next_to(linear_label, DOWN, buff=0.25)

        self.play(
            reg_dots.animate.set_color(YELLOW),
            Write(all_data_label),
            run_time=0.6 * RUN_TIME_SCALE
        )
        self.play(reg_dots.animate.set_color(GREY), run_time=0.3 * RUN_TIME_SCALE)
        self.wait(2.2)  # Line 3

        # ═══════════════════════════════════════════════════════════════
        # Beat 2: Matching 특성 + 장단점 비교 (9 - 19초)
        # 4. "Matching은 가정이 적어요."
        # 5. "비슷한 사람끼리만 비교하니 더 유연하고요."
        # 6. "하지만 차원이 높으면 매칭이 어려워져요."
        # 7. "반면 Regression은 차원 축소를 자연스럽게 해내죠."
        # ═══════════════════════════════════════════════════════════════

        # Matching 영역 (오른쪽)
        match_box = RoundedRectangle(
            width=5.5, height=4.5, corner_radius=0.2,
            color=GREEN, fill_opacity=0.1, stroke_width=2
        )
        match_box.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)

        match_title = Text("Matching", font_size=36, color=GREEN)
        match_title.next_to(match_box, UP, buff=0.2)

        # 매칭 점들
        match_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 5, 1],
            x_length=2.5, y_length=2,
            axis_config={"include_tip": False, "color": GREY_B, "stroke_width": 1.5},
        )
        match_axes.move_to(match_box.get_center() + UP * 0.5)

        # 처리군 (파란점)
        treated_pts = [(1, 2), (2.5, 3.5), (4, 1.5)]
        treated_dots = VGroup(*[
            Dot(match_axes.c2p(x, y), color=BLUE, radius=0.08)
            for x, y in treated_pts
        ])

        # 대조군 (회색점)
        control_pts = [(1.3, 2.3), (2.2, 3.2), (4.3, 1.8)]
        control_dots = VGroup(*[
            Dot(match_axes.c2p(x, y), color=GREY, radius=0.08)
            for x, y in control_pts
        ])

        # 매칭 연결선
        match_lines = VGroup(*[
            DashedLine(
                match_axes.c2p(*treated_pts[i]),
                match_axes.c2p(*control_pts[i]),
                color=GREEN, stroke_width=2, dash_length=0.1
            )
            for i in range(3)
        ])

        # "가정 ↓" 레이블
        flexible_label = Text("비모수적, 유연함", font_size=22, color=GREEN)
        flexible_label.next_to(match_axes, DOWN, buff=0.3)

        self.play(
            FadeIn(match_box), Write(match_title),
            run_time=0.5 * RUN_TIME_SCALE
        )
        self.play(Create(match_axes), run_time=0.3 * RUN_TIME_SCALE)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in treated_dots], lag_ratio=0.1),
            LaggedStart(*[GrowFromCenter(d) for d in control_dots], lag_ratio=0.1),
            run_time=0.5 * RUN_TIME_SCALE
        )
        self.wait(1.5)  # Line 4

        self.play(
            LaggedStart(*[Create(l) for l in match_lines], lag_ratio=0.1),
            Write(flexible_label),
            run_time=0.8 * RUN_TIME_SCALE
        )
        self.wait(2.0)  # Line 5

        # 장단점 표시
        # Matching 단점: 차원의 저주
        curse_icon = Text("⚠ 고차원", font_size=20, color=RED)
        curse_icon.next_to(flexible_label, DOWN, buff=0.25)

        self.play(Write(curse_icon), run_time=0.5 * RUN_TIME_SCALE)
        self.wait(2.0)  # Line 6

        # Regression 장점: 차원 축소
        dim_reduce = Text("✓ 차원 축소", font_size=20, color=BLUE)
        dim_reduce.next_to(all_data_label, DOWN, buff=0.25)

        self.play(Write(dim_reduce), run_time=0.5 * RUN_TIME_SCALE)
        self.wait(2.2)  # Line 7

        # ═══════════════════════════════════════════════════════════════
        # Beat 3: 결론 (19 - 26초)
        # 8. "둘 다 장단점이 있어요."
        # 9. "데이터와 상황에 맞는 도구를 선택하면 됩니다."
        # ═══════════════════════════════════════════════════════════════

        # 둘 다 체크마크
        check_reg = Text("✓", font_size=48, color=BLUE)
        check_reg.move_to(reg_box.get_center())
        check_match = Text("✓", font_size=48, color=GREEN)
        check_match.move_to(match_box.get_center())

        self.play(
            Write(check_reg), Write(check_match),
            run_time=0.6 * RUN_TIME_SCALE
        )
        self.wait(1.8)  # Line 8

        # 최종 메시지
        conclusion = Text("상황에 맞는 도구를 선택!", font_size=36, color=YELLOW)
        conclusion.to_edge(DOWN, buff=0.6)

        self.play(
            title.animate.set_opacity(0.3),
            Write(conclusion),
            run_time=0.8 * RUN_TIME_SCALE
        )

        self.wait(WAIT_TAIL)  # Line 9


# 테스트용 실행
if __name__ == "__main__":
    # manim -pql matching.py ParadoxOfComparison
    # manim -pql matching.py ConfoundingRevealed
    # manim -pql matching.py RegressionPartitions
    # manim -pql matching.py VarianceWeighting
    # manim -pql matching.py SubclassificationFormula
    # manim -pql matching.py CurseOfDimensionality
    pass
