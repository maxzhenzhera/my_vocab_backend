from dataclasses import dataclass

from fastapi import FastAPI

from .core.settings import AppSettings
from .core.settings.environments import AppEnvironmentType


__all__ = ['AppBuilder']


@dataclass
class AppBuilder:
    settings: AppSettings

    def __post_init__(self) -> None:
        self.app = FastAPI(**self.settings.fast_api.kwargs)

    def build_app(self) -> FastAPI:
        self._add_middlewares()
        self._add_event_handlers()
        self._add_exception_handlers()
        self._include_routers()
        self._inject_dependencies()
        return self.app

    def _add_middlewares(self) -> None:
        self._add_session_middleware()
        self._add_cors_middleware()

    def _add_session_middleware(self) -> None:
        from starlette.middleware.sessions import SessionMiddleware

        self.app.add_middleware(
            SessionMiddleware,
            secret_key=self.settings.session.secret
        )

    def _add_cors_middleware(self) -> None:
        from starlette.middleware.cors import CORSMiddleware

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.cors.origins,
            allow_credentials=True,
            allow_methods=self.settings.cors.origins,
            allow_headers=self.settings.cors.headers,
        )

    def _add_event_handlers(self) -> None:
        self._add_startup_handler()
        self._add_shutdown_handler()

    def _add_startup_handler(self) -> None:
        from .core.events import get_startup_handler

        self.app.add_event_handler(
            event_type='startup',
            func=get_startup_handler(self.app, self.settings)
        )

    def _add_shutdown_handler(self) -> None:
        from .core.events import get_shutdown_handler

        self.app.add_event_handler(
            event_type='shutdown',
            func=get_shutdown_handler(self.app)
        )

    def _add_exception_handlers(self) -> None:
        self._add_internal_server_exception_handler()

    def _add_internal_server_exception_handler(self) -> None:
        if self.settings.env_type is AppEnvironmentType.DEV:
            from .api.errors.server import internal_server_exception_handler

            self.app.add_exception_handler(Exception, internal_server_exception_handler)

    def _include_routers(self) -> None:
        self._include_api_router()

    def _include_api_router(self) -> None:
        from .api.routes import router

        self.app.include_router(
            router=router,
            prefix='/api'
        )

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
