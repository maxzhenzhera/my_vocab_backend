import logging
import warnings
from dataclasses import dataclass

from fastapi import FastAPI

from .core.settings import AppSettings
from .core.settings.environment import AppEnvType


__all__ = ['AppBuilder']


logger = logging.getLogger(__name__)


@dataclass
class AppBuilder:
    settings: AppSettings

    def __post_init__(self) -> None:
        self.app = FastAPI(**self.settings.fastapi.kwargs)

    @property
    def short_app_info(self) -> str:
        return f'< "{self.settings.fastapi.title}" [{self.settings.fastapi.version}] >'

    def build(self) -> FastAPI:
        self._add_middlewares()
        self._add_event_handlers()
        self._add_exception_handlers()
        self._include_routers()
        self._inject_dependencies()
        logger.info(f'App {self.short_app_info} has been built.')
        return self.app

    def _add_middlewares(self) -> None:
        self._add_session_middleware()
        self._add_cors_middleware()
        logger.debug('Middlewares have been added.')

    def _add_session_middleware(self) -> None:
        from starlette.middleware.sessions import SessionMiddleware

        self.app.add_middleware(
            SessionMiddleware,
            secret_key=self.settings.session.secret
        )
        logger.debug('Session middleware has been added.')

    def _add_cors_middleware(self) -> None:
        from starlette.middleware.cors import CORSMiddleware

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.cors.origins,
            allow_methods=self.settings.cors.methods,
            allow_headers=self.settings.cors.headers,
            allow_credentials=True
        )
        logger.debug('CORS middleware has been added.')

    def _add_event_handlers(self) -> None:
        self._add_startup_handler()
        self._add_shutdown_handler()
        logger.debug('Event handlers have been added.')

    def _add_startup_handler(self) -> None:
        from .core.events import get_startup_handler

        self.app.add_event_handler(
            event_type='startup',
            func=get_startup_handler(self.app, self.settings)
        )
        logger.debug('Startup handler has been added.')

    def _add_shutdown_handler(self) -> None:
        from .core.events import get_shutdown_handler

        self.app.add_event_handler(
            event_type='shutdown',
            func=get_shutdown_handler(self.app)
        )
        logger.debug('Shutdown handler has been added.')

    def _add_exception_handlers(self) -> None:
        self._add_internal_server_exception_handler()
        logger.debug('Exception handlers have been added.')

    def _add_internal_server_exception_handler(self) -> None:
        if self.settings.env_type is AppEnvType.DEV:
            from .api.errors.server import internal_server_exception_handler

            self.app.add_exception_handler(Exception, internal_server_exception_handler)
            warnings.warn(
                UserWarning(
                    'Exception handler that shows traceback on internal server error '
                    'has been added [Included for DEV environment].'
                )
            )

    def _include_routers(self) -> None:
        self._include_api_router()
        logger.debug('Routers have been included.')

    def _include_api_router(self) -> None:
        from .api.routes import router

        self.app.include_router(
            router=router,
            prefix='/api'
        )
        logger.debug('API router has been included.')

    def _inject_dependencies(self) -> None:
        from .api.dependencies.authentication import inject_authentication
        from .api.dependencies.db import inject_db
        from .api.dependencies.mail import inject_mail
        from .api.dependencies.oauth import inject_oauth
        from .api.dependencies.settings import inject_settings

        inject_authentication(self)
        inject_db(self)
        inject_mail(self)
        inject_oauth(self)
        inject_settings(self)
        logger.debug('Dependencies have been injected.')
