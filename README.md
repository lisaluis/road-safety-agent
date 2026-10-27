# Road Safety Policy Agent (Task 3)

Analyses the issues in the TOI editorial *"Sense & Licence"* and recommends evidence-based policy options for government, each with justification, expected impact and trade-offs.

## Problem definition
Why do road deaths rise despite stricter rules, and which enforcement-focused policies could reduce them?

## Run it
```
pip install -r requirements.txt
# PowerShell:  $env:GROQ_API_KEY="your_key"      Mac/Linux: export GROQ_API_KEY=your_key
python app.py                       # web page at http://localhost:5000
python agent.py "Your question"     # or run in the terminal
```
Get a free key at console.groq.com. The key is read from the environment and is never stored in this repo.

## Tech stack
| Item | Choice |
|---|---|
| Language | Python 3 |
| LLM | Groq API, `openai/gpt-oss-120b` (JSON mode); override with `GROQ_MODEL` |
| Web layer | Flask (`app.py`) + one HTML page (`agent.html`) |
| Evidence | `facts.json`: 12 sourced facts (ids F1 to F12) |
| Compute | CPU only; the model runs on Groq's servers |

## How it works
question -> load facts -> prompt -> LLM returns JSON -> schema check in code (at least 2 trade-offs per policy) -> display.
The four policy areas are fixed: e-challan recovery linked to renewals, repeat-offender licence suspension, enforcement technology, and awareness campaigns.

## Design principles
- **Evidence-grounded:** only the supplied facts may be used; every policy cites fact ids; no invented statistics.
- **Structured output:** same JSON schema every time, validated in code.
- **Trade-offs mandatory:** each option lists costs, risks and equity or privacy concerns.
- **Human-in-the-loop:** outputs are options for decision-makers, not decisions.
- **Separation of concerns:** `agent.py` (logic) has no web code; `app.py` only exposes it.
- **Secrets:** API key only from the environment.

## Known limitations
- Penalty amounts (F8 to F12) were written from memory and must be verified against the Motor Vehicles (Amendment) Act 2019.
- The model sometimes stretches a claim slightly beyond the facts; the evidence ids make this checkable.
- Answers are qualitative; no impact numbers are invented when the facts do not support them.

## Output
See screenshots: <!-- add screenshots/ images or links here -->
