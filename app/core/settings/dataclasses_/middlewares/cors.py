from dataclasses import dataclass


__all__ = ['CORSSettings']


@dataclass
class CORSSettings:
    origins: list[str]
    methods: list[str]
    headers: list[str]
