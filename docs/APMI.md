# APMI Class Documentation

## Overview

The `APMI` class provides an interface to interact with the ASMB6-iKVM module. It allows users to authenticate, manage sessions, retrieve sensor data, check the status of the host system, manage the host system and to retrive the jviewer.jnlp content.

---

## Class: `APMI`

### Constructor: `APMI(ip, http_port=80)`
- **Description**: Initializes the `APMI` instance with the target IP address and HTTP port.
- **Parameters**:
  - `ip` (str): The IP address of the ASMB6 module.
  - `http_port` (int, optional): The HTTP port to connect to (default is 80).

---
### Methods
- #### `login(username, password) -> dict`
  - **Description**: Authenticates the user with the ASMB6 module.
  - **Parameters**:
    - `username` (str): The username for authentication.
    - `password` (str): The password for authentication.
  - **Returns**:
    - `int`: Return code of the API call (0 if successful, otherwise an error code).
  - **Notes**:
    - Always call `logout()` before terminating the program to avoid leaving active sessions.


- #### `logout() -> int`
  - **Description**: Terminate the current session.    
  - **Returns**:
    - `int`:  Return code of the API call (0 if the session is valid, otherwise an error code).


- #### `validate_session() -> int`
  - **Description**: Validates the current session.
  - **Returns**:
    - `int`: Return code of the API call (0 if the session is valid, otherwise an error code).


- #### `sensors() -> Sensors`
  - **Description**: Retrieves and parses sensor data from the ASMB6 module.
  - **Returns**:
    - `Sensors`: A parsed object containing sensor data.


- #### `status() -> bool`
  - **Description**: Retrieves the current status of the host system.
  - **Returns**:
    - `bool`: `True` if the host system is powered on, otherwise `False`.


- #### `pwr_btn_status() -> bool`
  - **Description**: Retrieves the status of the power button.
  - **Returns**:
    - `bool`: `True` if the power button is enabled, otherwise `False`.


- #### `turn_off_board(immediate=False)`
  - **Description**: Turns off the host system.
  - **Parameters**:
    - `immediate` (bool, optional): If `True`, forces an immediate shutdown (default is `False`).


- #### `turn_on_board()`
  - **Description**: Turns on the host system.


- #### `power_cycle_board()`
  - **Description**: Power cycles the host system.


- #### `reset_board()`
  - **Description**: Resets the host system.


- #### `get_events() -> dict`
  - **Description**: Retrieves the event log from the ASMB6 module.
  - **Returns**:
    - `dict`: A dictionary containing event log entries.


- #### `get_jnlp() -> str`
  - **Description**: Retrieves the content of the `jviewer.jnlp` file.
  - **Returns**:
    - `str`: The content of the `jviewer.jnlp` file.
