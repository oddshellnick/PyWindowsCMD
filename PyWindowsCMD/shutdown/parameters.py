from PyWindowsCMD import errors
from PyVarTools.python_instances_tools import get_class_attributes


class ShutdownType:
	"""
	Represents the type of shutdown operation to perform.

	Attributes:
		display_gui (str): Displays the shutdown GUI.
		logoff (str): Logs off the current user.
		shutdown (str): Shuts down the computer.
		shutdown_with_sign_in_on_boot (str): Shuts down and requires sign-in on next boot.
		restart (str): Restarts the computer.
		restart_with_sign_in_on_boot (str): Restarts and requires sign-in on next boot.
		abort_shutting_down (str): Aborts a pending shutdown.
		shutdown_without_warning (str): Shuts down without warning.
		hibernate (str): Hibernates the computer.

	:Usage:
		shutdown_type = ShutdownType.shutdown
	"""
	
	display_gui = "/i"
	logoff = "/l"
	shutdown = "/s"
	shutdown_with_sign_in_on_boot = "/sg"
	restart = "/r"
	restart_with_sign_in_on_boot = "/g"
	abort_shutting_down = "/a"
	shutdown_without_warning = "/p"
	hibernate = "/h"


class ShutdownReasonType:
	"""
	Represents the type of shutdown reason.

	Attributes:
		planned (str): Indicates a planned shutdown.
		user_defined (str): Indicates a user-defined shutdown.
		unplanned (str): Indicates an unplanned shutdown.

	:Usage:
		reason_type = ShutdownReasonType.planned
	"""
	
	planned = "P:"
	user_defined = "U:"
	unplanned = ""


class ShutdownReason:
	"""
	Represents the reason for a shutdown operation.  Used with the /d parameter.

	Attributes:
		reason_type (str): The type of reason (planned, user-defined, or unplanned).
		major_reason_number (int): The major reason code (0-255).
		minor_reason_number (int): The minor reason code (0-65535).

	:Usage:
		reason = ShutdownReason(ShutdownReasonType.planned, 4, 2)
		command_parameter = reason.get_command() # /d P:4:2
	"""
	
	def __init__(
			self,
			reason_type: str = ShutdownReasonType.unplanned,
			major_reason_number: int = 0,
			minor_reason_number: int = 0,
	):
		"""
		Initializes a ShutdownReason object.

		Args:
			reason_type (str): The type of shutdown reason. Defaults to unplanned.
			major_reason_number (int): The major reason code. Defaults to 0.
			minor_reason_number (int): The minor reason code. Defaults to 0.

		Raises:
			WrongCommandLineParameter: If invalid reason type, major reason number, or minor reason number is provided.
		"""
		if reason_type not in [
			value["value"]
			for value in get_class_attributes(ShutdownReasonType).values()
		]:
			raise errors.WrongCommandLineParameter("Unknown shutdown type (%s)" % str(reason_type))
		
		if not (0 <= major_reason_number <= 255):
			raise errors.WrongCommandLineParameter("Major reason number of shutdown or reboot has to be in range [0;255]")
		
		if not (0 <= minor_reason_number <= 65535):
			raise errors.WrongCommandLineParameter(
					"Minor reason number of shutdown or reboot has to be in range [0;65535]"
			)
		
		self.reason_type = reason_type
		self.major_reason_number = major_reason_number
		self.minor_reason_number = minor_reason_number
	
	def get_command(self) -> str:
		"""
		Returns the command-line string for the shutdown reason.

		Returns:
			str: The formatted reason string for the /d parameter.

		:Usage:
			reason = ShutdownReason(ShutdownReasonType.planned, 5, 10)
			command_part = reason.get_command() # Returns "/d P:5:10"
		"""
		return f"/d {self.reason_type}{self.major_reason_number}:{self.minor_reason_number}"
