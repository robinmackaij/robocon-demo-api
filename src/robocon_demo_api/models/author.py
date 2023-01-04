from pydantic import BaseModel

from robocon_demo_api.models.base import Resource, Species


class NewAuthor(BaseModel):
    name: str
    species: Species
    bio: str | None = None


class Author(Resource, NewAuthor):
    """Author class"""
