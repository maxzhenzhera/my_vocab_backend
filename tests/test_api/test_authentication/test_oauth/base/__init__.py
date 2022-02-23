from .login import (
    BaseTestOAuthLoginRouteCaseByUserWithOAuth,
    BaseTestOAuthLoginRouteCaseByUserWithoutOAuth
)
from .redirect_to_oauth_route import BaseTestRedirectToOAuthRouteCase
from .register import BaseOauthRegisterRouteCase
from .route import BaseTestCommonErrorsOfOAuthRoute


__all__ = [
    'BaseTestOAuthLoginRouteCaseByUserWithOAuth',
    'BaseTestOAuthLoginRouteCaseByUserWithoutOAuth',
    'BaseTestRedirectToOAuthRouteCase',
    'BaseOauthRegisterRouteCase',
    'BaseTestCommonErrorsOfOAuthRoute'
]
