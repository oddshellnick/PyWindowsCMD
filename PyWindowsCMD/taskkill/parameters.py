from typing import Literal

from PyWindowsCMD import errors


class ProcessFilter:
    """
    Represents a filter for selecting processes based on a criteria.

    Attributes:
        filter_name (str): The filter expression.

    :Usage:
        process_filter = ProcessFilter("STATUS eq RUNNING")
        command_parameter = process_filter.get_command()
    """

    def __init__(self, filter_name: str, filter_operator: str, filter_value: str):
        """
        Initializes a ProcessFilter object.

        Args:
            filter_name (str): The filter string.
            filter_operator (str): The filter string.
            filter_value (str): The filter string.
        """
        self.filter_name = filter_name
        self.filter_operator = filter_operator
        self.filter_value = filter_value

    def get_command(self) -> str:
        """
        Returns the command-line string for the process filter.

        Returns:
            str: The formatted filter string.
        """
        return f'/FI "{self.filter_name} {self.filter_operator} {self.filter_value}"'


class WindowTitleProcessFilter(ProcessFilter):
    """
    Filters processes by their window title.

    :Usage:
        window_title_filter = WindowTitleProcessFilter("eq", "Untitled - Notepad")
        command_parameter = window_title_filter.get_command() # /FI "WINDOWTITLE eq Untitled - Notepad"

    """

    def __init__(self, operator: Literal["eq", "ne"], value: str):
        """
        Initializes a WindowTitleProcessFilter.

        Args:
            operator (Literal["eq", "ne"]): The comparison operator ("eq" or "ne").
            value (str): The window title to filter by.

        Raises:
            WrongCommandLineParameter: If an invalid operator is provided.
        """
        if operator not in ["eq", "ne"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for WINDOWTITLE filter. Valid operators {['eq', 'ne']}"
            )

        super().__init__(filter_name="WINDOWTITLE", filter_operator=operator, filter_value=value)


class UsernameProcessFilter(ProcessFilter):
    """
    Filters processes by their username.

    :Usage:

        username_filter = UsernameProcessFilter("eq", "testuser", "domain")
        command_parameter = username_filter.get_command() # /FI "USERNAME eq domain\testuser"
    """

    def __init__(self, operator: Literal["eq", "ne"], username: str, domain: str = ""):
        """
        Initializes a UsernameProcessFilter.

        Args:
            operator (Literal["eq", "ne"]):  The comparison operator ("eq" or "ne").
            username (str): The username to filter by.
            domain (str, optional):  The domain. Defaults to "".

        Raises:
            WrongCommandLineParameter: If an invalid operator is provided.
        """

        if operator not in ["eq", "ne"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for USERNAME filter. Valid operators {['eq', 'ne']}"
            )

        if domain:
            domain = f"{domain}\\"

        super().__init__(filter_name="USERNAME", filter_operator=operator, filter_value=f"{domain}{username}")


class UserContext:
    """
    Represents user credentials for remote system access.

    Attributes:
        username (str): The username.
        domain (str, optional): The domain. Defaults to "".
        password (str, optional): The password.  If None, no password is used. If "", prompts for password. Defaults to None.

    :Usage:
        user_context = UserContext("administrator", "mydomain", "password123")
        command_parameter = user_context.get_command()
    """

    def __init__(self, username: str, domain: str = "", password: str | None = None):
        """
        Initializes a UserContext object.

        Args:
            username (str): The username.
            domain (str, optional): The domain. Defaults to "".
            password (str, optional): The password. Defaults to None.
        """
        self.username = username
        self.domain = domain
        self.password = password

    def get_command(self) -> str:
        """
        Constructs the command-line string for the user context.

        Returns:
            str: The formatted user context string.

        :Usage:
            context = UserContext("user", "domain", "pass")
            command_part = context.get_command() # /U domain\\user /P pass
        """
        domain = f"{self.domain}\\" if self.domain else ""

        if self.password is None:
            password = f""
        elif self.password == "":
            password = " /P"
        else:
            password = f" /P {self.password}"

        return f"/U {domain}{self.username}{password}"


class RemoteSystem:
    """
    Represents a remote system for `taskkill` operations.

    Attributes:
        remote_system (str): The name or IP address of the remote system.
        user_context (UserContext, optional): The user context for accessing the remote system. Defaults to None.

    :Usage:
        remote_system = RemoteSystem("192.168.1.100", UserContext("admin", "domain", "password"))
        command_parameter = remote_system.get_command()
    """

    def __init__(
        self,
        remote_system: str,
        user_context: UserContext | None = None,
    ):
        """
        Initializes a RemoteSystem object.

        Args:
            remote_system (str): The remote system's name or IP address.
            user_context (UserContext, optional): The user credentials for the remote system. Defaults to None.
        """
        self.remote_system = remote_system
        self.user_context = user_context

    def get_command(self) -> str:
        """
        Constructs the command-line string for the remote system.

        Returns:
            str: The formatted remote system string.

        :Usage:
            remote = RemoteSystem("server", UserContext("user", "domain"))
            command_part = remote.get_command() # /S server /U domain\\user
        """
        user_context = "" if self.user_context is None else f" {self.user_context.get_command()}"
        return f"/S {self.remote_system}{user_context}"


