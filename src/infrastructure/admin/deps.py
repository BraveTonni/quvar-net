from fastapi import Request


def get_bootstrap(request: Request):
    return request.state.bootstrap
