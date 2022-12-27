from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from src.db.models.base import Base
from src.schemas.user import UserSchema


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    user_path = Column(String(32), nullable=False)

    files = relationship('File')

    def to_user_schema(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username
        )
