from sqlalchemy import Column, BigInteger, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from src.db.models.base import Base


class File(Base):
    __tablename__ = 'files'

    id = Column(BigInteger, primary_key=True)
    file_name = Column(String(64), nullable=False)
    file_path = Column(Text, nullable=False)
    downloadable = Column(Boolean, default=False)
    user_id = Column(BigInteger, ForeignKey('users.id'))

    user = relationship('User', back_populates='files')

