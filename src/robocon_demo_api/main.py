from fastapi import FastAPI

from robocon_demo_api.routers.person import person_router

def create_app():
    app = FastAPI()
    app.include_router(person_router)

    return app


api = create_app()
