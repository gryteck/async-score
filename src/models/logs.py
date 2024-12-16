import uuid
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel

from src.models.runs import Status


class Log(BaseModel):
    cadastral_number: int
    run_id: str | None
    status: Status
    error_message: str = ""


class LogResponse(Log):
    id: int
    created_at: datetime = datetime.now(tz=timezone(timedelta(hours=+3)))


class LogsListResponse(BaseModel):
    total_page_count: int
    current_page: int
    logs: list[dict]
