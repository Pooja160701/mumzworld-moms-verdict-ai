# 🛍️ Mumzworld Moms Verdict AI

An AI-powered system that transforms hundreds of noisy product reviews into a structured, trustworthy **“Moms Verdict”** — in both **English and Arabic**.

---

## 🚀 One-Line Summary

Given raw product reviews, this system generates a **grounded, multilingual, structured verdict** with pros, cons, and confidence — helping moms make faster, better decisions.

---

## 🎯 Problem

E-commerce platforms like Mumzworld contain hundreds of reviews per product:
- Mixed opinions
- Multiple languages (EN + AR)
- No clear summary

👉 Users must manually read and interpret everything.

---

## 💡 Solution

This project builds a **RAG-based AI system** that:

1. Retrieves relevant reviews
2. Extracts key insights (pros, cons, issues)
3. Generates a structured verdict
4. Outputs in **English + Arabic**
5. Handles uncertainty explicitly

## 🧠 Key Innovation

This system uses a **hybrid approach (rule-based + LLM)**:

- Pre-extracts signals (e.g., "durable", "broke", "expensive") from reviews
- Forces the LLM to ground outputs in real evidence
- Cleans and normalizes extracted terms for consistency

👉 This significantly improves:
- Reliability
- Grounding
- Performance on conflicting reviews

---

## 🧠 Example Output

```json
{
  "summary_en": "The baby stroller is durable and of good quality, though some users find it only average.",
  "summary_ar": "عربة الأطفال متينة وذات جودة جيدة، لكن بعض المستخدمين يرونها عادية.",
  "pros": ["Durable", "Good quality"],
  "cons": ["Average performance"],
  "confidence_score": 0.8,
  "uncertainty_flag": false
}
```

---

## 🏗️ Architecture

```
User Query
    ↓
Review Dataset (Synthetic, EN + AR)
    ↓
Chunking
    ↓
Embeddings (Sentence Transformers)
    ↓
FAISS Vector Store
    ↓
Retriever (Top-K reviews)
    ↓
LLM (gpt-4o-mini)
    ↓
Structured Output (JSON)
    ↓
Validation (Pydantic)
    ↓
Post-Processing (cleaned outputs)
    ↓
Retry + Fallback
```

---

## ⚙️ Tech Stack

* Python
* FAISS (vector search)
* Sentence Transformers (embeddings)
* OpenAI (LLM)
* Pydantic (schema validation)
* Faker (data generation)

---

## 📦 Setup (Under 5 Minutes)

### 1. Clone repo

```bash
git clone https://github.com/YOUR_USERNAME/mumzworld-moms-verdict-ai.git
cd mumzworld-moms-verdict-ai
```

---

### 2. Create environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add API key

Create `.env`:

```
OPENAI_API_KEY=your_key_here
```

---

### 5. Generate dataset

```bash
cd scripts
python generate_data.py
```

---

### 6. Run pipeline

```bash
cd ../app
python pipeline.py
```

---

### 7. Run evaluation

```bash
python evaluator.py
```

Expected output:

* Prints structured verdicts
* Shows final score

---

## 📊 Evaluation

* 10 test cases (including adversarial inputs)
* Metrics:

  * Groundedness
  * Structured output validity
  * Uncertainty handling
  * Extraction quality

**Final Score: 30 / 45 (with stricter semantic evaluation)**

> Note: The evaluation was upgraded from simple string matching to semantic similarity and stricter extraction rules, resulting in more realistic and challenging scoring.

See [`EVALS.md`](./EVALS.md) for full details.

---

## ⚠️ Failure Modes

* Conflicting reviews may produce generic summaries
* Uncertainty calibration is heuristic
* Arabic output is good but not always native-level nuance

---

## 🔁 Tradeoffs

See [`TRADEOFFS.md`](./TRADEOFFS.md)

Highlights:

* RAG over fine-tuning for groundedness
* FAISS for simplicity over scalability
* Structured output over free-form generation

---

## 🧪 Tooling

* OpenAI API (gpt-4o-mini) for reasoning
* Sentence Transformers for embeddings
* Local FAISS index for retrieval

Used for:

* Prompt iteration
* Output validation
* Evaluation

---

## ⏱️ Time Log

- Problem selection: 45 mins
- Data + pipeline: 2 hours
- Evaluation system: 1.5 hours
- Prompt + scoring improvements: 1 hour
- Documentation: 45 mins

---

## 🤖 AI Usage Note

Used ChatGPT for:
- Prompt engineering
- Debugging pipeline issues

Used sentence-transformers for embeddings.
Used OpenAI API for structured reasoning.

---

### 📈 Iteration Progress

| Version | Score |
|--------|------|
| v1 (baseline) | 26 / 36 |
| v2 (improved eval + hybrid extraction) | 30 / 45 |

Key improvements:
- Added semantic grounding (embeddings)
- Added rule-based signal extraction
- Reduced vague summaries
- Improved uncertainty handling

---

## 📌 Key Takeaways

- Hybrid systems (rule-based + LLM) significantly improve reliability over pure prompting
- Grounded AI systems outperform free-form generation
- Evaluation design directly impacts perceived model performance
- Explicit uncertainty handling improves user trust

---

## 🚀 What I Would Build Next

* Persistent vector DB (Pinecone / Weaviate)
* Better Arabic fluency tuning
* Confidence calibration using signal density
* UI (Streamlit) for real-time demo

---

## 🎥 Demo

(Link Balance: )

---

## 🙌 Submission

Track A: AI Engineering Intern

---