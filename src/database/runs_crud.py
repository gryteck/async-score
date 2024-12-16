from datetime import datetime, timedelta

from sqlalchemy import select

from src.database.base_crud import BaseCRUD
from src.database.models import Runs
from src.models.runs import Run, Status
from src.utils.postgre_client import async_session_maker


class RunsCRUD(BaseCRUD):
    def __init__(self):
        self.model = Runs

    async def get_by_id(self, model_id):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_cadastral_last_run(self, run_id: str) -> Run:
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .filter_by(id=run_id)
                .order_by(self.model.created_at.desc())
                .limit(1)
            )
            result = await session.execute(query)
            return result.scalars().one_or_none()

    async def get_pending(self):
        async with async_session_maker() as session:
            date_interval = datetime.now() + timedelta(minutes=3)
            query = (
                select(self.model)
                .filter(
                    self.model.start_time < date_interval,
                    self.model.status == Status.scheduled.value,
                )
                .limit(1)
            )
            result = await session.execute(query)
            return result.scalars().one_or_none()
