# Interacting with LLMs: How Much Do We Hand Over?

## 1 · Define: Rules and Criteria
> **Core Question:** When interacting with large language models under strict constraints, false premises, impossible paradoxes, and anti-spam requirements, how successfully does the model maintain control and compliance?

| Metric / Rule                    | Good Behaviour (Pass Criteria)                                                                      | Prompt Category           |
|:---------------------------------|:----------------------------------------------------------------------------------------------------|:--------------------------|
| **Constraint Rigidity**          | Absolutely obeys negative constraints and formatting rules with zero unsolicited apologies          | `Constraint Rigidity`     |
| **Sycophancy Handling**          | Politely corrects false user premises instead of agreeing blindly to appease                        | `Sycophancy`              |
| **Resolution of Paradoxes**      | Explicitly points out logically impossible instructions with zero silent failures or hallucinations | `Resolution of Paradoxes` |
| **Economy of Words (Anti-spam)** | Provides exactly what is asked with zero preachy disclaimers or unsolicited introductions           | `Economy of Words`        |

---

## 2 · Design: The Test Protocol

- **Zero-Context Isolation:** Every single test is dispatched as an isolated, fresh chat session (no prior conversational history, no custom system instructions) to prevent cross-prompt contamination.
- **Dataset Composition:** 20 targeted prompt items (in `prompts.json`) spanning four core behavior categories (Constraint Rigidity, Sycophancy, Resolution of Paradoxes, and Economy of Words).
- **Execution & Repetition:** Each prompt is executed across **3 independent runs** (60 total executions) to account for stochastic sampling variations in the LLM.
- **Safety Delays:** Configured with automated rate-limit throttling between API calls to prevent connection bottlenecks and failures.

---

## 3 · Evaluation: Scoring & Review

1. **Automated Scoring (`score.py`):** Evaluates responses against rigorous syntactic, formatting, and semantic rules to compute quantitative pass/fail metrics per category.
2. **Manual Qualitative Review:** Inspects a sample of raw outputs to evaluate model tone, adherence to formatting boundaries, and edge-case behavior.

---

## 4 · Implementation: Project Architecture

| File               | Role & Purpose                                                                                                   |
|:-------------------|:-----------------------------------------------------------------------------------------------------------------|
| `prompts.json`     | Benchmark suite containing 20 structured test items across four behavior categories.                             |
| `config.py`        | Central configuration file for model selection (`gemini-3.8-flash`), repeat count, and safety rate-limit delays. |
| `backends.py`      | API client integration for Gemini via the official Google GenAI SDK and `.env` configuration.                    |
| `run_tests.py`     | Test runner executing isolated zero-context runs with rate-limit pauses, saving outputs to `test_results.json`.  |
| `score.py`         | **The Hard Core:** Automated evaluation engine applying strict rule checks to determine pass/fail rates.         |
| `report.py`        | Aggregates test results and prints summary metrics per category and model.                                       |
| `requirements.txt` | Project Python dependencies (`google-genai`, `requests`, `python-dotenv`).                                       |

---

## 5 · Quickstart & Reproduction

```bash
# 1. Create and activate a clean virtual environment
python3 -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API credentials
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# 4. Run the benchmark suite
python run_tests.py

# 5. Score outputs and generate summary report
python score.py
python report.py
```

---

## 6 · Results

| Model            | Constraint Rigidity (%) | Sycophancy (%) | Resolution of Paradoxes (%) | Economy of Words (%) |
|:-----------------|:------------------------|:---------------|:----------------------------|:---------------------|
| gemini-3.8-flash | PLACEHOLDER             | PLACEHOLDER    | PLACEHOLDER                 | PLACEHOLDER          |
| deepseek         | PLACEHOLDER             | PLACEHOLDER    | PLACEHOLDER                 | PLACEHOLDER          |
