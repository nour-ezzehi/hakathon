from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="Mood Companion")

app.include_router(routes.router)
