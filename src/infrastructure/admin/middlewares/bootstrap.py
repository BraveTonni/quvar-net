from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from typing import Any


class BootstrapMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any, bootstrap: Any):
        super().__init__(app)
        self.bootstrap = bootstrap

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request.state.bootstrap = self.bootstrap
        response = await call_next(request)

        return response
