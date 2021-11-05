from time import time
from typing import Any


class TimeoutValue:
    """Value whose values time out."""

    def __init__(self, value: Any, timeout: int):
        """Creates a value with timeout in seconds

        Args:
            value (Any): the value to set
            timeout (int): the timeout in seconds
        """
        self._value = value
        self._last_set = time()
        self.timeout = timeout

    def __repr__(self):
        """Returns the value of the object."""
        remaining = int(self.timeout - (time() - self._last_set))
        return f"{__class__.__name__}({self.value}, {remaining})"

    @property
    def value(self) -> Any:
        """Gets the value only if the timing has not exceded."""
        timing = time() - self._last_set

        if timing < self.timeout:
            return self._value

        return None

    @value.setter
    def value(self, value: Any, timeout=None):
        """Sets the value while resetting the timer."""
        self._value = value
        self._last_set = time()

        if timeout is not None:
            self.timeout = timeout
