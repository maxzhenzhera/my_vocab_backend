from passlib.context import CryptContext


__all__ = ['pwd_context']


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
