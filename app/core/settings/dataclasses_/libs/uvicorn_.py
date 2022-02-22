from dataclasses import dataclass


__all__ = ['UvicornSettings']


@dataclass
class UvicornSettings:
    host: str
    port: int
    reload: bool
    logging_config_path: str

    @property
    def kwargs(self) -> dict[str, str | int | bool]:
        return {
            'host': self.host,
            'port': self.port,
            'reload': self.reload,
            'log_config': self.logging_config_path,
        }
