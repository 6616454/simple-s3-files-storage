from typing import TypeVar, Type, Generic

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.infrastructure.db.base import Base

Model = TypeVar('Model', bound=Base)


class BaseRepository(Generic[Model]):

    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id_: int):
        query = select(self.model).where(self.model.id == id_)
        return (await self.session.execute(query)).scalar_one_or_none()

    async def get_all(self) -> list[Model]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def update_obj(self, id_: int, **kwargs) -> None:
        query = update(self.model).where(self.model.id == id_).values(
            kwargs)
        await self.session.execute(query)
        await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def save(self, obj: Model) -> None:
        self.session.add(obj)

    async def delete(self, obj: Model) -> None:
        await self.session.delete(obj)

    async def refresh(self, obj: Model) -> None:
        await self.session.refresh(obj)
