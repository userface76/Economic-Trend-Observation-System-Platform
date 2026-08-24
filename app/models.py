from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DailyReport(Base):
    __tablename__ = "daily_reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_date: Mapped[date] = mapped_column(Date, unique=True, index=True)
    regime: Mapped[str] = mapped_column(String(20))
    summary: Mapped[str] = mapped_column(Text)
    indicators: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StockCandidate(Base):
    __tablename__ = "stock_candidates"
    id: Mapped[int] = mapped_column(primary_key=True)
    report_date: Mapped[date] = mapped_column(Date, index=True)
    ticker: Mapped[str] = mapped_column(String(30), index=True)
    name: Mapped[str] = mapped_column(String(100))
    score: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20))
    current_price: Mapped[float] = mapped_column(Float)
    confirmation_price: Mapped[float] = mapped_column(Float)
    invalidation_price: Mapped[float] = mapped_column(Float)
    score_detail: Mapped[dict] = mapped_column(JSON)
    risk: Mapped[str] = mapped_column(Text)

