from fastapi import FastAPI
from fastapi.routing import APIRouter

router = APIRouter(
    tags=["Product"],
)

def create_app() -> FastAPI:
    app = FastAPI(
        title='Graintrack DDD project',
        docs_url='/api/docs',
        description="API for managing products, categories, reservations, and sales within a Domain-Driven Design (DDD) architecture.",
        debug=True,
    )

    app.include_router(router, prefix="/product")

    return app




