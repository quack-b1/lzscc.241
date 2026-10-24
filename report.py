import json
import os

RESULTS_FILE = "test_results.json"

def generate_report():
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: {RESULTS_FILE} not found. Run run_tests.py first.")
        return

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n" + "="*40)
    print("      LLM INTERACTION TEST REPORT      ")
    print("="*40)
    
    models = set(d["model"] for d in data)
    for model in models:
        model_data = [d for d in data if d["model"] == model]
        print(f"\nModel: {model}")
        print(f"Total Prompts Evaluated: {len(model_data)}")
        
        categories = set(d["category"] for d in model_data)
        for cat in categories:
            cat_data = [d for d in model_data if d["category"] == cat]
            print(f"  - Category '{cat}': {len(cat_data)} test executions")
            
    print("\nSample Responses:")
    for d in data[:3]:
        print(f"  [ID {d['id']}] ({d['category']}): {d['prompt'][:30]}... -> Response: {d['response'][:50]}...")
    print("="*40)

if __name__ == "__main__":
    generate_report()