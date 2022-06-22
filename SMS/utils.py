
from rest_framework.views import exception_handler
from http import HTTPStatus
from typing import Any

from rest_framework.views import Response


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Using the description's of the HTTPStatus class as error message.
        http_code_to_message = {v.value: v.description for v in HTTPStatus}

        error_payload = {
            "message": "",
            "details": [],
        }
        
        error_payload["message"] = http_code_to_message[response.status_code]
        error_payload["details"] = response.data
        response.data = error_payload
    return response
