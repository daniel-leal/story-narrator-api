import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.presentation.routes.auth_routes import router as auth_router
from app.character.presentation.routes.character_routes import (
    router as character_router,
)
from app.core.database import sessionmanager
from app.story.presentation.routes.scenario_routes import router as scenario_router

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
app.include_router(character_router, prefix="/characters", tags=["Character"])
app.include_router(scenario_router, prefix="/scenarios", tags=["Scenarios"])


@app.get("/", tags=["Health Check"], response_model=dict)
async def root():
    return {"message": "Status: OK"}
