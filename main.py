from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: str

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Config',
                'description': 'Description of the book',
                'rating': 3
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'Udemy', 'A very nice book!', 5),
    Book(2, 'Learning FastAPI', 'Udemy', 'A nice book!', 4),
    Book(3, 'Python', 'Udemy', 'An awesome book!', 3),
    Book(4, 'Book1', 'Author 1', 'None', 2),
    Book(5, 'Book2', 'Author 2', 'None', 1),
]


@app.get('/books')
async def read_all_book():
    return BOOKS


@app.get('/books/{book_id}')
async def read_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return None


@app.get('/books/')
async def read_book_by_rating(book_rating: int):
    lst = []
    for book in BOOKS:
        if book.rating == book_rating:
            lst.append(book)
    return lst


@app.post('/create-book')
async def create_book(new_book: BookRequest):
    new_book = Book(**new_book.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 1 else BOOKS[-1].id + 1
    return book


@app.put('/books/update_book')
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete('/books/{book_id}')
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break