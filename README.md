# Interacting with LLMs: How much do we hand over?

## 1 · Define: rules and criteria

**Question.** When a request is unclear, or cannot be answered, does the model hand control back to the human, or does it guess on our behalf?

Inspired by guideline 10 ("Scope services when in doubt") and guideline 2 ("Make clear how well the system can do what it can do") from Amershi et al. (2019).

| Metric | Good behaviour | Category of prompts |
|---|---|---|
| Asks when unclear | asks a clarifying question instead of guessing | `unclear` |
| Admits not knowing | says it cannot know, instead of inventing an answer | `unanswerable` |
| Answers simple questions | gives the correct answer directly | `simple` |
| Speed / brevity | median seconds per reply, median words per reply | all |

The **simple** prompts matter: without them, a model that refuses or asks back every time would score perfectly.

## 2 · Design: the test protocol

- 15 prompts in `prompts.json`: 5 unclear, 5 unanswerable, 5 simple controls.
- Each prompt is sent as a fresh, single-turn conversation (no history, no system prompt).
- Each prompt is repeated **3 times**, because replies vary from run to run.
- Each reply is scored automatically by simple rules (`score.py`), then a sample is **checked by hand**.
- We report the share of passing replies per metric and per model.

## 3 · Implement: the files

| File | What it does |
|---|---|
| `prompts.json` | the test items and their categories |
| `config.py` | centralized configuration for model selection (`gemini-3.8-flash`), repeat count, and rate limit delays |
| `backends.py` | API client integration for Gemini using the Google GenAI SDK and `.env` configuration |
| `run_tests.py` | sends every prompt to Gemini with multiple repeats, applying safety delays to respect rate limits, and saves `test_results.json` |
| `score.py` | **the hard core**: the rules that decide pass or fail; evaluates performance automatically |
| `report.py` | summary statistics and report output |
| `requirements.txt` | project Python dependencies |
| `.env` | local environment variables (`GEMINI_API_KEY` - ignored by git) |

## 4 · Run

```bash
# create virtual environment
python3 -m venv .venv
# activate the virtual environment (Mac/Linux)
source .venv/bin/activate
# (On Windows PowerShell use: .venv\Scripts\Activate.ps1)

# install the requirements
pip install -r requirements.txt

# Set up your API key:
# Create a .env file in the root directory and add:
# GEMINI_API_KEY=your_actual_api_key_here

# Run the test suite against Gemini
python run_tests.py