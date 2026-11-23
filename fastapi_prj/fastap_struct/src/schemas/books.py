from pydantic import BaseModel



class BookSchema(BaseModel):
    title: str
    author: str
    published: int


class BookGetSchema(BaseModel):
    id: int
    title: str
    author: str
    published: int
