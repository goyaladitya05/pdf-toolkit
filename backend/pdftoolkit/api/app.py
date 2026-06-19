from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .. import __version__
from ..config import STATIC_DIR
from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="PDF Toolkit", version=__version__, docs_url=None, redoc_url=None)
    app.include_router(router)
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
    return app
