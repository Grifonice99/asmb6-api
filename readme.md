# ASMB6 API

A Python interface for interacting with the ASMB6-iKVM remote management module.

This library provides programmatic access to authentication, session handling, hardware monitoring, and basic power management functions through the module’s HTTP management interface.

---

## Overview

The ASMB6 API is designed as a lightweight Python wrapper around the module’s web-based management interface. It enables automation and integration into scripts or monitoring systems without relying on the WebUI.

The library provides:

* Session-based authentication
* Structured sensor objects
* Power and host state queries
* Programmatic power control operations

The goal is to expose a clean and predictable Python interface suitable for automation and monitoring tasks.

---

## Features

### Authentication & Session Management

* Login and logout support
* Session validation
* Explicit return codes for API calls

### Hardware Monitoring

* Temperature sensors
* Voltage sensors
* Fan speed monitoring
* Power supply status
* Structured `Sensors` container with parsed values
* Access to raw sensor payload for debugging

### Host Control & Status

* Retrieve host power state
* Query power button status
* Power control operations (shutdown, power on, reset, cycle)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Grifonice99/asmb6-api
cd asmb6-api
```

Install required dependency:

```bash
pip install requests
```

---

## Basic Usage

```python
from apmi import APMI

apmi = APMI("192.168.1.100")

# Authenticate
status = apmi.login("admin", "password")
if status != 0:
    raise RuntimeError(f"Login failed with code {status}")

# Query host power state
powered_on = apmi.status()
print("Host is on" if powered_on else "Host is off")

# Retrieve sensors
sensors = apmi.sensors()
print(sensors.cpu1.reading)

# Logout
apmi.logout()
```

---

## Design Notes

* Command execution methods return explicit status codes.
* Device state queries return domain-level values (e.g., `bool`).
* Sensor data is exposed through structured objects rather than raw dictionaries.
* Raw API payloads remain accessible for debugging or inspection purposes.

---

## Disclaimer

This project was developed and tested on an ASUS Z9PE-D16 motherboard equipped with an ASMB6-iKVM module.

Compatibility with other motherboards, firmware versions, or ASMB6 variants is not guaranteed. Behavior may differ depending on firmware revisions or platform-specific implementations.

Users are encouraged to test carefully in their own environment before relying on this library in production systems.

---

## License

This project is licensed under the terms defined in the `LICENSE` file.
