from typing import Optional
from subprocess import Popen
from PyWindowsCMD.shutdown.parameters import ShutdownReason
from PyWindowsCMD.shutdown.command import build_shutdown_command


def shutdown_windows(
		shutdown_type: str,
		prepare_for_fast_startup: bool = False,
		fw: bool = False,
		document_reason_of_shutdown: bool = False,
		open_advanced_boot_options_menu: bool = False,
		target_computer: Optional[str] = None,
		time_out_period: int = 30,
		force_running_applications_to_close: bool = False,
		shutdown_reason: Optional[ShutdownReason] = None,
		comment: str = "",
):
	"""
	Shuts down or restarts a Windows computer using the `shutdown` command.

	This function executes the `shutdown` command with specified options to control the shutdown process.

	Args:
		shutdown_type (str): The type of shutdown to perform (e.g., "s" for shutdown, "r" for restart). See `ShutdownType` for options.
		prepare_for_fast_startup (bool): Prepares the system for fast startup. Valid only with shutdown type "s". Defaults to False.
		fw (bool): Combine with a shutdown option to enter the firmware user interface on next boot. Defaults to False.
		document_reason_of_shutdown (bool): Documents the reason for the shutdown. Defaults to False.
		open_advanced_boot_options_menu (bool): Opens the advanced boot options menu on restart. Valid only with shutdown type "r". Defaults to False.
		target_computer (Optional[str]): The target computer's IPv4 address. Defaults to None.
		time_out_period (int): The time-out period before shutdown in seconds (0-315360000, default is 30). Implies /f if > 0.
		force_running_applications_to_close (bool): Forces running applications to close without warning. Implied if `time_out_period` > 0. Defaults to False.
		shutdown_reason (Optional[ShutdownReason]): The reason for the shutdown. Defaults to None.
		comment (str): A comment explaining the shutdown (max 512 characters). Defaults to "".

	:Usage:
		shutdown_windows(ShutdownType.shutdown, time_out_period=60, comment="Performing maintenance")
		shutdown_windows(ShutdownType.restart, target_computer="192.168.1.100")
	"""
	Popen(
			build_shutdown_command(
					shutdown_type=shutdown_type,
					enable_fast_startup=prepare_for_fast_startup,
					enter_firmware_ui=fw,
					log_shutdown_reason=document_reason_of_shutdown,
					show_advanced_boot_options=open_advanced_boot_options_menu,
					target_computer=target_computer,
					time_out_period=time_out_period,
					force_running_applications_to_close=force_running_applications_to_close,
					shutdown_reason=shutdown_reason,
					comment=comment,
			),
			shell=True,
	)
