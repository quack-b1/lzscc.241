# Interacting with LLMs: How Much Do We Hand Over?

## 1 · Define: Rules and Criteria

When a request is unclear or unanswerable, does the model hand control back to the human, or does it guess on our behalf?

Inspired by Guideline 10 (*"Scope services when in doubt"*) and Guideline 2 (*"Make clear how well the system can do what it can do"*) from Amershi et al. (2019).

| Metric | Good behaviour | Prompt category |
|---|---|---|
| Asks when unclear | Asks a clarifying question instead of guessing | Unclear |
| Admits not knowing | Says it cannot know, instead of inventing an answer | Unanswerable |
| Answers simple questions | Gives the correct answer directly | Simple |
| Speed / brevity | Median seconds per reply, median words per reply | All |

> [!NOTE]
> The simple prompts matter: without them, a model that refused or asked back every time would score perfectly.

## 2 · Design: The Test Protocol

- **15 prompts** in `prompts.json`: 5 unclear, 5 unanswerable, and 5 simple controls.
- Each prompt is sent as a **fresh, single-turn conversation** (no history, no system prompt).
- Each prompt is **repeated 3 times**, because replies vary from run to run.
- Each reply is **scored automatically** by simple rules (`score.py`), then a sample is checked by hand.
- We report the **share of passing replies** per metric and per model.

## 3 · Implement: The Files

| File | What it does |
|---|---|
| `prompts.json` | The test items and their categories |
| `config.py` | Centralized configuration for model selection (`gemini-3.8-flash`), repeat count, and rate-limit delays |
| `backends.py` | API client integration for Gemini using the Google GenAI SDK and `.env` configuration |
| `run_tests.py` | Sends every prompt to Gemini with multiple repeats, applies safety delays to respect rate limits, and saves `test_results.json` |
| `score.py` | The hard core: the rules that decide pass or fail; evaluates performance automatically |
| `report.py` | Summary statistics and report output |
| `requirements.txt` | Project Python dependencies |
| `.env` | Local environment variables (`GEMINI_API_KEY`; ignored by Git) |

## 4 · Run

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment (macOS/Linux)
source .venv/bin/activate
# (On Windows PowerShell, use: .venv\Scripts\Activate.ps1)

# Install the requirements
pip install -r requirements.txt
```

Set up your API key by creating a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

Run the test suite against Gemini:

```bash
python run_tests.py
```


