"""Custom exceptions raised while validating parser arguments."""


class ExceptionParser(Exception):
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
            "Only one argument is allowed: <config.txt>"
        ),
    ) -> None:
        super().__init__(message)


class ExceptionNameParser(ExceptionParser):
    """Raised when the configuration file name is invalid."""

    def __init__(
        self,
        message: str = (
            'The configuration file name is not "config.txt"'
        ),
    ) -> None:
        super().__init__(message)
