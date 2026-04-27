import json
from pipeline import (
    load_reviews,
    chunk_reviews,
    create_vector_store,
    retrieve_reviews,
    filter_by_product,
    generate_valid_verdict
)

def load_test_cases(path="../data/test_cases.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_case(case, index, chunks):
    product = case["product"]
    query = case["query"]

    filtered_chunks = filter_by_product(chunks, product)

    if not filtered_chunks:
        return {
            "case": case["name"],
            "score": 0,
            "reason": "No data for product"
        }

    # Build FAISS on filtered chunks
    filtered_index, filtered_chunks, _ = create_vector_store(filtered_chunks)

    results = retrieve_reviews(query, filtered_index, filtered_chunks)

    verdict = generate_valid_verdict(results)

    score = 0

    # Check summary exists
    if verdict.summary_en:
        score += 1

    # Check grounding (simple heuristic)
    review_text = " ".join([r["text"] for r in results]).lower()
    pros_lower = [p.lower() for p in verdict.pros]

    if any(p in review_text for p in pros_lower):
        score += 1

    if len(verdict.pros) > 0 or len(verdict.cons) > 0:
        score += 1

    if "mixed" in verdict.summary_en.lower() and len(verdict.pros) <= 1:
        score -= 1

    # Uncertainty handling
    if case["name"] in ["low_data", "empty_query", "garbage_input"]:
        if verdict.uncertainty_flag:
            score += 1
    else:
        if not verdict.uncertainty_flag:
            score += 1

    return {
        "case": case["name"],
        "score": score,
        "max_score": 4,
        "verdict": verdict.model_dump()
    }

def run_evaluations():
    reviews = load_reviews()
    chunks = chunk_reviews(reviews)

    index, chunks, _ = create_vector_store(chunks)

    test_cases = load_test_cases()

    results = []

    for case in test_cases:
        result = evaluate_case(case, index, chunks)
        results.append(result)

    return results

if __name__ == "__main__":
    results = run_evaluations()

    print("\nEVALUATION RESULTS:\n")

    total = 0
    max_total = 0

    for r in results:
        print(r)
        total += r.get("score", 0)
        max_total += r.get("max_score", 0)

    print(f"\nFinal Score: {total}/{max_total}")