from dataclasses import dataclass


WEIGHTS = {
    "supply_demand": 25,
    "money_flow": 20,
    "sentiment_gap": 20,
    "bottom_confirmation": 20,
    "financial_safety": 15,
}


@dataclass(frozen=True)
class ScoreResult:
    total: int
    status: str
    detail: dict[str, int]


def score_candidate(metrics: dict[str, float], price_confirmed: bool = False) -> ScoreResult:
    detail = {
        key: round(max(0.0, min(1.0, float(metrics.get(key, 0.0)))) * weight)
        for key, weight in WEIGHTS.items()
    }
    total = sum(detail.values())
    if total >= 80 and price_confirmed:
        status = "확인 후보"
    elif total >= 70:
        status = "관찰 후보"
    else:
        status = "제외"
    return ScoreResult(total=total, status=status, detail=detail)

