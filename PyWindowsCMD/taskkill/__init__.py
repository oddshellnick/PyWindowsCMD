from subprocess import Popen
from typing import Optional, Union
from PyWindowsCMD.taskkill.command import build_taskkill_command
from PyWindowsCMD.taskkill.parameters import (
	ImageName,
	ProcessFilter,
	ProcessID,
	RemoteSystem,
	selector_type
)


def taskkill_windows(
		taskkill_type: str,
		remote_system: Optional[RemoteSystem] = None,
		selectors: Optional[Union[selector_type, list[selector_type]]] = None,
):
	"""
	Terminates processes on a local or remote Windows system using `taskkill`.

	This function executes the constructed `taskkill` command to terminate processes based on specified criteria.

	Args:
		taskkill_type (str): The type of termination to perform (e.g., "/F" for forceful termination).  See `TaskKillType`.
		remote_system (Optional[RemoteSystem]):  Specifies a remote system to execute the command on. Defaults to None.
		selectors (Optional[Union[selector_type, list[selector_type]]]): One or more selectors to identify the processes to terminate. Defaults to None.
	"""
	Popen(
			build_taskkill_command(
					taskkill_type=taskkill_type,
					remote_system=remote_system,
					selectors=selectors
			),
			shell=True,
	)
