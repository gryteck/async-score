import enum
import uuid

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


class Messages(BaseModel):
    run_id: uuid.UUID
    cadastral_number: int
    params: dict = {}
    status: Status
    run_type: RunType
    result: float | None
