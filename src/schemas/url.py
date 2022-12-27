from typing import Optional

from pydantic import BaseModel


class CreateUrl(BaseModel):
    public: bool = True
    visibility: bool = True


class UpdateUrl(BaseModel):
    public: Optional[bool] = None
    visibility: Optional[bool] = None


class UrlSchema(CreateUrl):
    id: int
    user_id: int
    short_url: str
    counter: int

    class Config:
        orm_mode = True
