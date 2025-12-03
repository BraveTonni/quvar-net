from fastapi import FastAPI

from .bootstrap import BootstrapMiddleware


def register_middlewares(app: FastAPI, bootstrap) -> None:
    app.add_middleware(BootstrapMiddleware, bootstrap=bootstrap)
