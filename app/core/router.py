from fastapi.applications import FastAPI

from app.auth.presentation.routes.auth_routes import router as auth_router
from app.character.presentation.routes.character_routes import (
    router as character_router,
)
from app.scenario.presentation.routes.scenario_routes import router as scenario_router
from app.story.presentation.routes.story_routes import router as story_router


def include_routers(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(character_router, prefix="/characters", tags=["Character"])
    app.include_router(scenario_router, prefix="/scenarios", tags=["Scenarios"])
    app.include_router(story_router, prefix="/stories", tags=["Story"])
