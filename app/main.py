import json
from pathlib import Path
from datetime import date

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc, select

from app.database import SessionLocal, init_db
from app.models import DailyReport, StockCandidate
from app.report_loader import load_bundled_reports
from analysis.country_profiles import COUNTRY_PROFILES, TOP_STOCKS


BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="Economic Trend Observation System Platform")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def latest_country_stocks(country: str) -> tuple[list[dict], str | None]:
    """최신 리포트의 TOP 20을 읽고, 없으면 대표 종목 목록을 반환합니다."""
    for path in sorted((BASE_DIR / "data" / "reports").glob("*.json"), reverse=True):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        items = payload.get("top_stocks", {}).get(country, [])
        if items:
            return items[:20], payload.get("report_date")

    fallback = [{
        "rank": rank, "name": name, "ticker": symbol, "current": "업데이트 대기",
        "change_1d": "-", "change_1w": "-", "change_1m": "-",
        "money_flow": "다음 자동 리포트에서 갱신",
        "link": f"https://www.tradingview.com/chart/?symbol={symbol.replace(':', '%3A')}",
    } for rank, (name, symbol) in enumerate(TOP_STOCKS[country], 1)]
    return fallback, None


@app.on_event("startup")
def startup() -> None:
    init_db()
    load_bundled_reports()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    with SessionLocal() as db:
        report = db.scalar(select(DailyReport).order_by(desc(DailyReport.report_date)).limit(1))
        candidates = []
        if report:
            candidates = list(db.scalars(select(StockCandidate).where(StockCandidate.report_date == report.report_date).order_by(desc(StockCandidate.score))))
    return templates.TemplateResponse("dashboard.html", {"request": request, "report": report, "candidates": candidates})


@app.get("/guide", response_class=HTMLResponse)
def guide(request: Request):
    return templates.TemplateResponse("guide.html", {"request": request})


@app.get("/countries", response_class=HTMLResponse)
def countries(request: Request, country: str = "KR"):
    code = country.upper() if country.upper() in COUNTRY_PROFILES else "KR"
    selected = COUNTRY_PROFILES[code]
    stocks, stocks_date = latest_country_stocks(code)
    return templates.TemplateResponse(
        "countries.html",
        {"request": request, "countries": COUNTRY_PROFILES, "selected": selected,
         "stocks": stocks, "stocks_date": stocks_date},
    )


@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    with SessionLocal() as db:
        reports = list(db.scalars(select(DailyReport).order_by(desc(DailyReport.report_date)).limit(90)))
    return templates.TemplateResponse("history.html", {"request": request, "reports": reports})


@app.get("/reports/{report_date}", response_class=HTMLResponse)
def report_detail(request: Request, report_date: date):
    with SessionLocal() as db:
        report = db.scalar(
            select(DailyReport).where(DailyReport.report_date == report_date)
        )
        candidates = []
        if report:
            candidates = list(db.scalars(
                select(StockCandidate)
                .where(StockCandidate.report_date == report.report_date)
                .order_by(desc(StockCandidate.score))
            ))
    return templates.TemplateResponse(
        "report_detail.html",
        {"request": request, "report": report, "candidates": candidates},
        status_code=200 if report else 404,
    )
