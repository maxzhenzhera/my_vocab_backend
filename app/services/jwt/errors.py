__all__ = [
    'InvalidTokenSignatureError',
    'ExpiredTokenSignatureError'
]


class InvalidTokenSignatureError(Exception):
    """
    Common token decoding exception.
    Raised if the token signature is invalid in any way except expiration claim.
    """


class ExpiredTokenSignatureError:
    """ Raised if the token signature has expired. """