class TaskKillTypes:
    """
    Represents the type of process termination to use with `taskkill`.

    Attributes:
        terminate (str): Sends a termination signal to the process.
        forcefully_terminate (str): Forcefully terminates the process.

    :Usage:
        kill_type = TaskKillType.forcefully_terminate
    """

    terminate = "/T"
    forcefully_terminate = "/F"


class StatusProcessFilter(ProcessFilter):
    """
    Filters processes by their status.

    :Usage:
        status_filter = StatusProcessFilter("eq", "RUNNING")
        command_parameter = status_filter.get_command() # /FI "STATUS eq RUNNING"
    """

    def __init__(self, operator: Literal["eq", "ne"], value: Literal["RUNNING", "NOT RESPONDING", "UNKNOWN"]):
        """
        Initializes a StatusProcessFilter.

        Args:
            operator (Literal["eq", "ne"]): The comparison operator ("eq" or "ne").
            value (Literal["RUNNING", "NOT RESPONDING", "UNKNOWN"]): The status value to filter by.

        Raises:
             WrongCommandLineParameter: If an invalid operator or value is provided.
        """
        if operator not in ["eq", "ne"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for STATUS filter. Valid operators {['eq', 'ne']}"
            )

        if value not in ["RUNNING", "NOT RESPONDING", "UNKNOWN"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{value}' value for STATUS filter. Valid values {['RUNNING', 'NOT RESPONDING', 'UNKNOWN']}"
            )

        super().__init__(filter_name="STATUS", filter_operator=operator, filter_value=value)


class SessionProcessFilter(ProcessFilter):
    """
    Filters processes by their session ID.

    :Usage:
        session_filter = SessionProcessFilter("eq", 2)
        command_parameter = session_filter.get_command() # /FI "SESSION eq 2"
    """

    def __init__(self, operator: Literal["eq", "ne", "gt", "lt", "ge", "le"], value: str | int):
        """
        Initializes a SessionProcessFilter.

        Args:
            operator (Literal["eq", "ne", "gt", "lt", "ge", "le"]): The comparison operator.
            value (str | int): The session ID to filter by.

        Raises:
            WrongCommandLineParameter: If an invalid operator is provided.
        """
        if operator not in ["eq", "ne", "gt", "lt", "ge", "le"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for SESSION filter. Valid operators {['eq', 'ne', 'gt', 'lt', 'ge', 'le']}"
            )

        super().__init__(filter_name="SESSION", filter_operator=operator, filter_value=str(value))


class ServicesProcessFilter(ProcessFilter):
    """
    Filters processes by their associated services.

    :Usage:
        services_filter = ServicesProcessFilter("eq", "Spooler")
        command_parameter = services_filter.get_command() # /FI "SERVICES eq Spoole"
    """

    def __init__(self, operator: Literal["eq", "ne"], value: str):
        """
        Initializes a ServicesProcessFilter.

        Args:
            operator (Literal["eq", "ne"]): The comparison operator ("eq" or "ne").
            value (str): The service name to filter by.

        Raises:
            WrongCommandLineParameter: If an invalid operator is provided.
        """
        if operator not in ["eq", "ne"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for SERVICES filter. Valid operators {['eq', 'ne']}"
            )

        super().__init__(filter_name="SERVICES", filter_operator=operator, filter_value=value)


class ProcessID:
    """
    Represents a process ID for terminating a specific process.

    Attributes:
       process_id (int): The process ID.

    :Usage:
        process_id = ProcessID("1234")
        command_parameter = process_id.get_command()
    """

    def __init__(self, process_id: int):
        """
        Initializes a ProcessID object.

        Args:
            process_id (int):  The process ID.
        """
        self.process_id = process_id

    def get_command(self) -> str:
        return f"/PID {self.process_id}"


class PIDProcessFilter(ProcessFilter):
    """
    Filters processes by their process ID (PID).

    :Usage:
        pid_filter = PIDProcessFilter("gt", 1000)
        command_parameter = pid_filter.get_command() # /FI "PID gt 1000"
    """

    def __init__(self, operator: Literal["eq", "ne", "gt", "lt", "ge", "le"], value: str | int):
        """
        Initializes a PIDProcessFilter.

        Args:
            operator (Literal["eq", "ne", "gt", "lt", "ge", "le"]):  The comparison operator.
            value (str | int): The PID value to filter by.

        Raises:
             WrongCommandLineParameter: If an invalid operator is provided.
        """
        if operator not in ["eq", "ne", "gt", "lt", "ge", "le"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for IMAGENAME filter. Valid operators {['eq', 'ne', 'gt', 'lt', 'ge', 'le']}"
            )

        super().__init__(filter_name="PID", filter_operator=operator, filter_value=str(value))


