from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.orm import relationship

from src.db.models.base import Base


class File(Base):
    __tablename__ = 'files'

    id = Column(BigInteger, primary_key=True)
    file_path = Column(Text, nullable=False)

    url = relationship('Url')
    user = relationship('User', back_populates='files')
