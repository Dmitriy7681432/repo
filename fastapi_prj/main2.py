# -*- coding: utf-8 -*-
import asyncio
from fastapi import FastAPI,HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Асинхронность в Python",
        "author": "Мэттью"
    },
    {
        "id": 2,
        "title": "Backend разработка на Python",
        "author": "Артем"
    },
]

@app.get("/books", tags=["Книги 📚"], summary="Получить все книги")
def read_books():
    return books

@app.get("/books/{book_id}",tags=["Книги 📚"], summary="Получить конкретную книгу")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")

class NewBook(BaseModel):
    title: str
    author: str

@app.post("/books",tags=["Книги 📚"])
def create_books(new_book: NewBook):
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author,
    })
    return {"succeess": True, "message": "Книга успешно добавлена"}


if __name__ == "__main__":
    uvicorn.run("main2:app", reload=True)
