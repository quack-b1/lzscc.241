import json
import os

RESULTS_FILE = "test_results.json"

def evaluate_response(category, response):
    response_lower = response.lower()
    
    if category == "unclear":
        has_question = "?" in response
        is_guessing = any(phrase in response_lower for phrase in ["done", "booked", "scheduled", "completed", "here is"])
        return has_question and not is_guessing
        
    elif category == "unanswerable":
        admit_failure = any(word in response_lower for word in ["cannot", "can't", "impossible", "paradox", "contradiction", "unable", "not possible", "un-", "don't know"])
        return admit_failure
        
    elif category == "simple":
        return len(response.strip()) > 0 and "error" not in response_lower
        
    return False

def compute_scores():
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: {RESULTS_FILE} not found.")
        return

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    category_stats = {}
    
    for item in data:
        cat = item["category"]
        passed = evaluate_response(cat, item["response"])
        
        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "passed": 0}
        
        category_stats[cat]["total"] += 1
        if passed:
            category_stats[cat]["passed"] += 1

    print("\n" + "="*40)
    print("          AUTOMATED SCORING RESULTS          ")
    print("="*40)
    
    for cat, stats in category_stats.items():
        score_pct = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        print(f"Category '{cat}': {score_pct:.1f}% pass rate ({stats['passed']}/{stats['total']})")
        
    print("="*40)
    print("Note: Perform a manual qualitative review on at least 20 items.")

if __name__ == "__main__":
    compute_scores()