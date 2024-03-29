from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response

from robocon_demo_api.config import CONFIG
from robocon_demo_api.models.base import Detail
from robocon_demo_api.models.poem import NewPoem, Poem
from robocon_demo_api.storage.database import (
    delete_poem,
    get_poem,
    get_poems,
    store_poem,
)

poem_router = APIRouter(prefix="/poems")


@poem_router.get(
    "", status_code=200, response_model=list[Poem], operation_id="get_all_poems"
)
def get_poems_() -> list[Poem]:
    return get_poems()


@poem_router.post(
    "", status_code=201, response_model=Poem, responses={422: {"model": Detail}}
)
def create_poem_(new_poem: NewPoem) -> Poem:
    poem = Poem(**new_poem.dict())
    try:
        store_poem(poem)
    except ValueError as exception:
        if exception.args[0] == "AuthorNotFound":
            raise HTTPException(status_code=422, detail=exception.args[1]) from None
    return poem


@poem_router.get(
    "/{poem_id}",
    status_code=200,
    response_model=Poem,
    responses={404: {"model": Detail}},
)
def get_poem_(poem_id: UUID) -> Poem:
    poem = get_poem(poem_id=poem_id)
    if not poem:
        raise HTTPException(
            status_code=404, detail=f"No poem with id {poem_id} found."
        ) from None
    return poem


@poem_router.delete(
    "/{poem_id}",
    status_code=204,
    response_class=Response,
    responses={404: {"model": Detail}},
)
def delete_poem_(poem_id: UUID, request: Request) -> None:
    api_key = request.headers.get("api-key", "")
    if api_key != CONFIG.api_key:
        raise HTTPException(status_code=401)
    if not get_poem(poem_id=poem_id):
        raise HTTPException(
            status_code=404, detail=f"Poem with id {poem_id} not found."
        ) from None
    delete_poem(poem_id=poem_id)
