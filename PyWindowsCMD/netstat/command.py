from PyWindowsCMD import errors
from typing import Literal, Optional


def build_netstat_routing_table_command() -> str:
	"""
	Builds the `netstat` command to display the routing table.

	Returns:
		str: The constructed `netstat` command.
	"""
	commands = ["netstat", "/r"]
	
	return " ".join(commands)


def build_netstat_per_protocol_statistics_command() -> str:
	"""
	Builds the `netstat` command to display per-protocol statistics.

	Returns:
		str: The constructed `netstat` command.

	Raises:
		WrongCommandLineParameter: If an invalid protocol is specified.
	"""
	
	commands = ["netstat", "/s"]
	return " ".join(commands)


def build_netstat_ethernet_statistics_command() -> str:
	"""
	Builds the `netstat` command to display Ethernet statistics.

	Returns:
		str: The constructed `netstat` command.
	"""
	commands = ["netstat", "/e"]
	
	return " ".join(commands)


def build_netstat_connections_list_command(
		show_all_listening_ports: bool = False,
		show_all_ports: bool = False,
		show_offload_state: bool = False,
		show_templates: bool = False,
		show_connections_exe: bool = False,
		show_connections_FQDN: bool = False,
		show_connection_pid: bool = False,
		show_connection_time_spent: bool = False,
		protocol: Optional[Literal["TCP", "TCPv6", "UDP", "UDPv6"]] = None,
) -> str:
	"""
	Builds the `netstat` command to display a list of active connections.

	Args:
		show_all_listening_ports (bool):  Displays all listening ports. Defaults to False.
		show_all_ports (bool): Displays all ports. Defaults to False.
		show_offload_state (bool): Shows the offload state. Defaults to False.
		show_templates (bool): Shows active TCP connections and the template used to create them. Defaults to False.
		show_connections_exe (bool): Displays the executable involved in creating each connection or listening port. Defaults to False.
		show_connections_FQDN (bool): Displays addresses and port numbers in fully qualified domain name (FQDN) format. Defaults to False.
		show_connection_pid (bool):  Displays the process ID (PID) associated with each connection. Defaults to False.
		show_connection_time_spent (bool): Displays the amount of time, in seconds, since the connection was established. Defaults to False.
		protocol (Optional[Literal["TCP", "TCPv6", "UDP", "UDPv6"]]): The protocol to filter connections by.  If None, displays connections for all specified protocols. Defaults to None.

	Returns:
		str: The constructed `netstat` command.

	Raises:
		WrongCommandLineParameter: If an invalid protocol is specified.
	"""
	commands = ["netstat", "/n"]
	
	if show_all_listening_ports:
		commands.append("/a")
	
	if show_all_ports:
		commands.append("/q")
	
	if show_connection_pid:
		commands.append("/o")
	
	if show_offload_state:
		commands.append("/t")
	
	if show_templates:
		commands.append("/y")
	
	if show_connection_time_spent:
		commands.append("/i")
	
	if show_connections_exe:
		commands.append("/b")
	
	if show_connections_FQDN:
		commands.append("/f")
	
	if protocol is not None:
		if protocol not in ["TCP", "TCPv6", "UDP", "UDPv6"]:
			raise errors.WrongCommandLineParameter("Wrong protocol.")
	
		commands.append(f"/p {protocol}")
	
	return " ".join(commands)
