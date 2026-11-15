"""Custom exceptions raised while validating the configuration.

They derive from ValueError so callers can handle them together with
the other configuration errors.
"""


class ExceptionParser(ValueError):
    """Base exception for configuration parser errors."""

    def __init__(
        self, message: str = "Unknown parser error"
    ) -> None:
        super().__init__(message)


class ExceptionLengthParser(ExceptionParser):
    """Raised when the command-line argument count is invalid."""

    def __init__(
        self,
        message: str = (
            "Invalid argument length. "
            "Only one argument is allowed: <config file>"
        ),
    ) -> None:
        super().__init__(message)
