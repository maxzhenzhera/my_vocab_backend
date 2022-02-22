__all__ = [
    'SetRefreshTokenCookieAsOpenAPIHeader',
    'UnsetRefreshTokenCookieAsOpenAPIHeader'
]


SetRefreshTokenCookieAsOpenAPIHeader = {
    'description': 'Set refresh token',
    'schema': {
        'type': 'string',
        'example': (
            'UUID4 instance; '
            'Path=/api/auth; '
            'HttpOnly'
        )
    }
}
UnsetRefreshTokenCookieAsOpenAPIHeader = {
    'description': 'Unset refresh token',
    'schema': {
        'type': 'string',
        'example': (
            'UUID4 instance; '
            'Expires=0; '
            'Max-Age=0; '
            'Path=/api/auth'
        )
    }
}
