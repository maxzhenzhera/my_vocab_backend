from dataclasses import dataclass


__all__ = ['SocketSettings']


@dataclass
class SocketSettings:
    host: str
    port: int

    @property
    def bind(self) -> str:
        return f'{self.host}:{self.port}'
