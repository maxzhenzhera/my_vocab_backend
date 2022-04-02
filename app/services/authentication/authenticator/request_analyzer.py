import warnings
from dataclasses import dataclass
from typing import cast

from fastapi import Request


__all__ = ['RequestAnalyzer']


warnings.warn(
    UserWarning(
        'Client IP address handling have to be improved. '
        'Reminder: `uvicorn`.`forwarded_allow_ips` - [*].'
    )
)


@dataclass
class RequestAnalyzer:
    request: Request

    @property
    def client_ip_address(self) -> str:
        return cast(str, self.request.client.host or self.request.headers['X-Real-IP'])

    @property
    def client_user_agent(self) -> str:
        return self.request.headers['user-agent']
