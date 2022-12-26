from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from src.db.models.base import Base
from src.dto.user import UserDTO


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    urls = relationship('Url')

    def to_user_schema(self) -> UserDTO:
        return UserDTO(
            id=self.id,
            username=self.username
        )
