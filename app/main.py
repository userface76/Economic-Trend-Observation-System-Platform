from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc, select

from app.database import SessionLocal, init_db
from app.models import DailyReport, StockCandidate


BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="Economic Trend Observation System Platform")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.on_event("startup")
def startup() -> None:
    init_db()


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


@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    with SessionLocal() as db:
        reports = list(db.scalars(select(DailyReport).order_by(desc(DailyReport.report_date)).limit(90)))
    return templates.TemplateResponse("history.html", {"request": request, "reports": reports})

