from analysis.scoring import score_candidate


def test_confirmed_candidate():
    result = score_candidate({
        "supply_demand": 1,
        "money_flow": 1,
        "sentiment_gap": 1,
        "bottom_confirmation": 1,
        "financial_safety": 1,
    }, price_confirmed=True)
    assert result.total == 100
    assert result.status == "확인 후보"


def test_low_score_is_excluded():
    result = score_candidate({}, price_confirmed=False)
    assert result.total == 0
    assert result.status == "제외"
