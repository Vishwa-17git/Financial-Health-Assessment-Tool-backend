def generate_health_score(metrics):
    score = 0

    if metrics["profit_margin"] > 15:
        score += 30
    elif metrics["profit_margin"] > 8:
        score += 20
    else:
        score += 10

    if metrics["cash_flow"] > 0:
        score += 30
    else:
        score += 10

    if metrics["expenses"] < metrics["revenue"]:
        score += 20

    if metrics["profit"] > 0:
        score += 20

    return min(score, 100)


def generate_insights(metrics):
    """Return simple, deterministic insights derived from computed metrics."""
    insights = []

    pm = metrics.get("profit_margin", 0)
    if pm < 0:
        insights.append("Negative profit margin — consider reducing costs or growing revenue.")
    elif pm < 8:
        insights.append("Profit margin is below target; improve pricing or reduce expenses.")
    elif pm < 15:
        insights.append("Profit margin is moderate; there's room for improvement.")
    else:
        insights.append("Profit margin looks healthy.")

    cf = metrics.get("cash_flow", 0)
    if cf <= 0:
        insights.append("Cash flow is non-positive; review working capital and collection cycles.")
    else:
        insights.append("Cash flow is positive.")

    if metrics.get("expenses", 0) > metrics.get("revenue", 0):
        insights.append("Expenses exceed revenue — this is a risk that needs immediate attention.")

    # Create a concise paragraph
    return " " .join(insights)
