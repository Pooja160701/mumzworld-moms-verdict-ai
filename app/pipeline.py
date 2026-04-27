import json
import faiss
import os
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
from schema import MomsVerdict

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_reviews(path="../data/raw_reviews.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def chunk_reviews(reviews, chunk_size=200):
    chunks = []

    for r in reviews:
        text = r["text"]
        for i in range(0, len(text), chunk_size):
            chunks.append({
                "review_id": r["review_id"],
                "product": r["product"],
                "text": text[i:i+chunk_size],
                "language": r["language"]
            })

    return chunks

def create_vector_store(chunks):
    texts = [c["text"] for c in chunks]

    embeddings = model.encode(texts, show_progress_bar=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, chunks, embeddings

def retrieve_reviews(query, index, chunks, top_k=5):
    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    return results

def filter_by_product(chunks, product_name):
    return [c for c in chunks if c["product"] == product_name]

def extract_signals(reviews):
    pros = set()
    cons = set()

    POSITIVE = ["good", "durable", "comfortable", "excellent", "value"]
    NEGATIVE = ["poor", "bad", "broke", "expensive", "okay", "average"]

    for r in reviews:
        text = r["text"].lower()

        for word in POSITIVE:
            if word in text:
                pros.add(word)

        for word in NEGATIVE:
            if word in text:
                cons.add(word)

    return list(pros), list(cons)

def extract_json(response_text):
    try:
        # Remove markdown code fences if present
        cleaned = re.sub(r"```json|```", "", response_text).strip()

        # Ensure it looks like a valid JSON object before parsing
        if cleaned.startswith("{") and cleaned.endswith("}"):
            return json.loads(cleaned)

        return None

    except Exception:
        return None
    
def validate_output(data):
    try:
        return MomsVerdict(**data)
    except Exception as e:
        return None

def add_sentiment_signal(reviews):
    signals = []
    for r in reviews:
        text = r["text"].lower()
        if any(word in text for word in ["good", "durable", "comfortable", "excellent"]):
            signals.append("positive")
        elif any(word in text for word in ["poor", "bad", "broke", "expensive"]):
            signals.append("negative")
        else:
            signals.append("neutral")
    return signals

def generate_verdict(retrieved_reviews):
    sentiments = add_sentiment_signal(retrieved_reviews)
    pre_pros, pre_cons = extract_signals(retrieved_reviews)

    context = "\n".join([
        f"Review {i+1} ({sentiments[i]}): {r['text']}"
        for i, r in enumerate(retrieved_reviews)
    ])

    prompt = f"""
You are an expert shopping assistant for moms.

Analyze the following product reviews and generate a structured verdict.

STRICT RULES:
- Use ONLY the provided reviews
- Do NOT hallucinate or invent information
- Every claim MUST be supported by at least one review
- If information is missing → say "I don't know"

UNCERTAINTY:
- Set uncertainty_flag = true ONLY if:
  - Reviews are insufficient OR
  - Strong contradictions exist across reviews
- Otherwise set it to false

MANDATORY EXTRACTION RULES:
- You MUST extract relevant insights from the reviews
- If ANY positive signal exists → include it in pros
- If ANY negative signal exists → include it in cons
- If BOTH exist → include BOTH pros AND cons

STRICT:
- Returning empty pros AND cons is NOT allowed unless ALL reviews are empty or meaningless
- Do NOT ignore weak signals — extract even small evidence

CONFLICT RESOLUTION:
- If reviews contain conflicting opinions:
  - Explicitly list BOTH positive and negative aspects
  - Do NOT summarize as "okay" or "mixed" without listing reasons

QUALITY:
- Be specific and concrete
- Avoid vague phrases like "mixed reviews" unless followed by clear reasons
- Prefer short, factual phrases over generic statements

GROUNDING:
- Every pro and con must directly reflect wording from the reviews
- Do NOT generalize beyond what is written

CONFIDENCE:
- High (0.8–1.0): consistent positive or negative signals
- Medium (0.5–0.8): mixed signals
- Low (0.0–0.5): weak or insufficient evidence

PRE-EXTRACTED SIGNALS (from reviews):
pros: {pre_pros}
cons: {pre_cons}

IMPORTANT:
- You MUST include these signals in final output if they are relevant
- Do NOT ignore them

REVIEWS:
{context}

Return ONLY valid JSON with:
summary_en, summary_ar, pros, cons, common_issues,
recommended_age, confidence_score, uncertainty_flag

Do not include markdown.
Do not include explanations.

Ensure Arabic output is natural and fluent, not literal translation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

def generate_valid_verdict(retrieved_reviews, max_retries=3):
    for attempt in range(max_retries):
        raw_output = generate_verdict(retrieved_reviews)

        json_data = extract_json(raw_output)

        if not json_data:
            print(f"Retry {attempt+1}: JSON extraction failed")
            continue

        validated = validate_output(json_data)
        validated.pros = clean_terms(validated.pros)
        validated.cons = clean_terms(validated.cons)

        if validated:
            return validated

        print(f"Retry {attempt+1}: Schema validation failed")

    # FINAL FALLBACK
    return MomsVerdict(
        summary_en="I don't know",
        summary_ar="لا أعرف",
        pros=[],
        cons=[],
        common_issues=[],
        recommended_age="I don't know",
        confidence_score=0.0,
        uncertainty_flag=True
    )

def clean_terms(terms):
    return [t.lower().strip().replace("this baby stroller is ", "") for t in terms]

if __name__ == "__main__":
    reviews = load_reviews()
    chunks = chunk_reviews(reviews)

    product = "Baby Stroller"

    filtered_chunks = filter_by_product(chunks, product)

    index, filtered_chunks, embeddings = create_vector_store(filtered_chunks)

    query = "Is this stroller durable and good quality?"
    results = retrieve_reviews(query, index, filtered_chunks)
    verdict = generate_valid_verdict(results)

    print("\nRetrieved Reviews:\n")
    print("\nFinal Structured Verdict:\n")
    print(verdict.model_dump())
    for r in results:
        print(r["text"])