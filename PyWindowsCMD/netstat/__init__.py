import re
import pandas
from PyWindowsCMD import errors
from subprocess import PIPE, Popen
from typing import (
	Literal,
	Optional,
	Union
)
from PyWindowsCMD.netstat.command import (
	build_netstat_connections_list_command,
	build_netstat_ethernet_statistics_command,
	build_netstat_per_protocol_statistics_command,
	build_netstat_routing_table_command
)


def read_icmpv6_statistics(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses ICMPv6 statistics from "netstat /s" command output.

	Args:
		cmd_output (str): The output from the "netstat /s" command.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed statistics.

	Raises:
		NetstatOutputError: If no ICMPv6 statistics are found in the output.
	"""
	icmpv6_statistics_table = re.search(
			r"ICMPv6 Statistics(?:\r\n)+(.+?)(?:(?:\r\n){2}|\Z)",
			cmd_output,
			re.DOTALL
	)
	
	if icmpv6_statistics_table:
		icmpv6_statistics = re.findall(
				r"(\w+(?: \w+)*)\s{2,}(\d+)\s{2,}(\d+)",
				icmpv6_statistics_table.group(1)
		)
	
		for i in range(len(icmpv6_statistics)):
			icmpv6_statistics[i] = list(icmpv6_statistics[i])
			icmpv6_statistics[i][1] = int(icmpv6_statistics[i][1])
			icmpv6_statistics[i][2] = int(icmpv6_statistics[i][2])
	
		return pandas.DataFrame(icmpv6_statistics, columns=["Header", "Received", "Sent"])
	else:
		raise errors.NetstatOutputError("No ICMPv6 statistics found in the cmd_output.")


def read_icmpv4_statistics(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses ICMPv4 statistics from "netstat /s" command output.

	Args:
		cmd_output (str): The output from the "netstat /s" command.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed statistics.

	Raises:
		NetstatOutputError: If no ICMPv4 statistics are found in the output.
	"""
	icmpv4_statistics_table = re.search(
			r"ICMPv4 Statistics(?:\r\n)+(.+?)(?:(?:\r\n){2}|\Z)",
			cmd_output,
			re.DOTALL
	)
	
	if icmpv4_statistics_table:
		icmpv4_statistics = re.findall(
				r"(\w+(?: \w+)*)\s{2,}(\d+)\s{2,}(\d+)",
				icmpv4_statistics_table.group(1)
		)
	
		for i in range(len(icmpv4_statistics)):
			icmpv4_statistics[i] = list(icmpv4_statistics[i])
			icmpv4_statistics[i][1] = int(icmpv4_statistics[i][1])
			icmpv4_statistics[i][2] = int(icmpv4_statistics[i][2])
	
		return pandas.DataFrame(icmpv4_statistics, columns=["Header", "Received", "Sent"])
	else:
		raise errors.NetstatOutputError("No ICMPv4 statistics found in the cmd_output.")


def read_ipv6_statistics(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses IPv6 statistics from "netstat /s" command output.

	Args:
		cmd_output (str): The output from the "netstat /s" command.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed statistics.

	Raises:
		NetstatOutputError: If no IPv6 statistics are found in the output.
	"""
	ipv6_statistics_table = re.search(
			r"IPv6 Statistics(?:\r\n)+(.+?)(?:(?:\r\n){2}|\Z)",
			cmd_output,
			re.DOTALL
	)
	
	if ipv6_statistics_table:
		ipv6_statistics = re.findall(r"(\w+(?: \w+)*)\s{2,}= (\d+)", ipv6_statistics_table.group(1))
	
		for i in range(len(ipv6_statistics)):
			ipv6_statistics[i] = list(ipv6_statistics[i])
			ipv6_statistics[i][1] = int(ipv6_statistics[i][1])
	
		return pandas.DataFrame(ipv6_statistics, columns=["Header", "Value"])
	else:
		raise errors.NetstatOutputError("No IPv6 statistics found in the cmd_output.")


def read_ipv4_statistics(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses IPv4 statistics from "netstat /s" command output.

	Args:
		cmd_output (str): The output from the "netstat /s" command.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed statistics.

	Raises:
		NetstatOutputError: If no IPv4 statistics are found in the output.
	"""
	ipv4_statistics_table = re.search(
			r"IPv4 Statistics(?:\r\n)+(.+?)(?:(?:\r\n){2}|\Z)",
			cmd_output,
			re.DOTALL
	)
	
	if ipv4_statistics_table:
		ipv4_statistics = re.findall(r"(\w+(?: \w+)*)\s{2,}= (\d+)", ipv4_statistics_table.group(1))
	
		for i in range(len(ipv4_statistics)):
			ipv4_statistics[i] = list(ipv4_statistics[i])
			ipv4_statistics[i][1] = int(ipv4_statistics[i][1])
	
		return pandas.DataFrame(ipv4_statistics, columns=["Header", "Value"])
	else:
		raise errors.NetstatOutputError("No IPv4 statistics found in the cmd_output.")


def read_udp_ipv6_statistics(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses UDP statistics for IPv6 from "netstat /s" command output.

	Args:
		cmd_output (str): The output from the "netstat /s" command.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed statistics.

	Raises:
		NetstatOutputError: If no UDP statistics for IPv6 are found in the output.
	"""
	udp_ipv6_statistics_table = re.search(
			r"UDP Statistics for IPv6(?:\r\n)+(.+?)(?:(?:\r\n){2}|\Z)",
			cmd_output,
			re.DOTALL
	)
	
	if udp_ipv6_statistics_table:
		udp_ipv6_statistics = re.findall(r"(\w+(?: \w+)*)\s{2,}= (\d+)", udp_ipv6_statistics_table.group(1))
	
		for i in range(len(udp_ipv6_statistics)):
			udp_ipv6_statistics[i] = list(udp_ipv6_statistics[i])
			udp_ipv6_statistics[i][1] = int(udp_ipv6_statistics[i][1])
	
		return pandas.DataFrame(udp_ipv6_statistics, columns=["Header", "Value"])
	else:
		raise errors.NetstatOutputError("No UDP statistics for IPv6 found in the cmd_output.")


def read_udp_ipv4_statistics(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses UDP statistics for IPv4 from "netstat /s" command output.

	Args:
		cmd_output (str): The output from the "netstat /s" command.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed statistics.

	Raises:
		NetstatOutputError: If no UDP statistics for IPv4 are found in the output.
	"""
	udp_ipv4_statistics_table = re.search(
			r"UDP Statistics for IPv4(?:\r\n)+(.+?)(?:(?:\r\n){2}|\Z)",
			cmd_output,
			re.DOTALL
	)
	
	if udp_ipv4_statistics_table:
		udp_ipv4_statistics = re.findall(r"(\w+(?: \w+)*)\s{2,}= (\d+)", udp_ipv4_statistics_table.group(1))
	
		for i in range(len(udp_ipv4_statistics)):
			udp_ipv4_statistics[i] = list(udp_ipv4_statistics[i])
			udp_ipv4_statistics[i][1] = int(udp_ipv4_statistics[i][1])
	
		return pandas.DataFrame(udp_ipv4_statistics, columns=["Header", "Value"])
	else:
		raise errors.NetstatOutputError("No UDP statistics for IPv4 found in the cmd_output.")


def read_tcp_ipv6_statistics(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses TCP statistics for IPv6 from "netstat /s" command output.

	Args:
		cmd_output (str): The output from the "netstat /s" command.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed statistics.

	Raises:
		NetstatOutputError: If no TCP statistics for IPv6 are found in the output.
	"""
	
	tcp_ipv6_statistics_table = re.search(
			r"TCP Statistics for IPv6(?:\r\n)+(.+?)(?:(?:\r\n){2}|\Z)",
			cmd_output,
			re.DOTALL
	)
	
	if tcp_ipv6_statistics_table:
		tcp_ipv6_statistics = re.findall(r"(\w+(?: \w+)*)\s{2,}= (\d+)", tcp_ipv6_statistics_table.group(1))
	
		for i in range(len(tcp_ipv6_statistics)):
			tcp_ipv6_statistics[i] = list(tcp_ipv6_statistics[i])
			tcp_ipv6_statistics[i][1] = int(tcp_ipv6_statistics[i][1])
	
		return pandas.DataFrame(tcp_ipv6_statistics, columns=["Header", "Value"])
	else:
		raise errors.NetstatOutputError("No TCP statistics for IPv6 found in the cmd_output.")


def read_tcp_ipv4_statistics(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses TCP statistics for IPv4 from "netstat /s" command output.

	Args:
		cmd_output (str): The output from the "netstat /s" command.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed statistics.

	Raises:
		NetstatOutputError: If no TCP statistics for IPv4 are found in the output.
	"""
	tcp_ipv4_statistics_table = re.search(
			r"TCP Statistics for IPv4(?:\r\n)+(.+?)(?:(?:\r\n){2}|\Z)",
			cmd_output,
			re.DOTALL
	)
	
	if tcp_ipv4_statistics_table:
		tcp_ipv4_statistics = re.findall(r"(\w+(?: \w+)*)\s{2,}= (\d+)", tcp_ipv4_statistics_table.group(1))
	
		for i in range(len(tcp_ipv4_statistics)):
			tcp_ipv4_statistics[i] = list(tcp_ipv4_statistics[i])
			tcp_ipv4_statistics[i][1] = int(tcp_ipv4_statistics[i][1])
	
		return pandas.DataFrame(tcp_ipv4_statistics, columns=["Header", "Value"])
	else:
		raise errors.NetstatOutputError("No TCP statistics for IPv4 found in the cmd_output.")


def read_per_protocol_statistics(cmd_output: str) -> dict[str, pandas.DataFrame]:
	"""
	Parses all per-protocol statistics from "netstat /s" command output.

	Args:
		cmd_output (str): The output from the "netstat /s" command.

	Returns:
		dict[str, pandas.DataFrame]: A dictionary containing DataFrames for each protocol's statistics.  Keys are "IPv4", "IPv6", "ICMPv4", "ICMPv6", "TCPv4", "TCPv6", "UDPv4", and "UDPv6".
	"""
	return {
		"IPv4": read_ipv4_statistics(cmd_output),
		"IPv6": read_ipv6_statistics(cmd_output),
		"ICMPv4": read_icmpv4_statistics(cmd_output),
		"ICMPv6": read_icmpv6_statistics(cmd_output),
		"TCPv4": read_tcp_ipv4_statistics(cmd_output),
		"TCPv6": read_tcp_ipv6_statistics(cmd_output),
		"UDPv4": read_udp_ipv4_statistics(cmd_output),
		"UDPv6": read_udp_ipv6_statistics(cmd_output),
	}


def get_per_protocol_statistics(
		protocol: Optional[Literal["TCP", "UDP", "TCPv6", "UDPv6", "IP", "IPv6", "ICMP", "ICMPv6"]] = None
) -> Union[pandas.DataFrame, dict[str, pandas.DataFrame]]:
	"""
	Retrieves and parses per-protocol statistics using "netstat /s".

	Args:
		protocol (Optional[Literal["TCP", "UDP", "TCPv6", "UDPv6", "IP", "IPv6", "ICMP", "ICMPv6"]]):  The protocol to retrieve statistics for. If None, retrieves statistics for all protocols. Defaults to None.

	Returns:
		Union[pandas.DataFrame, dict[str, pandas.DataFrame]]:  The DataFrame containing statistics for the specified protocol or a dictionary of DataFrames for all protocols if None is provided.
	"""
	if protocol is None:
		return read_per_protocol_statistics(
				Popen(build_netstat_per_protocol_statistics_command(), stdout=PIPE, shell=True) .communicate()[0] .decode("windows-1252", errors="ignore")
		)
	else:
		cmd_output = (
				Popen(build_netstat_per_protocol_statistics_command(), stdout=PIPE, shell=True) .communicate()[0] .decode("windows-1252", errors="ignore")
		)
	
		if protocol == "TCP":
			return read_tcp_ipv4_statistics(cmd_output)
		elif protocol == "TCPv6":
			return read_tcp_ipv6_statistics(cmd_output)
		elif protocol == "UDP":
			return read_udp_ipv4_statistics(cmd_output)
		elif protocol == "UDPv6":
			return read_udp_ipv6_statistics(cmd_output)
		elif protocol == "IP":
			return read_ipv4_statistics(cmd_output)
		elif protocol == "IPv6":
			return read_ipv6_statistics(cmd_output)
		elif protocol == "ICMP":
			return read_icmpv4_statistics(cmd_output)
		elif protocol == "ICMPv6":
			return read_icmpv6_statistics(cmd_output)


def read_ipv6_routing_table(cmd_output: str) -> dict[str, pandas.DataFrame]:
	"""
	Parses the IPv6 routing table from the output of the "netstat /r" command.

	Args:
		cmd_output (str): The output of the "netstat /r" command.

	Returns:
		dict[str, pandas.DataFrame]: A dictionary containing a Pandas DataFrame for active IPv6 routes (and an empty DataFrame for persistent routes, which are not currently parsed).  Keys are "active_routes" and "persistent_routes".

	Raises:
		NetstatOutputError: If no IPv6 routing table is found in the output.
	"""
	ipv6_routing_table = re.search(
			r"IPv6 Route Table(?:\r\n)+={3,}\s+Active Routes:(?:\r\n)+(.+?)(?:={3,}|\Z)\s+Persistent Routes:(?:\r\n)+(.+?)(?:={3,}|\Z)",
			cmd_output,
			re.DOTALL,
	)
	
	if ipv6_routing_table:
		active_routes = re.findall(r"(\d+)\s+(\d+)\s+(\S+)\s+(On-link)\s+", ipv6_routing_table.group(1))
	
		return {
			"active_routes": pandas.DataFrame(
					active_routes,
					columns=["If", "Metric", "Network Destination", "Gateway"]
			),
			"persistent_routes": pandas.DataFrame(),
		}
	else:
		raise errors.NetstatOutputError("No IPv6 routing table found in the cmd_output.")


def read_ipv4_routing_table(cmd_output: str) -> dict[str, pandas.DataFrame]:
	"""
	Parses the IPv4 routing table from the output of the "netstat /r" command.

	Args:
		cmd_output (str):  The output of the "netstat /r" command.

	Returns:
		dict[str, pandas.DataFrame]: A dictionary containing Pandas DataFrames for active and persistent IPv4 routes. Keys are "active_routes" and "persistent_routes".

	Raises:
		NetstatOutputError: If no IPv4 routing table is found in the output.
	"""
	ipv4_routing_table = re.search(
			r"IPv4 Route Table(?:\r\n)+={3,}\s+Active Routes:(?:\r\n)+(.+?)(?:={3,}|\Z)\s+Persistent Routes:(?:\r\n)+(.+?)(?:={3,}|\Z)",
			cmd_output,
			re.DOTALL,
	)
	
	if ipv4_routing_table:
		active_routes = re.findall(
				r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|On-link)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)\s+",
				ipv4_routing_table.group(1),
		)
		persistent_routes = re.findall(
				r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)\s+",
				ipv4_routing_table.group(2),
		)
	
		return {
			"active_routes": pandas.DataFrame(
					active_routes,
					columns=["Network Destination", "Netmask", "Gateway", "Interface", "Metric"]
			),
			"persistent_routes": pandas.DataFrame(
					persistent_routes,
					columns=["Network Address", "Netmask", "Gateway Address", "Metric"]
			),
		}
	else:
		raise errors.NetstatOutputError("No IPv4 routing table found in the cmd_output.")


def read_interface_routing_table(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses the interface list from the output of the "netstat /r" command.

	Args:
		cmd_output (str): The output of the "netstat /r" command.

	Returns:
		pandas.DataFrame: A DataFrame containing MAC addresses and interface names.

	Raises:
		NetstatOutputError: If no Interface List is found in the output.
	"""
	interface_routing_table = re.search(r"Interface List(?:\r\n)+(.+?)(?:={3,}|\Z)", cmd_output, re.DOTALL)
	
	if interface_routing_table:
		interfaces = re.findall(
				r"(\w+(?:(?:\.{3}| )\w+)*) \.+([\w#() -]+)\s+",
				interface_routing_table.group(1)
		)
	
		return pandas.DataFrame(interfaces, columns=["MAC", "Interface"])
	else:
		raise errors.NetstatOutputError("No Interface List found in the cmd_output.")


def read_netstat_routing_tables(cmd_output: str) -> dict[str, Union[pandas.DataFrame, dict[str, pandas.DataFrame]]]:
	"""
	Parses all routing-related information from the output of "netstat /r".

	Args:
		cmd_output (str): The output of the "netstat /r" command.

	Returns:
		dict[str, Union[pandas.DataFrame, dict[str, pandas.DataFrame]]]: A dictionary containing DataFrames for interfaces, IPv4 routes, and IPv6 routes. Keys are "interface_table", "ipv4_routing_table", and "ipv6_routing_table".
	"""
	return {
		"interface_table": read_interface_routing_table(cmd_output),
		"ipv4_routing_table": read_ipv4_routing_table(cmd_output),
		"ipv6_routing_table": read_ipv6_routing_table(cmd_output),
	}


def get_netstat_routing_data() -> dict[str, Union[pandas.DataFrame, dict[str, pandas.DataFrame]]]:
	"""
	Retrieves and parses routing information using "netstat /r".

	Returns:
		dict[str, Union[pandas.DataFrame, dict[str, pandas.DataFrame]]]: A dictionary containing parsed routing tables (interfaces, IPv4, and IPv6).
	"""
	return read_netstat_routing_tables(
			Popen(build_netstat_routing_table_command(), stdout=PIPE, shell=True) .communicate()[0] .decode("windows-1252", errors="ignore")
	)


def get_netstat_ipv6_routing_data() -> dict[str, pandas.DataFrame]:
	"""
	Retrieves and parses IPv6 routing information using "netstat /r".

	Returns:
		dict[str, pandas.DataFrame]: A dictionary containing a DataFrame for active IPv6 routes.
	"""
	return read_ipv6_routing_table(
			Popen(build_netstat_routing_table_command(), stdout=PIPE, shell=True) .communicate()[0] .decode("windows-1252", errors="ignore")
	)


def get_netstat_ipv4_routing_data() -> dict[str, pandas.DataFrame]:
	"""
	Retrieves and parses IPv4 routing information using "netstat /r".

	Returns:
		dict[str, pandas.DataFrame]: A dictionary containing DataFrames for active and persistent IPv4 routes.
	"""
	return read_ipv4_routing_table(
			Popen(build_netstat_routing_table_command(), stdout=PIPE, shell=True) .communicate()[0] .decode("windows-1252", errors="ignore")
	)


def get_netstat_interface_routing_data() -> pandas.DataFrame:
	"""
	Retrieves and parses interface information using "netstat /r".

	Returns:
		pandas.DataFrame: A DataFrame with MAC addresses and interface names.
	"""
	return read_interface_routing_table(
			Popen(build_netstat_routing_table_command(), stdout=PIPE, shell=True) .communicate()[0] .decode("windows-1252", errors="ignore")
	)


def read_netstat_connections_list(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses the output of the "netstat" command with connection details.

	Args:
		cmd_output (str): The output string from "netstat".

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed connection information. Columns may vary depending on the "netstat" command options used.
	"""
	lines = list(filter(None, cmd_output.splitlines()))
	
	headers = re.findall(r"(\w+(?: \(?\w+\)?)*)", lines[1])
	
	regex_line = []
	
	for header in headers:
		if header == "Proto":
			regex_line.append(r"(TCP|UDP|TCPv6|UDPv6)")
		elif header == "Local Address":
			regex_line.append(r"((?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\[::\]):\d{1,5})")
		elif header == "Foreign Address":
			regex_line.append(r"((?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\[::\]|\*:\*):\d{1,5})")
		elif header == "State":
			regex_line.append(
					r"(LISTENING|ESTABLISHED|CLOSE_WAIT|TIME_WAIT|FIN_WAIT1|FIN_WAIT2|BOUND|)"
			)
		elif header == "PID":
			regex_line.append(r"(\d+)")
		elif header == "Time in State (ms)":
			regex_line.append(r"(\d+)")
		elif header == "Offload State":
			regex_line.append(r"(InHost|)")
		elif header == "Template":
			regex_line.append(r"(Not Applicable|Internet)")
	
	netstat_frame = pandas.DataFrame(
			re.findall(
					r"\s+".join(regex_line) +
					r"(?:\n\s*(\w+))?(?:\n\s*\[([\w.]+)])?\n",
					"\n".join(lines[2:])
			),
			columns=headers + ["Component", "Executable"],
	)
	
	if all(x == "" for x in netstat_frame["Component"]):
		netstat_frame = netstat_frame.drop("Component", axis="columns")
	
	if all(x == "" for x in netstat_frame["Executable"]):
		netstat_frame = netstat_frame.drop("Executable", axis="columns")
	
	return netstat_frame


def get_netstat_connections_data(
		show_all_listening_ports: bool = False,
		show_all_ports: bool = False,
		show_offload_state: bool = False,
		show_templates: bool = False,
		show_connections_exe: bool = False,
		show_connections_FQDN: bool = False,
		show_connection_pid: bool = False,
		show_connection_time_spent: bool = False,
		protocol: Optional[Literal["TCP", "TCPv6", "UDP", "UDPv6"]] = None,
) -> pandas.DataFrame:
	"""
	Retrieves and parses active connection information using "netstat".

	Args:
		show_all_listening_ports (bool): Displays all listening ports. Defaults to False.
		show_all_ports (bool):  Displays all ports. Defaults to False.
		show_offload_state (bool): Shows the offload state. Defaults to False.
		show_templates (bool): Shows active TCP connections and the template used to create them. Defaults to False.
		show_connections_exe (bool): Displays the executable involved in creating each connection or listening port. Defaults to False.
		show_connections_FQDN (bool): Displays addresses and port numbers in fully qualified domain name (FQDN) format. Defaults to False.
		show_connection_pid (bool): Displays the process ID (PID) associated with each connection. Defaults to False.
		show_connection_time_spent (bool): Displays the amount of time, in seconds, since the connection was established. Defaults to False.
		protocol (Optional[Literal["TCP", "TCPv6", "UDP", "UDPv6"]]): The protocol to filter connections by. If None, displays connections for all specified protocols. Defaults to None.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed connection information.
	"""
	return read_netstat_connections_list(
			Popen(
					build_netstat_connections_list_command(
							show_all_listening_ports=show_all_listening_ports,
							show_all_ports=show_all_ports,
							show_offload_state=show_offload_state,
							show_templates=show_templates,
							show_connections_exe=show_connections_exe,
							show_connections_FQDN=show_connections_FQDN,
							show_connection_pid=show_connection_pid,
							show_connection_time_spent=show_connection_time_spent,
							protocol=protocol,
					),
					stdout=PIPE,
					shell=True,
			) .communicate()[0] .decode("windows-1252", errors="ignore")
	)


def get_localhost_processes_with_pids() -> dict[int, list[int]]:
	"""
	Gets active processes and their associated ports on localhost.

	Returns:
		dict[int, list[int]]: A dictionary mapping PIDs to a list of their localhost ports.
	"""
	netstat_connections = get_netstat_connections_data(show_all_ports=True, show_connection_pid=True)
	netstat_connections = netstat_connections.loc[
		netstat_connections["Local Address"].apply(
				lambda address: re.search(r"\A(127\.0\.0\.1|\[::]):\d+\Z", address) is not None
		)
	]
	
	return (
			netstat_connections.groupby(pandas.to_numeric(netstat_connections["PID"]))["Local Address"] .apply(
					lambda local_addresses: list(
							set(int(re.search(r":(\d+)\Z", address).group(1)) for address in local_addresses)
					)
			) .to_dict()
	)


def get_localhost_busy_ports() -> list[int]:
	"""
	Gets all busy ports on localhost.

	Returns:
		list[int]: A list of busy localhost ports.
	"""
	ports = get_netstat_connections_data(show_all_ports=True)
	
	return list(
			set(
					ports.loc[
						ports["Local Address"].apply(
								lambda address: re.search(r"\A(127\.0\.0\.1|\[::]):\d+\Z", address) is not None
						)
					]["Local Address"] .apply(lambda address: int(re.search(r":(\d+)", address).group(1))) .tolist()
			)
	)


def get_localhost_free_ports() -> list[int]:
	"""
	Gets all free ports on localhost (1024-49150).

	Returns:
		list[int]: A list of free localhost ports.
	"""
	busy_ports = get_localhost_busy_ports()
	return list(set(range(1024, 49151)) - set(busy_ports))


def get_localhost_minimum_free_port(ports_to_check: Optional[Union[int, list[int], set]] = None) -> int:
	"""
	Gets the minimum free port on localhost, checking a specific port or set of ports first.

	Args:
		ports_to_check (Optional[Union[int, list[int], set]]): A single port, a list of ports, or a set of ports to check first.
			If None, defaults to finding the minimum free port in the range 1024-49150.

	Returns:
		int: The minimum free localhost port (or the first available port from "ports_to_check" if found).

	Raises:
		ValueError: If "ports_to_check" is a list or set containing non-integer values.
	"""
	localhost_free_ports = get_localhost_free_ports()
	
	if isinstance(ports_to_check, int):
		return ports_to_check if ports_to_check in localhost_free_ports else min(localhost_free_ports)
	elif isinstance(ports_to_check, (list, set)):
		if not all(isinstance(port, int) for port in ports_to_check):
			raise ValueError("All ports must be int.")
	
		found_subset = set(ports_to_check) & set(localhost_free_ports)
		return min(found_subset) if found_subset else min(localhost_free_ports)
	else:
		return min(localhost_free_ports)


def read_ethernet_statistics(cmd_output: str) -> pandas.DataFrame:
	"""
	Parses ethernet statistics from "netstat -e" command output.

	Args:
		cmd_output (str): The output from the "netstat -e" command.

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed ethernet statistics.
	"""
	interfaces = re.findall(r"([\w-]+(?: [\w-]+)*)\s{2,}(\d+)\s{2,}(\d*)", cmd_output)
	
	for i in range(len(interfaces)):
		interfaces[i] = list(interfaces[i])
	
		interfaces[i][1] = int(interfaces[i][1])
		interfaces[i][2] = int(interfaces[i][2]) if interfaces[i][2] else 0
	
	return pandas.DataFrame(interfaces, columns=["Interface", "Received", "Sent"])


def get_ethernet_statistics() -> pandas.DataFrame:
	"""
	Retrieves and parses ethernet interface statistics using "netstat -e".

	Returns:
		pandas.DataFrame: A DataFrame containing the parsed ethernet statistics.
	"""
	return read_ethernet_statistics(
			Popen(build_netstat_ethernet_statistics_command(), stdout=PIPE, shell=True) .communicate()[0] .decode("windows-1252", errors="ignore")
	)
