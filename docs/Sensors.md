# Sensor Model Documentation

## Overview

The sensor model provides structured representations of hardware monitoring data retrieved from the ASMB6 module.

Each sensor type encapsulates threshold values, current readings, and state information as reported by the reverse-engineered HAPI interface.

The `Sensors` class aggregates all available sensors into a single structured object.

---

## Class: `base`

### Description

Base class for numeric sensors that provide readings and threshold values.

### Attributes

* `reading` (`float | int | None`)
  Current sensor reading.

* `unr` (`float | int | None`)
  Upper Non-Recoverable threshold.

* `uc` (`float | int | None`)
  Upper Critical threshold.

* `unc` (`float | int | None`)
  Upper Non-Critical threshold.

* `lnr` (`float | int | None`)
  Lower Non-Recoverable threshold.

* `lc` (`float | int | None`)
  Lower Critical threshold.

* `lnc` (`float | int | None`)
  Lower Non-Critical threshold.

* `state` (`int | None`)
  Sensor state value as reported by the HAPI interface.

---

## Class: `Temperature`

### Description

Represents a temperature sensor.

Inherits all attributes from `base`.

---

## Class: `Voltage`

### Description

Represents a voltage sensor.

Inherits all attributes from `base`.

---

## Class: `Fan`

### Description

Represents a fan speed sensor.

Inherits all attributes from `base`.

---

## Class: `PowerSupply`

### Description

Represents a power supply monitoring sensor.

Inherits all attributes from `base`.

---

## Class: `StateOnly`

### Description

Represents a state-only sensor without numeric readings or threshold values.

### Attributes

* `state` (`int | None`)
  State value as reported by the HAPI interface.

---

## Class: `Sensors`

### Description

Container class that aggregates all available hardware sensors into a structured object.

Each attribute corresponds to a specific physical sensor or system status indicator.

### Temperature Sensors (`Temperature`)

* `cpu1`
* `cpu2`
* `tr1`
* `tr2`

### Voltage Sensors (`Voltage`)

* `vcore1`
* `vcore2`
* `vtt_cpu`
* `vddq_ab_cpu1`
* `vddq_cd_cpu1`
* `vddq_ef_cpu2`
* `vddq_gh_cpu2`
* `v12`
* `v5`
* `vsb5`
* `v3_3`
* `vsb3_3`
* `vbat`

### Fan Sensors (`Fan`)

* `cpu_fan1`
* `cpu_fan2`
* `frnt_fan1`
* `frnt_fan2`
* `frnt_fan3`
* `frnt_fan4`
* `rear_fan1`
* `rear_fan2`

### Power Supply Sensors (`PowerSupply`)

* `pmbpower`

### State-Only Sensors (`StateOnly`)

* `cpu1_ecc1`
* `cpu1_ecc2`
* `cpu2_ecc1`
* `cpu2_ecc2`
* `chassisintrusion`
* `watchdog2`
* `nm_capabilities`

### Raw Data

* `raw` (`dict`)
  Contains the unprocessed raw sensor data returned by the HAPI API.
