from fastapi import FastAPI

from app.core.config import (
    server_config,
    uvicorn_config
)
from app.api.routes import router


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router, prefix=server_config.API_PREFIX)
    return application


app = get_application()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', **uvicorn_config)
