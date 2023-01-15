from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Resource(BaseModel):
    id: UUID = Field(default_factory=uuid4)


class Species(str, Enum):
    HUMAN = "human"
    ROBOT = "robot"
    UNKNOWN = "unknown"


class Detail(BaseModel):
    """Class for API message details."""

    detail: str
