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
from analysis.country_profiles import COUNTRY_PROFILES


BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="Economic Trend Observation System Platform")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


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
    selected = COUNTRY_PROFILES.get(country.upper(), COUNTRY_PROFILES["KR"])
    return templates.TemplateResponse(
        "countries.html",
        {"request": request, "countries": COUNTRY_PROFILES, "selected": selected},
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
