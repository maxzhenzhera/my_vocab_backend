__all__ = [
    'SESSION_EXPIRED',
    'ACCESS_TOKEN_IS_INVALID',
    'OWNER_OF_ACCESS_TOKEN_DOES_NOT_EXIST',
    'CURRENT_USER_IN_NOT_ACTIVE',
    'CURRENT_USER_IS_NOT_SUPERUSER',
    'LOGIN_FAILED',
    'EMAIL_IS_ALREADY_TAKEN',
    'REFRESH_SESSION_DOES_NOT_EXIST',
    'REFRESH_SESSION_EXPIRED',
    'CONFIRMATION_LINK_IS_INVALID'
]


# authentication dependency (access token processing)
SESSION_EXPIRED = 'The current session has expired. Please, refresh.'
ACCESS_TOKEN_IS_INVALID = 'The access token is invalid.'
OWNER_OF_ACCESS_TOKEN_DOES_NOT_EXIST = 'The owner of the access token does not exist.'
CURRENT_USER_IN_NOT_ACTIVE = 'The current user is not active.'
CURRENT_USER_IS_NOT_SUPERUSER = 'The current user is not a superuser.'

# exceptions' details
LOGIN_FAILED = 'The incorrect credentials.'
EMAIL_IS_ALREADY_TAKEN = 'The email {email} is busy. Please, use alternative.'
REFRESH_SESSION_DOES_NOT_EXIST = 'A refresh session does not exist.'
REFRESH_SESSION_EXPIRED = 'The refresh session has expired.'

# used in routes directly
CONFIRMATION_LINK_IS_INVALID = 'The confirmation link is invalid.'
