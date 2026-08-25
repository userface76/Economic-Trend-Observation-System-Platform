def classify_regime(growth_score: float, inflation_score: float, liquidity_score: float) -> str:
    """각 입력은 -1(약함)~1(강함). 간단한 초기 국면 분류기입니다."""
    momentum = growth_score + liquidity_score
    if momentum >= 0.6 and inflation_score <= 0.5:
        return "확장"
    if momentum >= 0:
        return "회복"
    if growth_score > -0.5:
        return "둔화"
    return "수축"

