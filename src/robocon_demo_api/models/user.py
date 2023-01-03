from pydantic import BaseModel

from robocon_demo_api.models.base import Human, Robot
from robocon_demo_api.models.poem import Poem


class User(BaseModel):
    favorite_poem: Poem


class HumanUser(User, Human):
    """A human user."""


class RobotUser(User, Robot):
    """A robot user."""
