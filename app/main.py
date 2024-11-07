# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from containers import init_container
from domain.exceptions.base_exception import ApplicationException


def create_app(container=None) -> FastAPI:
    app = FastAPI(
        title='Graintrack DDD project',
        docs_url='/api/docs',
        description="API for managing products, categories, reservations, and sales within a Domain-Driven Design (DDD) architecture.",
        debug=True,
    )

    # If no container is provided, use the default one
    if container is None:
        container = init_container()

    app.state.container = container

    from presentation.api.v1.endpoints import products, reservations, sales, categories
    app.include_router(products.router, prefix="/api/v1")
    app.include_router(reservations.router, prefix="/api/v1")
    app.include_router(sales.router, prefix="/api/v1")
    app.include_router(categories.router, prefix="/api/v1")

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(request: Request, exc: ApplicationException):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message}
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )

    return app

