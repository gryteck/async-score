import enum
import uuid
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel


class RunType(str, enum.Enum):
    """
    Виды запусков (может дополняться с новым функционалом)
    """
    calculate = "calculate"


class Status(str, enum.Enum):
    scheduled = "scheduled"
    processing = "processing"
    finished = "finished"
    failed = "failed"


class Run(BaseModel):
    id: uuid.UUID = None
    cadastral_number: int = None
    params: dict = {}
    status: Status = None
    run_type: RunType = None
    result: float = None
    start_time: datetime = None
