from datetime import datetime

from sqlalchemy import (
    JSON,
    DateTime,
    String,
    func,
    UUID
)
from sqlalchemy.orm import Mapped, mapped_column

from src.utils.postgre_client import Base


class Logs(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)

    cadastral_number: Mapped[int] = mapped_column(nullable=False)
    run_id: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    error_message: Mapped[str] = mapped_column(String(255), nullable=False, default="")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


class Runs(Base):
    __tablename__ = "runs"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    cadastral_number: Mapped[int] = mapped_column(nullable=False)
    params: Mapped[dict] = mapped_column(JSON, nullable=True)
    result: Mapped[float] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    run_type: Mapped[str] = mapped_column(String(255), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
