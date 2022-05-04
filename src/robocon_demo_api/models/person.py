from robocon_demo_api.models.base import Resource


class Attendee(Resource):
    name: str


class Speaker(Attendee):
    talk_id: str
