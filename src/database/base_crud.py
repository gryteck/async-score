from sqlalchemy import select, insert, update, delete
from src.utils.postgre_client import Base

from src.utils.postgre_client import async_session_maker


class BaseCRUD:
    model = Base

    @classmethod
    async def add(cls, **kwargs):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, model_id, **kwargs):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == model_id).values(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, model_id, **kwargs):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == model_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_by_id(cls, model_id) -> model:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, **kwargs) -> model:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **kwargs):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**kwargs).order_by(cls.model.id.asc())

            result = await session.execute(query)
            return result.scalars().all()
