import os
import math
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN
from investor_profiles import INVESTOR_PROFILES

MOCK_LLM = os.environ.get("MOCK_LLM", "1")

def get_stock_data(ticker):
    return STOCK_UNIVERSE[ticker]

def process_investor(profile):
    investor_id = profile["investor_id"]
    risk_tolerance = profile["risk_tolerance"]

    if risk_tolerance == "Conservative":
        tickers = ["PAYBOND", "PAYGOLD", "PAYRETAIL"]
    elif risk_tolerance == "Moderate":
        tickers = ["PAYRETAIL", "PAYINFRA", "PAYGOLD"]
    elif risk_tolerance == "Aggressive":
        tickers = ["PAYTECH", "PAYFIN", "PAYINFRA"]
    else:
        raise ValueError(f"Unknown risk tolerance: {risk_tolerance}")

    portfolio_data = {ticker: get_stock_data(ticker) for ticker in tickers}

    weight = 1.0 / 3.0
    rho = 0.3  
    expected_returns = []
    std_devs = []

    for ticker, data in portfolio_data.items():
        beta = data["beta"]
        sigma = data["std_dev"]
        capm_return = RISK_FREE_RATE + beta * (MARKET_RETURN - RISK_FREE_RATE)
        expected_returns.append(capm_return)
        std_devs.append(sigma)

    port_return = sum(weight * r for r in expected_returns)
    var_individual = sum((weight**2) * (s**2) for s in std_devs)

    cov_sum = 0
    for i in range(3):
        for j in range(i + 1, 3):
            cov_sum += weight * weight * rho * std_devs[i] * std_devs[j]

    port_variance = var_individual + (2 * cov_sum)
    port_std_dev = math.sqrt(port_variance)

    if port_std_dev > 0.20:
        escalation_flag = "ESCALATED_TO_HUMAN_ADVISOR"
    else:
        escalation_flag = "AUTO_FINALIZED"

    if MOCK_LLM == "1":
        if escalation_flag == "ESCALATED_TO_HUMAN_ADVISOR":
            narrative = f"FLAG: {escalation_flag} - Computed portfolio std dev ({port_std_dev:.2%}) exceeds 20% safety limit."
        else:
            narrative = f"For {risk_tolerance} investor {investor_id}, we recommend an allocation across {tickers} with an expected portfolio return of {port_return:.1%} and volatility of {port_std_dev:.1%}."
    else:
        narrative = f"[Real LLM generation logic would trigger here for {investor_id}]"

    return {
        "investor_id": investor_id,
        "escalation_flag": escalation_flag,
        "std_dev": port_std_dev,
        "narrative": narrative
    }

if __name__ == "__main__":
    print(f"--- RUNNING ADVISORY AGENT (MOCK_LLM={MOCK_LLM}) ---\n")
    for profile in INVESTOR_PROFILES:
        result = process_investor(profile)
        print(f"[{result['investor_id']}] Status: {result['escalation_flag']}")
        print(result['narrative'])
        print("-" * 65)
