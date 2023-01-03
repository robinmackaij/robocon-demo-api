from pydantic import BaseModel

from robocon_demo_api.models.base import Resource, Species


class NewAuthor(BaseModel):
    name: str
    bio: str | None = None
    species: Species


class Author(Resource, NewAuthor):
    """Author class"""
