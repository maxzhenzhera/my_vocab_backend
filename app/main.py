from fastapi import FastAPI

from app.api.routes import router
from app.core.config import (
    server_config,
    uvicorn_config
)
from app.core.events import (
    get_startup_handler,
    get_shutdown_handler
)


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_event_handler('startup', get_startup_handler(application))
    application.add_event_handler('shutdown', get_shutdown_handler(application))

    application.include_router(router, prefix=server_config.API_PREFIX)

    return application


app = get_application()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', **uvicorn_config)
