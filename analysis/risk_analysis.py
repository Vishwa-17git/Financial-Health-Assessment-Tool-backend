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
