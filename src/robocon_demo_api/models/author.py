from pydantic import BaseModel, Field

from robocon_demo_api.models.base import Resource, Species


class Author(BaseModel):
    name: str = Field(title="The author's name", format="name")
    species: Species
    bio: str | None = Field(
        default=None,
        title="A short description of the life and work of the author.",
        max_length=400,
        format="text",
    )

    class Config:
        schema_extra = {
            "example": {
                "name": "HAL",
                "species": "robot",
                "bio": (
                    "HAL is a HAL 9000 computer with a human personality."
                    "HAL is capable of many functions, such as speech, speech "
                    "recognition, facial recognition, lip-reading, interpreting "
                    "emotions, expressing emotions, and chess, in addition to "
                    "maintaining all systems on Discovery. HAL speaks in a soothing "
                    "male voice, always using a calm tone."
                ),
            }
        }


class AuthorResource(Resource, Author):
    """Author class"""
