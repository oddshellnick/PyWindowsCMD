from PyVarTools.python_instances_tools import get_class_fields

from PyWindowsCMD import errors
from PyWindowsCMD.shutdown.parameters import ShutdownReason, ShutdownType
from PyWindowsCMD.utilities import count_parameters


def build_shutdown_command(
    shutdown_type: str,
    enable_fast_startup: bool = False,
    enter_firmware_ui: bool = False,
    log_shutdown_reason: bool = False,
    show_advanced_boot_options: bool = False,
    target_computer: str | None = None,
    time_out_period: int = 30,
    force_running_applications_to_close: bool = False,
    shutdown_reason: ShutdownReason | None = None,
    comment: str = "",
) -> str:
    """
    Constructs a Windows CMD command for shutting down or restarting a computer.

    Uses the "SHUTDOWN" command to manage the computer's power state.  Implements
    various options for controlling the shutdown process.

    Args:
            shutdown_type (str): The type of shutdown to perform (e.g., "s" for shutdown, "r" for restart).  See `ShutdownType` for options.
            enable_fast_startup (bool): Prepares the system for fast startup.  Valid only with shutdown type "s". Defaults to False.
            enter_firmware_ui (bool):  Combine with a shutdown option to enter the firmware user interface on next boot. Defaults to False.
            log_shutdown_reason (bool): Documents the reason for the shutdown. Defaults to False.
            show_advanced_boot_options (bool): Opens the advanced boot options menu on restart. Valid only with shutdown type "r". Defaults to False.
            target_computer (str, optional): The target computer's IPv4 address. Defaults to None.
            time_out_period (int): The time-out period before shutdown in seconds (0-315360000, default is 30).  Implies /f if > 0.
            force_running_applications_to_close (bool): Forces running applications to close without warning. Implied if `time_out_period` > 0. Defaults to False.
            shutdown_reason (ShutdownReason, optional): The reason for the shutdown. Defaults to None.
            comment (str): A comment explaining the shutdown (max 512 characters). Defaults to "".

    Returns:
            str: The constructed shutdown command string.

    Raises:
            WrongCommandLineParameter: If invalid parameter combinations or values are provided.

    :Usage:
            command = cmd_shutdown_windows(ShutdownType.shutdown, time_out_period=60, comment="Performing maintenance")
            command = cmd_shutdown_windows(ShutdownType.restart, target_computer="192.168.1.100")
    """
    if (
        count_parameters(
            shutdown_type,
            enable_fast_startup,
            enter_firmware_ui,
            log_shutdown_reason,
            show_advanced_boot_options,
            target_computer,
            time_out_period,
            force_running_applications_to_close,
            shutdown_reason,
            comment,
        )
        == 0
    ):
        raise errors.WrongCommandLineParameter("Function called with no parameters.")

    if shutdown_type not in get_class_fields(ShutdownType).values():
        raise errors.WrongCommandLineParameter("Unknown shutdown type (%s)" % str(shutdown_type))

    if enable_fast_startup and shutdown_type != ShutdownType.shutdown:
        raise errors.WrongCommandLineParameter('"prepare_for_fast_startup" parameter used only with type "shutdown".')

    if show_advanced_boot_options and shutdown_type != ShutdownType.restart:
        raise errors.WrongCommandLineParameter(
            '"open_advanced_boot_options_menu" parameter used only with type "restart".'
        )

    if (
        shutdown_type == ShutdownType.abort_shutting_down
        and count_parameters(
            log_shutdown_reason,
            show_advanced_boot_options,
            target_computer,
            force_running_applications_to_close,
            shutdown_reason,
        )
        > 0
    ):
        raise errors.WrongCommandLineParameter('Type "abort shutting down" has to be alone or with parameter "fw".')

    if shutdown_type == ShutdownType.logoff and (target_computer or shutdown_reason):
        raise errors.WrongCommandLineParameter(
            '"shutdown" command can\'t have "target_computer" or "shutdown_reason" parameters with type "logoff".'
        )

    if not (0 <= time_out_period <= 315360000):
        raise errors.WrongCommandLineParameter("Wrong timeout. It has to be in range [0;315360000].")
    elif force_running_applications_to_close and time_out_period == 0:
        raise errors.WrongCommandLineParameter('"f" parameter has to be used only with parameter "t" > 0.')

    commands = ["shutdown", shutdown_type]

    if enable_fast_startup:
        commands.append("/hybrid")

    if enter_firmware_ui:
        commands.append("/fw")

    if log_shutdown_reason:
        commands.append("/e")

    if show_advanced_boot_options:
        commands.append("/o")

    if target_computer:
        commands.append(f"/m \\\\{target_computer}")

    if time_out_period:
        commands.append(f"/t {time_out_period}")

    if force_running_applications_to_close:
        commands.append("/f")

    if shutdown_reason:
        commands.append(shutdown_reason.get_command())

    if comment:
        commands.append(f'/c "{comment}"')

    return " ".join(commands)
