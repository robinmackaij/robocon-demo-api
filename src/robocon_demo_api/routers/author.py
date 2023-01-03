from uuid import UUID

from fastapi import APIRouter, HTTPException, Response

from robocon_demo_api.models.base import Detail
from robocon_demo_api.models.author import Author, NewAuthor
from robocon_demo_api.storage.database import get_author, get_authors, store_author


author_router = APIRouter(prefix="/authors")


@author_router.get("/", status_code=200, response_model=list[Author])
def get_authors_() -> list[Author]:
    return get_authors()


@author_router.post("/", status_code=201, response_model=Author)
def create_author_(new_author: NewAuthor) -> Author:
    author = Author(**new_author.dict())
    store_author(author)
    return author


@author_router.get("/{id}", status_code=200, response_model=Author, responses={404: {"model": Detail}})
def get_author_(author_id: UUID) -> Author:
    author = get_author(author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail=f"No author with id {author_id} found.") from None
    return author


# @author_router.delete("/{id}", status_code=204, response_class=Response, responses={404: {"model": Detail}})
# def delete_author_(id_: UUID) -> None:

#         raise HTTPException(status_code=404, detail="Poem not found") from None

#     return None
