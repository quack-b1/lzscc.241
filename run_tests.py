import json
import os
import time
from backends import GeminiBackend
from config import REPEATS, DELAY_SECONDS, SELECTED_MODEL

PROMPTS_FILE = "prompts.json"
OUTPUT_FILE = "test_results.json"


def run_evaluation():
    if not os.path.exists(PROMPTS_FILE):
        print(f"Error: {PROMPTS_FILE} not found.")
        return

    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        test_prompts = json.load(f)

    backend = GeminiBackend()
    results = []

    print(f"Starting test run using model '{SELECTED_MODEL}' ({REPEATS} repeats per prompt)...")

    for item in test_prompts:
        prompt_id = item["id"]
        category = item["category"]
        prompt_text = item["prompt"]

        for rep in range(1, REPEATS + 1):
            print(f"Testing Prompt ID {prompt_id} [{category}] - Repeat {rep}/{REPEATS}")
            start_time = time.time()
            response = backend.generate(prompt_text)
            duration = time.time() - start_time

            results.append({
                "id": prompt_id,
                "category": category,
                "prompt": prompt_text,
                "repeat": rep,
                "response": response,
                "latency_seconds": round(duration, 3),
                "model": SELECTED_MODEL
            })

            # Pause to respect rate limits
            time.sleep(DELAY_SECONDS)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Test run complete. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_evaluation()