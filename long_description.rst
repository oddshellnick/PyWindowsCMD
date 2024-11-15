PyWindowsCMD: Simplify Windows Command-Line Interactions
========================================================

PyWindowsCMD is a Python library designed to streamline working with common Windows command-line tools. It provides convenient functions and parameter handling for commands like ``netstat``, ``shutdown``, and ``taskkill``, abstracting away the complexities of constructing and executing these commands directly.


Key Features
------------

* **Simplified Command Execution:**  Construct and execute Windows commands with intuitive function calls and parameter management.
* **Structured Output Parsing:** Process the output of commands like ``netstat`` into easy-to-use Pandas DataFrames.
* **Cross-Compatibility:** Designed to work seamlessly across various Windows versions.
* **Clear Documentation and Examples:** Well-documented code and usage examples to get you started quickly.


Current Functionality
---------------------

* **netstat:** Retrieve system network statistics, including active connections, routing tables, and interface information.  Parse the returned data directly into Pandas DataFrames. Conveniently find free ports on localhost.
* **shutdown:** Initiate shutdowns and restarts of local or remote Windows systems with various options (forceful shutdown, reason logging, timeout period, etc.).
* **taskkill:** Terminate processes based on various criteria such as image name or process ID.


Installation
------------

Install PyWindowsCMD using pip:

.. code-block:: bash

   pip install PyWindowsCMD


Usage Examples
--------------

**taskkill:**

.. code-block:: python

    from PyWindowsCMD.taskkill.parameters import ImageName
    from PyWindowsCMD.taskkill import taskkill_windows

    # Forcefully kill all notepad.exe processes
    taskkill_windows("/F", selectors=ImageName("notepad.exe"))

**netstat:**

.. code-block:: python

    from PyWindowsCMD.netstat import get_netstat_connections_data

    # Get all active TCP connections
    connections = get_netstat_connections_data(protocol="TCP")


**shutdown:**

.. code-block:: python

    from PyWindowsCMD.shutdown.parameters import ShutdownReason, ShutdownReasonType, ShutdownType
    from PyWindowsCMD.shutdown import shutdown_windows

    # Restart the local machine after 60 seconds, logging the reason
    shutdown_windows(ShutdownType.restart, time_out_period=60, shutdown_reason=ShutdownReason(ShutdownReasonType.planned, 4, 2))



More comprehensive usage examples and detailed documentation can be found within the project's source code docstrings.


Future Notes
------------

PyWindowsCMD is an ongoing project and will be expanded to support more Windows commands in the future. We welcome contributions from the community. Feel free to suggest new commands to be added or submit pull requests with your own implementations.

