from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, Query, Request, Response, UploadFile
from fastapi.responses import FileResponse

from robocon_demo_api.config import CONFIG
from robocon_demo_api.models.author import Author, AuthorResource
from robocon_demo_api.models.base import Detail
from robocon_demo_api.storage.database import (
    delete_author,
    get_author,
    get_authors,
    get_poems,
    store_author,
)

PORTRAITS_FOLDER = CONFIG.portraits_path

author_router = APIRouter(prefix="/authors")


@author_router.get("", status_code=200, response_model=list[AuthorResource])
def get_authors_() -> list[AuthorResource]:
    return get_authors()


@author_router.post("", status_code=201, response_model=AuthorResource)
def create_author_(new_author: Author) -> AuthorResource:
    author = AuthorResource(**new_author.dict())
    store_author(author)
    return author


@author_router.get(
    "/{author_id}",
    status_code=200,
    response_model=AuthorResource,
    responses={404: {"model": Detail}},
)
def get_author_(
    author_id: UUID = Path(title="The ID of the author to get."),
) -> AuthorResource:
    author = get_author(author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=404, detail=f"No author with id {author_id} found."
        ) from None
    return author


@author_router.get(
    "/{author_id}/portraits",
    status_code=200,
    responses={404: {"model": Detail}},
)
def get_author_portrait_(
    author_id: UUID,
) -> FileResponse:
    author = get_author(author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=404, detail=f"No author with id {author_id} found."
        ) from None
    portrait_file_paths = [
        path
        for path in PORTRAITS_FOLDER.iterdir()
        if path.is_file() and path.name.startswith(f"{author_id}_portrait")
    ]
    if not portrait_file_paths:
        raise HTTPException(
            status_code=404, detail=f"No portrait for author with id {author_id} found."
        ) from None
    return FileResponse(portrait_file_paths[0])


@author_router.delete(
    "/{author_id}",
    status_code=204,
    response_class=Response,
    responses={404: {"model": Detail}},
)
def delete_author_(author_id: UUID, request: Request) -> None:
    api_key = request.headers.get("api-key", "")
    if api_key != CONFIG.api_key:
        raise HTTPException(status_code=401)
    author = get_author(author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=404, detail=f"Author with id {author_id} not found."
        ) from None
    if author.name == "unknown author" and author.species == "unknown":
        raise HTTPException(
            status_code=403,
            detail="The 'unknown author' cannot be deleted.",
        )
    if get_poems(author_id=author_id):
        raise HTTPException(
            status_code=403,
            detail=f"Cannot delete author with id {author_id}: There are poems associated with this author.",
        )
    delete_author(author_id=author_id)
    # also clean up any portaits uploaded for the deleted author
    portrait_file_paths = [
        path
        for path in PORTRAITS_FOLDER.iterdir()
        if path.is_file() and path.name.startswith(f"{author_id}_portrait")
    ]
    for portait_file in portrait_file_paths:
        portait_file.unlink()


@author_router.post(
    "{author_id}/upload_portait",
    status_code=204,
    response_class=Response,
    responses={403: {"model": Detail}, 404: {"model": Detail}},
)
def post_portait(
    author_id: UUID, uploaded_file: UploadFile, replace: bool = Query(default=False)
):
    if not get_author(author_id=author_id):
        raise HTTPException(
            status_code=404, detail=f"Author with id {author_id} not found."
        ) from None
    portrait_file_paths = [
        path
        for path in PORTRAITS_FOLDER.iterdir()
        if path.is_file() and path.name.startswith(f"{author_id}_portrait")
    ]
    if portrait_file_paths and replace is False:
        raise HTTPException(
            status_code=403,
            detail=(
                f"A portrait for author with id {author_id} is already present. To "
                "replace the existing portrait, use the `force` parameter."
            ),
        ) from None
    content_type = uploaded_file.content_type
    extension = content_type.rsplit("/", maxsplit=1)[-1]
    portrait_file_path = PORTRAITS_FOLDER / f"{author_id}_portrait.{extension}"
    with open(portrait_file_path, mode="wb+") as portrait_file:
        portrait_file.write(uploaded_file.file.read())
