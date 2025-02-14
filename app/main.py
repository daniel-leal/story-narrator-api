import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import sessionmanager
from app.core.router import include_routers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager.init_db()
    yield
    if sessionmanager.engine is not None:
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    title="Story Narrator API",
    version="0.1.0",
)

include_routers(app)


@app.get("/", tags=["Health Check"], response_model=dict)
async def root():
    return {"message": "Status: OK"}
