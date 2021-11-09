from authlib.integrations.starlette_client import OAuth

from ....core.config import oauth_config


__all__ = [
    'oauth',
    'GOOGLE_OAUTH_NAME'
]


GOOGLE_OAUTH_NAME = 'google'


oauth = OAuth(oauth_config)

oauth.register(
    name=GOOGLE_OAUTH_NAME,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'email'
    }
)
