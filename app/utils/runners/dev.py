import logging

from app.core.settings.app import AppDevSettings
from app.utils.logging_.config import get_logging_config


__all__ = ['run_dev']


logger = logging.getLogger(__name__)


def run_dev(app_path: str, settings: AppDevSettings) -> None:
    import uvicorn

    logger.info('Used runner for dev environment [Uvicorn].')
    uvicorn.run(
        app=app_path,
        host=settings.socket.host,
        port=settings.socket.port,
        log_config=get_logging_config(settings),
        **settings.uvicorn.kwargs
    )
