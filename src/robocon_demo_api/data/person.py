from typing import List

from robocon_demo_api.models.person import Attendee, Speaker

ATTENDEES: List[Attendee] = []
SPEAKERS = [a for a in ATTENDEES if isinstance(a, Speaker)]
