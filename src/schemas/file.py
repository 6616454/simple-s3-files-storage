from pydantic import BaseModel


class OutputFile(BaseModel):
    id: int
    file_name: str
    file_path: str
    downloadable: bool

    class Config:
        orm_mode = True
