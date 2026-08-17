from model import find_similar_questions

def predict_questions(text, job_role=""):
    results = find_similar_questions(f"{job_role} {text}", top_n=10)

    # Give a useful baseline score even when text similarity is low.
    for item in results:
        item["prediction"] = max(55, min(98, round(55 + item["score"] * 0.45, 1)))

    results.sort(key=lambda x: x["prediction"], reverse=True)
    return results
