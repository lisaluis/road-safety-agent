"""Road-safety policy agent: question -> facts lookup -> policy generation -> validated JSON table.
Setup:  pip install groq
        export GROQ_API_KEY="your_key"   (Colab: use userdata secret, never commit the key)
Run:    python agent.py "Why do road deaths rise despite stricter rules?"
"""
import json, os, sys
from groq import Groq

MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
POLICIES = ["E-challan recovery (link unpaid fines to licence/registration renewal)",
            "Repeat-offender licence suspension",
            "Enforcement technology (cameras, ANPR)",
            "Awareness and attitude campaigns"]
REQUIRED = ["policy", "justification", "evidence", "expected_impact", "trade_offs", "implementation_difficulty"]

SYSTEM = """You are a policy analyst advising Indian officials on road safety.
Rules:
0. Use Indian terms (RTO, Vahan, State transport department), never "DMV".
1. Use ONLY the numbered facts provided. Never invent statistics. Cite fact ids (e.g. F5) in 'evidence'.
2. Every policy MUST have at least 2 trade_offs (costs, risks, equity or privacy concerns).
3. expected_impact is a qualitative judgement; say when evidence is lacking instead of guessing numbers.
4. These are options for human decision-makers, not decisions.
Return ONLY a JSON object: {"issue_analysis": "2-3 sentences", "policies": [ {policy, justification,
evidence (list of strings with fact ids), expected_impact, trade_offs (list), implementation_difficulty (low|medium|high)} ]}"""

def load_facts(path=os.path.join(os.path.dirname(__file__), "facts.json")):
    return json.load(open(path, encoding="utf-8"))

def run(question, client):
    facts = "\n".join(f"{f['id']}: {f['fact']} [{f['source']}]" for f in load_facts())
    user = f"Question: {question}\n\nFacts:\n{facts}\n\nCover exactly these policies:\n- " + "\n- ".join(POLICIES)
    r = client.chat.completions.create(
        model=MODEL, temperature=0.2, response_format={"type": "json_object"},
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}])
    data = json.loads(r.choices[0].message.content)
    for p in data["policies"]:                       # enforce schema
        missing = [k for k in REQUIRED if k not in p]
        assert not missing, f"missing {missing}"
        assert len(p["trade_offs"]) >= 2, "trade-offs required"
    return data

def show(data):
    print("\nISSUE ANALYSIS:", data.get("issue_analysis", ""), "\n")
    for i, p in enumerate(data["policies"], 1):
        print(f"{i}. {p['policy']}  [difficulty: {p['implementation_difficulty']}]")
        print("   Why:      ", p["justification"])
        print("   Evidence: ", "; ".join(p["evidence"]))
        print("   Impact:   ", p["expected_impact"])
        print("   Trade-offs:", " | ".join(p["trade_offs"]), "\n")

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Why do road deaths rise despite stricter rules, and which enforcement policies could reduce them?"
    show(run(q, Groq(api_key=os.environ["GROQ_API_KEY"])))
