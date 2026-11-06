class ExceptionParser(Exception):
	def __init__(
		self, message: str = "Unknown parser error"
	) -> None:
		super().__init__(message)


class ExceptionLengthParser(ExceptionParser):
	def __init__(
		self,
		message: str = (
			"Invalid argument length. "
			"Only one argument is allowed: <config.txt>"
		),
	) -> None:
		super().__init__(message)


class ExceptionNameParser(ExceptionParser):
	def __init__(
		self,
		message: str = (
			"The configuration file name is not \"config.txt\""
		),
	) -> None:
		super().__init__(message)
