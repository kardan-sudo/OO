from fastapi import FastAPI
from back.routers.api.event import event_router

app = FastAPI()

app.include_router(event_router)