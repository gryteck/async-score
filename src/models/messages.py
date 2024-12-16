import uuid

from pydantic import BaseModel

from src.models.runs import Status, RunType


class Messages(BaseModel):
    run_id: str
    cadastral_number: int
    params: dict = {}
    status: Status
    run_type: RunType
    result: float | None = None
