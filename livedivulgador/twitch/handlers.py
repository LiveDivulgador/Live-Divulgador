from httpx import Response

from livedivulgador.twitch.exceptions import (
    InsufficientPermissions,
    InvalidCredentialsException,
    ObjectNotFoundException,
    TwitchException,
    UnexpectedResponseException,
)


def handle_response(response: Response) -> dict:
    """Return a json object otherwise raises an error
    Args:
            response (Response): HTTP response object
    Raises:
            InvalidCredentialsException: Credentials are invalid (401)
            InsufficientPermissions: User has insufficient permissions (403)
            ObjectNotFoundException: The object was not found (404)
            TwitchException: Miro specific exceptions (5xx)
            UnexpectedResponseException: For unexpected events raises unexpected response from server
    Returns:
            Dict: Dictionary object with the json response from the server
    """

    if is_2xx_status_code(response.status_code):
        return response.json()

    if response.status_code == 401:
        raise InvalidCredentialsException(response.status_code)

    if response.status_code == 403:
        raise InsufficientPermissions(response.status_code)

    if response.status_code == 404:
        raise ObjectNotFoundException(response.status_code)

    if is_5xx_status_code(response.status_code):
        raise TwitchException(response.status_code)

    raise UnexpectedResponseException(response.status_code)


def is_2xx_status_code(status_code: int) -> bool:
    return str(status_code).startswith("2")


def is_5xx_status_code(status_code: int) -> bool:
    return str(status_code).startswith("5")
