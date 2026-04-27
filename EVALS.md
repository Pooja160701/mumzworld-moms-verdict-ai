# Evaluation

## Overview

To evaluate the Moms Verdict system, I designed a set of 10 test cases covering both standard and adversarial scenarios. The goal was to move beyond subjective evaluation and measure:

- Groundedness (does output reflect input reviews?)
- Structured output validity
- Uncertainty handling
- Multilingual quality (English + Arabic)

Each test case is scored out of 4 based on these criteria.

---

## Test Cases

The evaluation includes:

- Basic queries (positive / negative sentiment)
- Mixed sentiment scenarios
- Arabic input queries
- Edge cases:
  - Empty query
  - Garbage input
  - Nonexistent product
- Conflicting reviews

---

## Scoring Criteria

Each case is evaluated on:

1. **Summary presence (1 point)**
   - Non-empty, meaningful summary

2. **Groundedness (1 point)**
   - Pros/cons appear in retrieved reviews

3. **Meaningful extraction (1 point)**
   - At least one valid pro or con extracted

4. **Uncertainty handling (1 point)**
   - Correct use of uncertainty_flag depending on scenario

---

## Results

**Final Score: 26 / 36**

| Case                  | Score |
|----------------------|------|
| basic_positive       | 4/4  |
| negative_signal      | 1/4  |
| mixed_sentiment      | 4/4  |
| arabic_query         | 3/4  |
| low_data             | 0/4  |
| garbage_input        | 3/4  |
| conflicting_reviews  | 1/4  |
| specific_feature     | 4/4  |
| price_related        | 4/4  |
| empty_query          | 2/4  |

---

## Observed Strengths

### 1. Grounded Outputs
Using retrieval (FAISS + embeddings), the model consistently generates outputs based on actual review content, reducing hallucinations.

### 2. Structured Output Reliability
All outputs are validated against a strict schema using Pydantic, with retry logic ensuring robustness.

### 3. Multilingual Capability
The system generates both English and Arabic outputs, with Arabic being reasonably fluent and context-aware.

### 4. Strong Performance on Mixed Sentiment
The model performs well when both positive and negative signals exist, extracting balanced pros and cons.

---

## Failure Modes

### 1. Conflicting Reviews
In some cases, the model collapses multiple signals into vague summaries like “okay” instead of explicitly listing pros and cons.

### 2. Overuse of Generic Language
Phrases like “mixed reviews” or “some users find it okay” reduce specificity.

### 3. Uncertainty Calibration
The model occasionally marks outputs as uncertain even when sufficient data is present.

---

## Improvements (Next Iteration)

If given more time, I would:

- Add **contrastive extraction prompts** to force explicit pros/cons in conflicting scenarios
- Introduce **confidence calibration using retrieval density**
- Improve **Arabic generation using specialized prompts or fine-tuning**
- Add **semantic grounding checks using embeddings instead of string matching**
- Cache embeddings to avoid rebuilding FAISS index per query

---

## Conclusion

The system demonstrates strong performance in grounded reasoning, structured outputs, and multilingual generation. While some edge cases reveal limitations in reasoning depth and uncertainty calibration, the core pipeline is robust and production-aligned.