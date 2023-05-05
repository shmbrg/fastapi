from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from fastapi import FastAPI, HTTPException, Request, status, Form, Header


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of book", min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "c4e81260-40b3-422b-994a-86cabb82ec74",
                "title": "Computer Science Pro",
                "author": "Coding with Seb",
                "description": "A very nice description of a book!",
                "rating": 60
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, title="Description of book", min_length=1, max_length=100)


books = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f'Hey, why do you want {exception.books_to_return} '
                            f'books? You need to read more!'}
    )


@app.post("/books/login")
async def book_login(username: str = Form(...), password: str = Form(...)):
    return {
        "username": username,
        "password": password
    }


# fake authentication (home assignment)
@app.post("/books/login/{book_id}")
async def book_login_auth(book_id: int,
                          username: Optional[str] = Header(None),
                          password: Optional[str] = Header(None)):
    if username == "FastAPIUser" and password == "Test1234!":
        return books[book_id]
    return "Invalid user"


@app.post("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header}


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(books) < 1:
        create_books_no_api()

    if books_to_return and 0 < books_to_return <= len(books):
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(books[i-1])
            i += 1
        return new_books
    return books


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in books:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in books:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    books.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in books:
        counter += 1
        if x.id == book_id:
            books[counter-1] = book
            return books[counter-1]
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in books:
        counter += 1
        if x.id == book_id:
            del books[counter-1]
            return f'ID:{book_id} deleted'
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id="c4e81260-40b3-422b-994a-86cabb82ec74",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="24e81260-40b3-422b-994a-86cabb82ec74",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=70)
    book_3 = Book(id="34e81260-40b3-422b-994a-86cabb82ec74",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)
    book_4 = Book(id="44e81260-40b3-422b-994a-86cabb82ec74",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=90)
    books.append(book_1)
    books.append(book_2)
    books.append(book_3)
    books.append(book_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={"X-Header-Error": "Nothing to be seen at the UUID"})