import os
from disclosure_snippets import DISCLOSURE_SNIPPETS

MOCK_LLM = os.environ.get("MOCK_LLM", "1")

def extract_signals(snippet: str) -> dict:
    """
    Extracts structured signals from a disclosure text snippet.
    Mock Mode: Uses keyword/regex rules to simulate LLM extraction.
    """
    text = snippet.lower()

    risk_flags = []
    if "litigation" in text:
        risk_flags.append("litigation")
    if "regulatory" in text or "regulator" in text:
        risk_flags.append("regulatory")
    if "customers together account" in text or "concentration" in text:
        risk_flags.append("customer concentration")

    hedging_keywords = ["assuming", "cautiously", "visibility"]
    hedging_detected = any(keyword in text for keyword in hedging_keywords)

    if "confident" in text or "approved" in text:
        sentiment = "confident"
    elif hedging_detected:
        sentiment = "cautious"
    else:
        sentiment = "neutral"

    if MOCK_LLM == "1":
        return {
            "risk_flags": risk_flags,
            "hedging_detected": hedging_detected,
            "sentiment": sentiment
        }
    else:
        return {"error": "Real LLM integration not implemented in this baseline."}

if __name__ == "__main__":
    print(f"--- RUNNING DISCLOSURE EXTRACTION (MOCK_LLM={MOCK_LLM}) ---\n")
    for snippet in DISCLOSURE_SNIPPETS:
        doc_id = snippet.split(":")[0]

        result = extract_signals(snippet)
        print(f"[{doc_id}] Extraction Result:")
        print(result)
        print("-" * 50)
