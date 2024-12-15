import logging

from fastapi import HTTPException, status
from sqlalchemy import func, insert, select, text

from src.database.models import Logs
from src.models.logs import LogResponse
from src.utils.postgre_client import async_session_maker


class LogsCRUD:
    model = Logs

    async def get_run_log_last(self, run_id: int) -> LogResponse:
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .filter_by(run_id=run_id)
                .order_by(self.model.created_at.desc())
                .limit(1)
            )
            logging.info(query)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    async def get_client_logs_list(self, run_id: int, page_num: int, page_size: int) -> dict:
        async with async_session_maker() as session:
            query = select(func.count(self.model.id)).filter_by(run_id=run_id)
            count = (await session.execute(query)).fetchone()[0]

            total_pages = (  # Расчет общего количества страниц
                int(count / page_size) if count % page_size == 0 else int(count / page_size) + 1
            )

            if page_num > total_pages and total_pages:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="page_num out of total pages range",
                )

            query = (  # Получение данных с учетом пагинации
                select(Logs.__table__.columns)
                .filter_by(run_id=run_id)
                .order_by(Logs.created_at.desc())
                .offset((page_num - 1) * page_size)
                .limit(page_size)
            )
            result = await session.execute(query)
            logs = result.mappings().all()

        return {
            "total_page_count": total_pages,
            "current_page": page_num,
            "logs": logs
        }

    async def add_log(self, **kwargs):
        async with async_session_maker() as session:
            query = insert(self.model).values(**kwargs)
            await session.execute(query)
            await session.commit()
