import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import sessionmanager
from app.core.dependencies import get_auth_service
from app.core.docs.openapi import custom_openapi
from app.core.router import include_routers
from app.core.settings.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database session manager
    sessionmanager.init_db()

    # Initialize auth service
    async with sessionmanager.session() as session:
        app.state.auth_service = get_auth_service(session)

    yield
    if sessionmanager.engine is not None:
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for generating stories with characters and scenarios",
    contact={
        "name": "Daniel Leal",
        "url": "https://daniel-leal.com",
        "email": "daniel.leal@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = lambda: custom_openapi(app)

include_routers(app)


@app.get("/", tags=["Health Check"], response_model=dict)
async def root():
    return {"message": "Status: OK"}
