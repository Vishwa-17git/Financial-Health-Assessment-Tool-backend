def calculate_metrics(df):
    # Use pandas sums (may return numpy scalar types). Convert to native Python numbers
    revenue = df["Revenue"].sum()
    expenses = df["Expenses"].sum()
    emi = df.get("Loan_EMI", 0).sum()

    # Convert numpy scalars to native Python types (int or float)
    def to_native_number(x):
        try:
            x = float(x)
            if x.is_integer():
                return int(x)
            return round(x, 2)
        except Exception:
            return x

    revenue = to_native_number(revenue)
    expenses = to_native_number(expenses)
    emi = to_native_number(emi)

    profit = revenue - expenses
    profit_margin = (profit / revenue) * 100 if revenue else 0
    cash_flow = profit - emi

    metrics = {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "profit_margin": round(profit_margin, 2),
        "cash_flow": to_native_number(cash_flow),
    }

    return metrics
