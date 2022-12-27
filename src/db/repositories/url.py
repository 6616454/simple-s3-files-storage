from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, update

from src.db.models.url import Url
from src.db.repositories.base import BaseRepository


class UrlRepository(BaseRepository[Url]):

    def __init__(self, session: AsyncSession):
        super().__init__(Url, session)

    async def get_url_by_short(
            self,
            short_url: str,
            user_id: int = None
    ) -> Url:
        if user_id:
            query = select(self.model).where(and_(self.model.short_url == short_url, self.model.user_id == user_id))
            return (await self.session.execute(query)).scalar_one_or_none()

        query = select(self.model).where(self.model.short_url == short_url)
        result = (await self.session.execute(query)).scalar_one_or_none()

        return result

    async def create_url(
            self,
            original_url: str,
            short_url: str,
            public: bool,
            visibility: bool,
            user_id: int
    ) -> Url:
        new_url = Url(
            original_url=original_url,
            short_url=short_url,
            public=public,
            visibility=visibility,
            user_id=user_id
        )

        await self.save(new_url)
        await self.commit()
        await self.refresh(new_url)

        return new_url

    async def get_urls_by_user_id(self, user_id: int) -> list[Url]:
        query = select(self.model).where(and_(self.model.user_id == user_id, self.model.visibility == True))
        result = (await self.session.execute(query)).scalars().all()

        return result

    async def update_url(self, short_url: str, user_id: int, **kwargs) -> None:
        query = update(self.model).where(and_(self.model.short_url == short_url, self.model.user_id == user_id)).values(
            kwargs)
        await self.session.execute(query)
        await self.commit()
