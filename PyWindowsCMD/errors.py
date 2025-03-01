class WrongCommandLineParameter(Exception):
	"""
	Custom exception raised when an invalid command-line parameter is provided.

	:Usage:
		raise WrongCommandLineParameter("Invalid input")
	"""
	
	def __init__(self, message):
		"""
		Initializes the WrongCommandLineParameter exception.

		Args:
			message (str): The error message to store.
		"""
		super().__init__(message)


class NetstatOutputError(Exception):
	"""
	Custom exception raised when there is an error parsing the output of the `netstat` command.

	:Usage:
		raise NetstatOutputError("Could not parse netstat output")
	"""
	
	def __init__(self, message):
		"""
		Initializes the NetstatOutputError exception.

		Args:
			message (str): The error message to store.
		"""
		super().__init__(message)
