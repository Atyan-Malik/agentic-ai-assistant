
import requests
from typing import Any


def get_error_message(
    error: Exception | Any,
    response: requests.Response | None = None,
) -> str:
    """
    Convert API, connection, timeout, and unexpected errors
    into user-friendly messages.
    """

    if response is not None:
        try:
            data = response.json()
            detail = data.get("detail", data)

            if isinstance(detail, dict):
                message = (
                    detail.get("message")
                    or detail.get("error")
                    or detail.get("detail")
                )

                if message:
                    return str(message)

                return str(detail)

            if detail:
                return str(detail)

        except (ValueError, AttributeError):
            if response.text:
                return response.text

        return f"Request failed with status {response.status_code}."

    if isinstance(error, requests.Timeout):
        return (
            "The request timed out. The agent or a tool may be taking "
            "too long. Check the FastAPI terminal for details."
        )

    if isinstance(error, requests.ConnectionError):
        return (
            "Cannot connect to the backend. Make sure FastAPI is "
            "running at http://127.0.0.1:8000."
        )

    if isinstance(error, requests.RequestException):
        return f"Request failed: {error}"

    if isinstance(error, Exception):
        return f"Unexpected error: {error}"

    return "An unknown error occurred."
