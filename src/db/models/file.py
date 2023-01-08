from sqlalchemy import Column, BigInteger, Text, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from src.db.models.base import Base
from src.schemas.file import OutputFile


class File(Base):
    __tablename__ = 'files'

    id = Column(BigInteger, primary_key=True)
    file_name = Column(String(64), nullable=False)
    file_path = Column(Text, nullable=False, unique=True)
    downloadable = Column(Boolean, default=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='files')

    def to_file_schema(self):
        return OutputFile(
            id=self.id,
            file_name=self.file_name,
            file_path=self.file_path,
            downloadable=self.downloadable
        )

