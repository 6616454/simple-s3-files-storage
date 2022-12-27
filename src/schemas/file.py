from pydantic import BaseModel


class OutputFile(BaseModel):
    id: int
    filename: str
    file_path: str

    class Config:
        orm_mode = True
