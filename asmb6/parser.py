import re

# IPMI sensor type codes:
# 1   : Temperature
# 2   : Voltage
# 4   : Fan
# 5   : Physical Security
# 8   : PMB Power
# 12  : Memory ECC Sensor
# 13  : Drive Slot
# 35  : Watchdog
# 193 : OEM Memory ECC Sensor
# 220 : Node Manager capabilities


class Base:
    def __init__(self):
        self.reading = None
        self.unr = None
        self.uc = None
        self.unc = None
        self.lnr = None
        self.lc = None
        self.lnc = None
        self.state = None


class StateOnly:
    def __init__(self):
        self.state = None


class Temperature(Base):
    def __init__(self):
        super().__init__()


class Voltage(Base):

    def __init__(self):
        super().__init__()


class Fan(Base):
    def __init__(self):
        super().__init__()


class PowerSupply(Base):
    def __init__(self):
        super().__init__()


class Sensors:
    def __init__(self):
        self.cpu1: Temperature = Temperature()
        self.cpu2: Temperature = Temperature()
        self.tr1: Temperature = Temperature()
        self.tr2: Temperature = Temperature()
        self.vcore1: Voltage = Voltage()
        self.vcore2: Voltage = Voltage()
        self.vtt_cpu: Voltage = Voltage()
        self.vddq_ab_cpu1: Voltage = Voltage()
        self.vddq_cd_cpu1: Voltage = Voltage()
        self.vddq_ef_cpu2: Voltage = Voltage()
        self.vddq_gh_cpu2: Voltage = Voltage()
        self.v12: Voltage = Voltage()
        self.v5: Voltage = Voltage()
        self.vsb5: Voltage = Voltage()
        self.v3_3: Voltage = Voltage()
        self.vsb3_3: Voltage = Voltage()
        self.vbat: Voltage = Voltage()
        self.cpu_fan1: Fan = Fan()
        self.cpu_fan2: Fan = Fan()
        self.frnt_fan1: Fan = Fan()
        self.frnt_fan2: Fan = Fan()
        self.frnt_fan3: Fan = Fan()
        self.frnt_fan4: Fan = Fan()
        self.rear_fan1: Fan = Fan()
        self.rear_fan2: Fan = Fan()
        self.cpu1_ecc1: StateOnly = StateOnly()
        self.cpu1_ecc2: StateOnly = StateOnly()
        self.cpu2_ecc1: StateOnly = StateOnly()
        self.cpu2_ecc2: StateOnly = StateOnly()
        self.pmbpower: PowerSupply = PowerSupply()
        self.chassisintrusion: StateOnly = StateOnly()
        self.watchdog2: StateOnly = StateOnly()
        self.nm_capabilities: StateOnly = StateOnly()
        self.raw = {}
    
    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(key)


def serialize(raw):
    raw = raw.replace("=", ":")
    raw = raw.replace(";", "")
    raw = re.sub(r"(\b[A-Za-z_][A-Za-z0-9_]*\b)\s*:", r'"\1":', raw)
    raw = raw.replace("'", '"')
    return raw


def sanitize(text: str):
    return (
        "{"
        + "\n".join(filter(lambda x: not x.startswith("//"), text.split("\n")))
        + "}"
    )


def Parse_data(raw) -> Base:
    sensor: Base = Base()
    sensor.lnc = raw["LowNCThresh"]
    sensor.lc = raw["LowCTThresh"]
    sensor.lnr = raw["LowNRThresh"]
    sensor.unc = raw["HighNCThresh"]
    sensor.uc = raw["HighCTThresh"]
    sensor.unr = raw["HighNRThresh"]
    sensor.reading = raw["SensorReading"]/1000
    sensor.state = raw["SensorState"]
    return sensor


def parse_sensors(raw) -> Sensors:
    SensorsDict = {}
    for x in raw:
        if "SensorNumber" in x:
            SensorsDict[x["SensorNumber"]] = x

    sensors = Sensors()
    sensors.cpu1 = Parse_data(SensorsDict[49])
    sensors.cpu2 = Parse_data(SensorsDict[50])
    sensors.vcore1 = Parse_data(SensorsDict[52])
    sensors.vcore2 = Parse_data(SensorsDict[53])
    sensors.v3_3 = Parse_data(SensorsDict[54])
    sensors.v5 = Parse_data(SensorsDict[55])
    sensors.v12 = Parse_data(SensorsDict[56])
    sensors.vsb5 = Parse_data(SensorsDict[59])
    sensors.vbat = Parse_data(SensorsDict[60])
    sensors.vtt_cpu = Parse_data(SensorsDict[61])
    sensors.vsb3_3 = Parse_data(SensorsDict[64])
    sensors.vddq_ab_cpu1 = Parse_data(SensorsDict[77])
    sensors.vddq_cd_cpu1 = Parse_data(SensorsDict[78])
    sensors.vddq_ef_cpu2 = Parse_data(SensorsDict[80])
    sensors.vddq_gh_cpu2 = Parse_data(SensorsDict[81])
    sensors.cpu_fan1 = Parse_data(SensorsDict[160])
    sensors.cpu_fan2 = Parse_data(SensorsDict[161])
    sensors.frnt_fan1 = Parse_data(SensorsDict[162])
    sensors.frnt_fan2 = Parse_data(SensorsDict[163])
    sensors.frnt_fan3 = Parse_data(SensorsDict[164])
    sensors.frnt_fan4 = Parse_data(SensorsDict[165])
    sensors.rear_fan1 = Parse_data(SensorsDict[166])
    sensors.rear_fan2 = Parse_data(SensorsDict[167])
    sensors.tr1 = Parse_data(SensorsDict[204])
    sensors.tr2 = Parse_data(SensorsDict[205])
    sensors.nm_capabilities.state = SensorsDict[26]["SensorState"]
    sensors.chassisintrusion.state = SensorsDict[79]["SensorState"]
    sensors.cpu1_ecc1.state = SensorsDict[209]["SensorState"]
    sensors.cpu1_ecc2.state = SensorsDict[210]["SensorState"]
    sensors.cpu2_ecc1.state = SensorsDict[211]["SensorState"]
    sensors.cpu2_ecc2.state = SensorsDict[212]["SensorState"]
    sensors.watchdog2.state = SensorsDict[255]["SensorState"]
    sensors.raw=SensorsDict
    return sensors
