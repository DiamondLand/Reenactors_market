from fastapi import FastAPI

app = FastAPI()

from .controller import controller

app.include_router(controller)