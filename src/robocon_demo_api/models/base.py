from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class Resource(BaseModel):
    id: UUID = Field(default_factory=uuid4)
