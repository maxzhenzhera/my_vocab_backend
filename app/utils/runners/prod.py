import logging

from app.core.settings.app import AppProdSettings
from app.utils.logging_.config import get_logging_config


__all__ = ['run_prod']


logger = logging.getLogger(__name__)


def run_prod(app_path: str, settings: AppProdSettings) -> None:
    from app.utils.gunicorn_ import StandaloneApplication

    logger.info(
        'Used runner for prod environment [Gunicorn] '
        f'with [{settings.gunicorn.workers}] workers.'
    )
    StandaloneApplication(
        app=app_path,
        bind=settings.socket.bind,
        logconfig_dict=get_logging_config(settings),
        **settings.gunicorn.kwargs,
    ).run()
