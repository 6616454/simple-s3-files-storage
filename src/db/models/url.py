from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.db.models.base import Base
from src.dto.url import UrlDTO


class Url(Base):
    __tablename__ = 'urls'

    id = Column(BigInteger, primary_key=True)
    original_url = Column(Text, nullable=False)
    short_url = Column(String(32), nullable=False)
    public = Column(Boolean, default=True)
    visibility = Column(Boolean, default=True)
    counter = Column(BigInteger, default=0)
    user_id = Column(ForeignKey('users.id'))

    user = relationship('User', back_populates='urls')

    def to_url_schema(self):
        return UrlDTO(
            id=self.id,
            original_url=self.original_url,
            short_url=self.short_url,
            public=self.public,
            visibility=self.visibility,
            user_id=self.user_id,
            counter=self.counter
        )
