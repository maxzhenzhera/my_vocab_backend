__all__ = [
    'GOOGLE_OAUTH_NAME',
    'GOOGLE_OAUTH_SERVER_METADATA_URL',
    'GOOGLE_OAUTH_CLIENT_KWARGS'
]


GOOGLE_OAUTH_NAME = 'google'
GOOGLE_OAUTH_SERVER_METADATA_URL = (
    'https://accounts.google.com/.well-known/openid-configuration'
)
GOOGLE_OAUTH_CLIENT_KWARGS = {
    'scope': 'email'
}
