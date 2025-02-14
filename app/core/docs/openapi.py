from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI) -> dict:  # pragma: no cover
    """
    Customizes OpenAPI schema for the FastAPI application.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Returns
    -------
    dict
        The customized OpenAPI schema with security configurations.
    """

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token in the format: Bearer <token>",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema
