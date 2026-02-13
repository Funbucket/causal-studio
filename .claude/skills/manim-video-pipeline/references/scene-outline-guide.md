# Scene 구조 설계 가이드

ipynb/개념 문서를 영상에 적합한 Scene 단위로 재구성하는 가이드.

## 목표

1. 원본 문서의 논리 전개를 분석
2. 영상에 적합한 Scene 단위로 재구성
3. Scene 순서가 인지적 긴장을 형성하도록 설계
4. 각 Scene의 Visual Pivot 정의

## Scene 설계 원칙

### 기본 규칙
- 한 Scene = 하나의 사고 단계
- Scene은 20~40초 내외 (정확한 초 숫자 작성 금지)
- Scene은 2~4개의 Beat(전개 단위)로 구성
- 장면 전환 = 개념 전환

### 피해야 할 것
- 원본을 그대로 나열
- 시각적으로 명확한 부분을 불필요하게 분리
- 과도한 세분화

## Scene 구성 요소

### 1. Scene 이름
- snake_case 형식
- 핵심 개념을 반영
- 예: `paradox_of_comparison`, `confounding_revealed`

### 2. 핵심 주장 (Claim)
- 1줄로 요약
- 시청자가 배울 핵심 메시지
- 예: "단순 평균 비교는 인과 효과가 아니다"

### 3. Expected Misconception
- 시청자가 가질 수 있는 오해
- Visual Pivot으로 깨뜨릴 대상
- 예: "치료군이 더 좋으면 약이 효과 있는 거 아닌가?"

### 4. Visual Pivot
- 오해를 깨는 시각적 전환점
- 구체적인 시각 요소로 명시
- 예: "교란 변수 연결선이 나타나며 숨겨진 관계 드러남"

### 5. Beat 구조
각 Beat의 역할을 1줄로:
- Beat 1: 문제 상황 제시
- Beat 2: 오해 유도 또는 긴장 형성
- Beat 3: Visual Pivot + 해소
- Beat 4: (선택) 개념 정리

## 출력 형식

```markdown
# {Topic} Scene 구조

## 영상 요약
{1줄 요약}

---

## Scene 01: {scene_name}

**핵심 주장**: {Claim}

**Expected Misconception**: {오해}

**Visual Pivot**: {시각적 전환}

**Beats**:
1. {Beat 1 역할}
2. {Beat 2 역할}
3. {Beat 3 역할}

---

## Scene 02: {scene_name}
...

---

## Scene 연결 구조

| From | To | 연결 |
|------|-----|------|
| Scene 01 | Scene 02 | {어떻게 이어지는지} |
| Scene 02 | Scene 03 | {인지적 긴장 형성} |
...
```

## 인지적 긴장 설계

### 긴장 패턴
1. **Setup → Conflict → Resolution**
   - 상황 제시 → 문제 발견 → 해결책

2. **Question → Exploration → Answer**
   - 질문 제기 → 탐색 → 답변

3. **Intuition → Challenge → Insight**
   - 직관 유도 → 반례 제시 → 새로운 통찰

### Scene 간 연결
- Scene N의 결론이 Scene N+1의 질문으로
- 해결된 문제가 새로운 문제를 유발
- 점진적 복잡도 증가

## 예시: Matching Estimator

```markdown
## Scene 01: paradox_of_comparison
**핵심 주장**: 단순 평균 비교는 인과 효과가 아닐 수 있다
**Expected Misconception**: 치료군이 더 좋으면 약 효과다
**Visual Pivot**: "진짜 효과일까?" 질문 등장
**Beats**:
1. 약과 입원 기간 데이터 제시
2. 단순 평균 비교 결과 표시
3. 질문 제기로 긴장 유발

## Scene 02: confounding_revealed
**핵심 주장**: 교란 변수가 치료 선택과 결과 모두에 영향
**Expected Misconception**: 두 그룹은 약 외에는 동일하다
**Visual Pivot**: 중증도 → 치료/결과 연결선 등장
**Beats**:
1. 숨겨진 변수(중증도) 등장
2. 치료 선택과의 관계 시각화
3. 결과와의 관계까지 연결
```

## 주의사항

- 코드 작성 금지 (이 단계에서)
- 스크립트 문장 작성 금지
- 초 단위 타임코드 금지
- 원본 ipynb 구조에 과도하게 얽매이지 말 것
- 영상에 적합한 구조로 재배열
