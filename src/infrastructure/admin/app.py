import uvicorn

from fastapi import FastAPI

from src.infrastructure.admin.api import register_routers
from src.infrastructure.admin.middlewares import register_middlewares


class WebPanel:
    def __init__(self, bootstrap):
        self.bootstrap = bootstrap
        self.app = FastAPI(title="Admin WebPanel")

        register_routers(self.app)
        register_middlewares(self.app, bootstrap)

    async def start(self):
        config = uvicorn.Config(self.app, host="127.0.0.1", port=3567, log_level="info")
        server = uvicorn.Server(config)

        await server.serve()
