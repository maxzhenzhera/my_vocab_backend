import traceback

from fastapi import Request
from fastapi.responses import PlainTextResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


def internal_server_exception_handler(
        _: Request,
        exception: Exception
) -> PlainTextResponse:
    """ Return the traceback of the internal server error. """
    exception_traceback = ''.join(
        traceback.format_exception(
            type(exception),
            value=exception,
            tb=exception.__traceback__
        )
    )
    message = (
          f'{"Internal server error has occurred.":<50}|\n'
          f'{"Please, check the traceback.":<50}|\n'
          f'{"-" * 50}x\n\n'
    )
    message += exception_traceback
    return PlainTextResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=message
    )
