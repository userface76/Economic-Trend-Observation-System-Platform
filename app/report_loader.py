import json
from datetime import date
from pathlib import Path

from sqlalchemy import select

from app.database import SessionLocal
from app.models import DailyReport, StockCandidate


REPORT_DIR = Path(__file__).resolve().parent.parent / "data" / "reports"


def load_bundled_reports() -> None:
    """GitHub에 포함된 날짜별 JSON 리포트를 PostgreSQL에 동기화합니다."""
    if not REPORT_DIR.exists():
        return

    with SessionLocal() as db:
        for path in sorted(REPORT_DIR.glob("*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            report_date = date.fromisoformat(payload["report_date"])
            report = db.scalar(
                select(DailyReport).where(DailyReport.report_date == report_date)
            )
            if report is None:
                report = DailyReport(report_date=report_date)
                db.add(report)

            report.regime = payload["regime"]
            report.summary = payload["summary"]
            report.indicators = payload.get("indicators", [])

            db.query(StockCandidate).filter(
                StockCandidate.report_date == report_date
            ).delete()
            for item in payload.get("candidates", []):
                db.add(StockCandidate(report_date=report_date, **item))

        db.commit()