class ModulesProcessFilter(ProcessFilter):
    """
    Filters processes by their loaded modules.

    :Usage:
        modules_filter = ModulesProcessFilter("eq", "user32.dll")
        command_parameter = modules_filter.get_command() # /FI "MODULES eq user32.dll"

    """

    def __init__(self, operator: Literal["eq", "ne"], value: str):
        """
        Initializes a ModulesProcessFilter.

        Args:
            operator (Literal["eq", "ne"]): The comparison operator ("eq" or "ne").
            value (str): The DLL name to filter by.

        Raises:
            WrongCommandLineParameter: If an invalid operator is provided.
        """
        if operator not in ["eq", "ne"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for MODULES filter. Valid operators {['eq', 'ne']}"
            )

        super().__init__(filter_name="MODULES", filter_operator=operator, filter_value=value)


class MemoryUsageProcessFilter(ProcessFilter):
    """
    Filters processes by their memory usage.

    :Usage:
        memory_filter = MemoryUsageProcessFilter("gt", "500000") # Greater than 500000 KB
        command_parameter = memory_filter.get_command() # /FI "MEMUSAGE gt 500000"
    """

    def __init__(self, operator: Literal["eq", "ne", "gt", "lt", "ge", "le"], value: str | int):
        """
        Initializes a MemoryUsageProcessFilter.

        Args:
            operator (Literal["eq", "ne", "gt", "lt", "ge", "le"]): The comparison operator.
            value (str | int): The memory usage value in KB.

        Raises:
            WrongCommandLineParameter: If an invalid operator is provided.
        """
        if operator not in ["eq", "ne", "gt", "lt", "ge", "le"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for MEMUSAGE filter. Valid operators {['eq', 'ne', 'gt', 'lt', 'ge', 'le']}"
            )

        super().__init__(filter_name="MEMUSAGE", filter_operator=operator, filter_value=str(value))


class ImageNameProcessFilter(ProcessFilter):
    """
    Filters processes by their image name.

    :Usage:
        image_name_filter = ImageNameProcessFilter("eq", "chrome.exe")
        command_parameter = image_name_filter.get_command() # /FI "IMAGENAME eq chrome.exe"
    """

    def __init__(self, operator: Literal["eq", "ne"], value: str):
        """
        Initializes an ImageNameProcessFilter.

        Args:
            operator (Literal["eq", "ne"]): The comparison operator ("eq" or "ne").
            value (str): The image name to filter by.

        Raises:
             WrongCommandLineParameter: If an invalid operator is provided.
        """
        if operator not in ["eq", "ne"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for IMAGENAME filter. Valid operators {['eq', 'ne']}"
            )

        super().__init__(filter_name="IMAGENAME", filter_operator=operator, filter_value=value)


class ImageName:
    """
    Represents an image name for terminating processes by their executable name.

    Attributes:
        image_name (str): The image name (e.g., "notepad.exe").

    :Usage:
        image_name = ImageName("chrome.exe")
        command_parameter = image_name.get_command()
    """

    def __init__(self, image_name: str):
        """
        Initializes an ImageName object.

        Args:
            image_name (str): The executable image name.
        """
        self.image_name = image_name

    def get_command(self) -> str:
        """
        Returns the command-line string for the image name.

        Returns:
            str: The formatted image name string.
        """
        return f"/IM {self.image_name}"


class CPUTimeProcessFilter(ProcessFilter):
    """
    Filters processes by their CPU time usage.

    :Usage:
        cpu_time_filter = CPUTimeProcessFilter("gt", 0, 15, 0) # Greater than 15 minutes
        command_parameter = cpu_time_filter.get_command() # /FI "CPUTIME gt 0:15:0"
    """

    def __init__(
        self,
        operator: Literal["eq", "ne", "gt", "lt", "ge", "le"],
        hours: str | int,
        minutes: str | int,
        seconds: str | int,
    ):
        """
        Initializes a CPUTimeProcessFilter.

        Args:
            operator (Literal["eq", "ne", "gt", "lt", "ge", "le"]): The comparison operator.
            hours (str | int):  The hours component of the CPU time.
            minutes (str | int):  The minutes component of the CPU time.
            seconds (str | int): The seconds component of the CPU time.

        Raises:
            WrongCommandLineParameter: If an invalid operator is provided.
        """
        if operator not in ["eq", "ne", "gt", "lt", "ge", "le"]:
            raise errors.WrongCommandLineParameter(
                f"Invalid '{operator}' operator for CPUTIME filter. Valid operators {['eq', 'ne', 'gt', 'lt', 'ge', 'le']}"
            )

        super().__init__(filter_name="CPUTIME", filter_operator=operator, filter_value=f"{hours}:{minutes}:{seconds}")
