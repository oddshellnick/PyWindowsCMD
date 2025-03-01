from typing import Optional
from PyWindowsCMD import errors
from PyWindowsCMD.utilities import count_parameters
from PyVarTools.python_instances_tools import get_class_attributes
from PyWindowsCMD.taskkill.parameters import (
	RemoteSystem,
	TaskKillTypes,
	selector_type
)


def build_taskkill_command(
		taskkill_type: str,
		remote_system: Optional[RemoteSystem] = None,
		selectors: Optional[selector_type, list[selector_type]] = None,
) -> str:
	"""
	Constructs a Windows CMD command for terminating processes using `taskkill`.

	Args:
		taskkill_type (str): The type of termination to perform (e.g., "/F" for forceful termination). See `TaskKillType` for options.
		remote_system (Optional[RemoteSystem]): Specifies a remote system to execute the command on. Defaults to None.
		selectors (Optional[selector_type, list[selector_type]]):  One or more selectors to identify processes to terminate. Defaults to None.

	Returns:
		str: The constructed `taskkill` command string.

	Raises:
		WrongCommandLineParameter: If invalid parameter combinations or values are provided.
	"""
	if count_parameters(taskkill_type, remote_system, selectors) == 0:
		raise errors.WrongCommandLineParameter("Function called with no parameters.")
	
	if taskkill_type not in [value["value"] for value in get_class_attributes(TaskKillTypes).values()]:
		raise errors.WrongCommandLineParameter(
				f"Invalid taskkill type parameter. Valid types {list(get_class_attributes(TaskKillTypes).values())}"
		)
	
	commands = ["taskkill"]
	
	if remote_system is not None:
		commands.append(remote_system.get_command())
	
	if selectors is not None:
		if isinstance(selectors, list):
			for selector in selectors:
				commands.append(selector.get_command())
		else:
			commands.append(selectors.get_command())
	
	commands.append(taskkill_type)
	
	return " ".join(commands)
