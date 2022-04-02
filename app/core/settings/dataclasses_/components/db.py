from dataclasses import dataclass


__all__ = ['DBSettings']


@dataclass
class DBSettings:
    dialect: str
    driver: str
    uri: str

    @property
    def sqlalchemy_scheme(self) -> str:
        return f'{self.dialect}+{self.driver}'

    @property
    def sqlalchemy_url(self) -> str:
        if self.sqlalchemy_scheme in self.uri:
            return self.uri
        return self.uri.replace(self.dialect, self.sqlalchemy_scheme)
