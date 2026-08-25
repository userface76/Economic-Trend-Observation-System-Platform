from datetime import date

from sqlalchemy import select

from analysis.market_regime import classify_regime
from analysis.scoring import score_candidate
from app.database import SessionLocal, init_db
from app.models import DailyReport, StockCandidate


SAMPLE_INDICATORS = [
    {"name": "KOSPI", "symbol": "KRX:KOSPI", "change_1d": 0.0},
    {"name": "S&P 500", "symbol": "SP:SPX", "change_1d": 0.0},
    {"name": "USD/KRW", "symbol": "FX_IDC:USDKRW", "change_1d": 0.0},
    {"name": "미국 10년물", "symbol": "TVC:US10Y", "change_1d": 0.0},
    {"name": "VIX", "symbol": "CBOE:VIX", "change_1d": 0.0},
]


def run() -> None:
    init_db()
    today = date.today()
    regime = classify_regime(0.1, 0.1, 0.1)
    sample_score = score_candidate(
        {
            "supply_demand": 0.72,
            "money_flow": 0.64,
            "sentiment_gap": 0.78,
            "bottom_confirmation": 0.70,
            "financial_safety": 0.86,
        },
        price_confirmed=False,
    )

    with SessionLocal() as db:
        existing = db.scalar(select(DailyReport).where(DailyReport.report_date == today))
        if existing:
            existing.regime = regime
            existing.summary = "초기 샘플 리포트입니다. API 키와 실제 시장 데이터 공급원을 연결하세요."
            existing.indicators = SAMPLE_INDICATORS
            db.query(StockCandidate).filter(StockCandidate.report_date == today).delete()
        else:
            db.add(DailyReport(report_date=today, regime=regime, summary="초기 샘플 리포트입니다. API 키와 실제 시장 데이터 공급원을 연결하세요.", indicators=SAMPLE_INDICATORS))

        if sample_score.total >= 70:
            db.add(StockCandidate(
                report_date=today, ticker="SAMPLE", name="분석 구조 확인용 샘플",
                score=sample_score.total, status=sample_score.status,
                current_price=100.0, confirmation_price=105.0, invalidation_price=92.0,
                score_detail=sample_score.detail,
                risk="실제 투자 후보가 아닌 화면 및 데이터베이스 확인용입니다.",
            ))
        db.commit()
    print(f"Daily report created: {today}")


if __name__ == "__main__":
    run()

