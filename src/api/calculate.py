import logging
import uuid

from fastapi import APIRouter, Depends, status

from src.models.logs import LogResponse, LogsListResponse
from src.services.calculate import CalculateService
from src.services.runs import RunsService

router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

calculate_service = CalculateService()
run_service = RunsService()


@router.get(
    "/result",
    summary="Вывод логов задачи",
    status_code=status.HTTP_200_OK,
)
async def get_logs_list(result: float = Depends(run_service.get_result)):
    return {"score": result}

@router.post(
    "/calc/",
    summary="Высчитывание скора",
    status_code=status.HTTP_200_OK,
)
async def add_log(run_id: uuid.UUID = Depends(calculate_service.process)):
    return {"id": str(run_id)}
