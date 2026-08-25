import pandas as pd
from stock_universe import STOCK_UNIVERSE, RISK_FREE_RATE, MARKET_RETURN

def calculate_dcf():
    print("--- PAYTM HYPOTHETICAL BUSINESS LINE DCF VALUATION ---\n")

    ebit = 500.0
    tax_rate = 0.25
    da = 100.0
    capex = 150.0
    delta_nwc = 50.0

    base_fcff = ebit * (1 - tax_rate) + da - capex - delta_nwc
    print(f"Base Year FCFF: ₹{base_fcff:.2f}M")

    payfin_beta = STOCK_UNIVERSE["PAYFIN"]["beta"]  # 1.35
    cost_of_equity = RISK_FREE_RATE + payfin_beta * (MARKET_RETURN - RISK_FREE_RATE)

    cost_of_debt_after_tax = 0.08
    weight_equity = 0.70
    weight_debt = 0.30

    wacc = (weight_equity * cost_of_equity) + (weight_debt * cost_of_debt_after_tax)
    print(f"Calculated WACC: {wacc:.2%}")

    initial_growth_rate = 0.12
    terminal_growth_rate = 0.04 

    assert (wacc - terminal_growth_rate) >= 0.03, "Constraint failed: Terminal growth not 3% below WACC!"

    projected_fcff = [base_fcff * ((1 + initial_growth_rate) ** i) for i in range(1, 6)]

    present_values = [fcff / ((1 + wacc) ** i) for i, fcff in enumerate(projected_fcff, 1)]
    pv_of_explicit_fcff = sum(present_values)

    terminal_value = (projected_fcff[-1] * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)
    pv_of_terminal_value = terminal_value / ((1 + wacc) ** 5)

    implied_ev = pv_of_explicit_fcff + pv_of_terminal_value
    print(f"Implied Enterprise Value (Base Case): ₹{implied_ev:.2f}M\n")

    ebitda = ebit + da
    assumed_multiple = 10.0
    ev_ebitda_valuation = ebitda * assumed_multiple
    print(f"EV/EBITDA Cross-Check Valuation ({assumed_multiple}x EBITDA of ₹{ebitda}M): ₹{ev_ebitda_valuation:.2f}M\n")

    print("--- SENSITIVITY TABLE: IMPLIED EV (Millions INR) ---")
    wacc_adjustments = [-0.01, 0.0, 0.01]
    growth_adjustments = [-0.01, 0.0, 0.01]

    sensitivity_data = []

    for w_adj in wacc_adjustments:
        row = []
        test_wacc = wacc + w_adj
        for g_adj in growth_adjustments:
            test_g = terminal_growth_rate + g_adj

            if test_wacc - test_g < 0.01:
                row.append("ERROR")
                continue

            cell_pvs = [fcff / ((1 + test_wacc) ** i) for i, fcff in enumerate(projected_fcff, 1)]
            cell_tv = (projected_fcff[-1] * (1 + test_g)) / (test_wacc - test_g)
            cell_pv_tv = cell_tv / ((1 + test_wacc) ** 5)
            row.append(f"₹{sum(cell_pvs) + cell_pv_tv:.1f}M")

        sensitivity_data.append(row)

    columns = [f"TG: {terminal_growth_rate + g:.1%}" for g in growth_adjustments]
    index = [f"WACC: {wacc + w:.2%}" for w in wacc_adjustments]
    df_grid = pd.DataFrame(sensitivity_data, index=index, columns=columns)
    print(df_grid.to_string())

if __name__ == "__main__":
    calculate_dcf()
