import os
from stock_universe import STOCK_UNIVERSE

MOCK_LLM = os.environ.get("MOCK_LLM", "1")

def run_debate(ticker: str):
    """
    Simulates a 3-agent debate (Bull, Bear, Synthesizer) over a specific stock.
    Mock Mode: Uses deterministic f-string templates injecting actual stock metrics.
    """
    data = STOCK_UNIVERSE.get(ticker)
    if not data:
        raise ValueError(f"Ticker {ticker} not found in STOCK_UNIVERSE.")

    beta = data["beta"]
    expected_return = data["analyst_expected_return"]
    std_dev = data["std_dev"]

    if MOCK_LLM == "1":
        bull_arg = (f"BULL AGENT: With an impressive analyst expected return of {expected_return:.1%} "
                    f"against a beta of {beta:.2f}, {ticker} offers highly attractive upside potential. "
                    f"The growth trajectory easily justifies the allocation.")

        bear_arg = (f"BEAR AGENT: I strongly disagree. A standard deviation of {std_dev:.1%} indicates "
                    f"excessive, dangerous volatility. Holding {ticker} introduces far too much uncompensated "
                    f"risk to a stable portfolio under current market conditions.")

        synthesizer_arg = (f"SYNTHESIZER AGENT: This debate highlights a classic high-risk, high-reward dynamic. "
                           f"While the Bull correctly identifies the compelling {expected_return:.1%} expected return, "
                           f"the Bear is right to flag the severe {std_dev:.1%} volatility. Recommendation: "
                           f"Permit allocation only for Aggressive risk profiles, with strict position sizing.")

    else:
        bull_arg = "[LLM generated Bull argument]"
        bear_arg = "[LLM generated Bear argument]"
        synthesizer_arg = "[LLM generated Synthesizer argument]"

    return bull_arg, bear_arg, synthesizer_arg

if __name__ == "__main__":
    target_ticker = "PAYTECH"
    print(f"--- RUNNING 3-AGENT DEBATE FOR {target_ticker} (MOCK_LLM={MOCK_LLM}) ---\n")

    bull, bear, synth = run_debate(target_ticker)

    print(bull)
    print("\n" + bear)
    print("\n" + synth)
    print("-" * 65)
