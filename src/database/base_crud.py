from sqlalchemy import delete, insert, select, update

from src.utils.postgre_client import async_session_maker


class BaseCRUD:
    model = None

    async def add(self, **kwargs):
        async with async_session_maker() as session:
            query = insert(self.model).values(**kwargs)
            await session.execute(query)
            await session.commit()

    async def update(self, model_id, **kwargs):
        async with async_session_maker() as session:
            query = update(self.model).filter_by(id=model_id).values(**kwargs)
            await session.execute(query)
            await session.commit()

    async def delete(self, model_id: int, **kwargs):
        async with async_session_maker() as session:
            query = delete(self.model).filter_by(id=model_id)
            await session.execute(query)
            await session.commit()

    async def get_by_id(self, model_id):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_one_or_none(self, **kwargs) -> model:
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def find_all(self, **kwargs):
        async with async_session_maker() as session:
            query = select(self.model).filter_by(**kwargs).order_by(self.model.id.asc())

            result = await session.execute(query)
            return result.scalars().all()
