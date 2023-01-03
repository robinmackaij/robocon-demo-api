from uuid import UUID

from pydantic import BaseModel

from robocon_demo_api.models.base import Resource


class NewPoem(BaseModel):
    title: str
    content: str
    author_id: UUID


class Poem(Resource, NewPoem):
    """Poem class"""
