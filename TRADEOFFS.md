# Tradeoffs

## Problem Selection

I chose to build a “Moms Verdict” engine that summarizes large volumes of product reviews into structured, multilingual insights.

### Why this problem
- High leverage: product decisions are a core friction point in e-commerce
- Realistic: Mumzworld has multilingual (EN + AR) users and review-heavy products
- AI-appropriate: requires summarization, reasoning, multilingual generation, and uncertainty handling

### Alternatives considered
- Customer support auto-replies → rejected (too common, lower signal)
- Gift recommendation agent → rejected (more UX than reasoning)
- Voice-to-shopping assistant → interesting but harder to evaluate rigorously

---

## 🧰 Tooling

**Models Used**
- gpt-4o-mini → structured reasoning + multilingual generation
- all-MiniLM-L6-v2 → embeddings for retrieval + evaluation

**How I used AI tools**
- ChatGPT: prompt iteration

**What worked**
- Hybrid approach (rules + LLM) improved reliability
- Structured prompts reduced hallucinations

**What didn’t**
- Pure LLM → missed weak signals
- String matching eval → too naive

**Where I intervened**
- Added rule-based signal extraction
- Added semantic similarity scoring
- Tightened prompt constraints

---

## Architecture Decisions

### 1. RAG (Retrieval-Augmented Generation) vs Fine-tuning

**Chosen:** RAG with embeddings + FAISS

**Why:**
- Ensures outputs are grounded in actual reviews
- Works well with small, synthetic datasets
- Easier to debug and evaluate

**Tradeoff:**
- Requires building and querying a vector index
- Slightly higher latency

**Alternative:**
- Fine-tuning a model → rejected due to time constraints and lack of labeled data

---

### 2. FAISS vs Managed Vector DB

**Chosen:** FAISS (local)

**Why:**
- Lightweight and fast to set up
- No external dependencies
- Ideal for prototype within ~5 hours

**Tradeoff:**
- No persistence or scaling features
- Index rebuilt per query in evaluation (inefficient but simple)

**Alternative:**
- Pinecone / Weaviate → better for production, unnecessary for prototype

---

### 3. Sentence-Transformers vs API Embeddings

**Chosen:** sentence-transformers (local model)

**Why:**
- Free and fast
- Avoids API cost
- Good enough semantic quality for short reviews

**Tradeoff:**
- Slightly lower embedding quality vs frontier models

---

### 4. Structured Output with Pydantic

**Chosen:** strict schema validation

**Why:**
- Guarantees consistent output format
- Enables reliable downstream usage
- Aligns with “production-ready” requirement

**Tradeoff:**
- Requires retry logic
- Adds complexity to pipeline

---

### 5. Retry + Fallback Strategy

**Chosen:** up to 3 retries + safe fallback output

**Why:**
- LLMs are not deterministic
- Prevents silent failures
- Ensures system always returns valid output

**Tradeoff:**
- Increased latency in worst case
- More API calls

---

### 6. Multilingual Generation vs Translation

**Chosen:** generate EN + AR directly

**Why:**
- Avoids translation artifacts
- Better aligns with native user experience

**Tradeoff:**
- Harder to control quality
- Arabic fluency depends on model capability

**Alternative:**
- Generate in English → translate → rejected due to lower quality

---

### 7. Evaluation Strategy

**Chosen:** heuristic-based scoring + adversarial test cases

**Why:**
- Fast to implement within time constraint
- Captures key failure modes:
  - grounding
  - uncertainty
  - structured output

**Tradeoff:**
- Heuristic checks (string matching) are imperfect
- Not fully semantic

**Future improvement:**
- Embedding-based similarity for grounding
- LLM-as-judge for reasoning quality

---

### 8. Data Generation (Synthetic)

**Chosen:** Faker-based synthetic dataset

**Why:**
- Avoids scraping (as required)
- Allows control over:
  - noise
  - contradictions
  - multilingual content

**Tradeoff:**
- Less realistic than real-world data
- Limited linguistic diversity

### 9. Hybrid Extraction vs Pure LLM

**Chosen:** Hybrid (rule-based + LLM)

**Why:**
- Prevents loss of weak signals during summarization
- Improves consistency in pros/cons extraction
- Reduces empty outputs in edge cases

**Tradeoff:**
- Slight increase in system complexity
- Requires maintaining keyword lists

**Impact:**
- Significant improvement in evaluation score and grounding reliability

---

## Known Limitations

- Conflicting reviews still sometimes produce minimal extraction (improved but not perfect)
- Confidence score is heuristic, not statistically calibrated
- Arabic output is good but not always native-level nuance
- Rule-based extraction depends on keyword coverage
- FAISS index rebuilt per query (inefficient)

---

## What I Would Build Next (With More Time)

1. Persistent vector store with caching
2. Better uncertainty calibration using:
   - review density
   - sentiment variance
3. Improved extraction using:
   - structured prompting (chain-of-thought internally)
4. Stronger evaluation:
   - semantic grounding checks
   - LLM-based grading
5. UI layer (Streamlit) for interactive demo
6. Real product review dataset integration

---

## Key Insight

The biggest insight from this project was that:

> Pure LLM-based systems tend to lose weak signals during summarization.

By introducing a hybrid approach (rule-based extraction + LLM reasoning), the system became significantly more reliable, especially in edge cases like conflicting reviews.

This reflects a broader principle:
- **LLMs are powerful, but benefit from structured guidance and constraints**

---