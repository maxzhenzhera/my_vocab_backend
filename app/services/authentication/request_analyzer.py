from dataclasses import dataclass

from fastapi import Request


__all__ = ['RequestAnalyzer']


@dataclass
class RequestAnalyzer:
    request: Request

    @property
    def client_ip_address(self) -> str:
        return self.request.client.host

    @property
    def client_user_agent(self) -> str:
        return self.request.headers['user-agent']
