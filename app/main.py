import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import sessionmanager
from app.presentation.routes.auth_routes import router as auth_router

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

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/", tags=["Health Check"], response_model=dict)
async def root():
    return {"message": "Status: OK"}
