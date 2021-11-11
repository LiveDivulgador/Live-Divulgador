class TwitchException(Exception):
    def __init__(self, status: int, details: str = ""):
        self.status = status
        self.details = details

    def __init__(self, cause: Exception):
        super(TwitchException, self).__init__(cause)


class InvalidCredentialsException(TwitchException):
    """An authentication error occurred because of bad credentials."""


class ObjectNotFoundException(TwitchException):
    """The requested object was not found."""


class UnexpectedResponseException(TwitchException):
    """The response has an unexpected code or data"""


class InsufficientPermissions(TwitchException):
    """Not enough permissions to perform a certain action"""
