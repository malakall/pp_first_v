from app.database import async_session_maker
from sqlalchemy import select, insert, update


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
            

    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()


    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit() 

    @classmethod
    async def update(cls, id_: int, **data):
        """
        Обновление записи по id.
        Пример вызова:
            await HeatmapDAO.update(heatmap.id, image_filename="foo.jpg")
        """
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == id_)
                .values(**data)
                .returning(cls.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()



