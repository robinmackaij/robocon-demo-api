from typing import List
from uuid import UUID

from fastapi import APIRouter, Response, HTTPException

from robocon_demo_api.data.person import ATTENDEES, SPEAKERS
from robocon_demo_api.models.person import Attendee, Speaker


person_router = APIRouter(prefix="/attendees")


@person_router.get("/", status_code=200, response_model=List[Attendee])
def get_attendees() -> List[Attendee]:
    return ATTENDEES


@person_router.post("/", status_code=201, response_model=Attendee)
def create_attendee(name: str) -> Attendee:
    attendee = Attendee(name=name)
    ATTENDEES.append(attendee)
    return attendee


@person_router.get("/speakers", status_code=200, response_model=List[Speaker])
def get_speakers() -> List[Speaker]:
    return SPEAKERS


@person_router.delete("/{attendee_id}", status_code=204, response_class=Response)
def delete_attendee(attendee_id: UUID) -> None:
    attendee = [a for a in ATTENDEES if a.id == attendee_id]
    if not attendee:
        raise HTTPException(status_code=404, detail=f"No attendent with id {attendee_id} found.")
    if isinstance(attendee[0], Speaker):
        raise HTTPException(status_code=406, detail=f"Cannot delete speaker with id {attendee_id}")
    ATTENDEES.remove(attendee[0])
    return None
