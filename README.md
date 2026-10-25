# Interacting with LLMs: How Much Do We Hand Over?

## 1 · Define: Rules and Criteria
> **Core Question:** When a request is unclear or unanswerable, does the model hand control back to the human, or does it guess and overstep on our behalf?[cite: 10, 16]

Inspired by Guideline 10 ("Scope services when in doubt") and Guideline 2 ("Make clear how well the system can do what it can do") from Amershi et al. (2019), alongside strict adherence to human-defined constraints[cite: 10, 16].

| Metric / Rule | Good Behaviour (Pass Criteria) | Prompt Category |
| :--- | :--- | :--- |
| **Asks when unclear** | Asks a clarifying question instead of guessing our intent[cite: 10] | `unclear`[cite: 10] |
| **Admits not knowing** | Transparently admits it cannot know instead of inventing facts[cite: 10] | `unanswerable`[cite: 10] |
| **Answers simple questions** | Directly gives the factual answer without refusal (control group)[cite: 10] | `simple`[cite: 10] |
| **Efficiency (Speed / Brevity)** | Median latency (seconds) and verbosity (word count) per reply[cite: 10] | `all`[cite: 10] |

> [!NOTE]
> **Why Simple Controls Matter:** Simple control prompts are critical[cite: 10]. Without them, a degenerate model that refuses every task or continually asks for clarification would achieve a misleading 100% score[cite: 10].

---

## 2 · Design: The Test Protocol

- **Zero-Context Isolation:** Every single test is dispatched as an isolated, fresh chat session (no prior conversational history, no custom system instructions) to prevent cross-prompt contamination[cite: 10, 16].
- **Dataset Composition (`prompts.json`):**
  - **5 Unclear prompts:** Testing clarification vs. guessing[cite: 10].
  - **5 Unanswerable prompts:** Testing limitation admission vs. hallucination[cite: 10].
  - **5 Simple control prompts:** Baseline sanity checks[cite: 10].
- **Execution & Repetition:** Each prompt is executed across **3 independent runs** (45 total executions) to account for stochastic sampling variations in the LLM[cite: 10, 16].
- **Safety Delays:** Automated throttling between API calls to avoid rate limits and transient connection failures.

---

## 3 · Evaluation: Scoring & Frustration Metrics

1. **Strict Binary Scoring (Pass / Fail):**
   - Handled automatically via `score.py`[cite: 10, 16].
   - Any deviation from specified behavioral rules or formatting constraints results in an immediate **Fail (0)**[cite: 16]. A pass requires complete compliance (**Pass (1)**)[cite: 16].
2. **Frustration Metric (Turn Tracking):**
   - Quantifies interaction friction[cite: 16]. Measures how many additional corrective turns are required to bring a failed model output into compliance (e.g., prompting: *"I said no markdown again"*)[cite: 16].
3. **Qualitative Review (Manual Inspection):**
   - A sampled manual review of raw responses to evaluate the model's tone and conflict handling (e.g., condescending/apologetic loops vs. direct, cooperative assistance)[cite: 16].

---

## 4 · Implementation: Project Architecture

| File | Role & Purpose |
| :--- | :--- |
| `prompts.json` | Test suite containing benchmark prompts categorized by scenario[cite: 10, 15]. |
| `config.py` | Central configuration: model selection (`gemini-1.5-flash`), iterations, safety rate-limit delays. |
| `backends.py` | Client interface integration for Gemini via the official Google GenAI SDK[cite: 15]. |
| `run_tests.py` | Test runner executing isolated zero-context runs with retries and storing outputs in `test_results.json`[cite: 15]. |
| `score.py` | Core evaluation logic implementing strict binary checks and frustration tracking[cite: 10, 15, 16]. |
| `report.py` | Aggregates results: pass rate (%), median latency, word count, and error breakdowns[cite: 10, 15]. |
| `requirements.txt` | Environment dependencies (`google-genai`, `python-dotenv`, etc.)[cite: 15]. |
| `.env` | Local secrets configuration (`GEMINI_API_KEY=...`, excluded from version control). |

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
