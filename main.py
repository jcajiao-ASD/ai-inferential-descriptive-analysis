"""FastAPI Application Entry Point."""

from fastapi import FastAPI
from src.core.app_lifespan import app_lifespan
from src.presentation.api.healthcheck import healthcheck_controller
from src.presentation.middleware.cors import add_cors_middleware

app = FastAPI(
    title="Domain services - Project",
    description="Description services",
    version="0.0.1",
    contact={
        "name": "Grupo ASD S.AS.",
        "url": "https://www.grupoasd.com/contacto/",
    },
    lifespan=app_lifespan,
)

add_cors_middleware(app)

app.include_router(healthcheck_controller.router, tags=["healthcheck"], prefix="/api")
