import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from dataclasses import dataclass
from INA3221_linux import INA3221
import time
from datetime import datetime
from uuid import UUID
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource
import config


@dataclass
class INA3221Data:
    counter: int
    voltage_0: float
    current_0: float
    voltage_1: float
    current_1: float
    voltage_2: float
    current_2: float

@dataclass
class DeviceMap:
    id: UUID
    model: UUID
    type: str
    ina3221: INA3221
    data: INA3221Data

# Get default gateway ID or ID from input argument and then get corresponding configurations from config file
invalid = True
if len(config.GATEWAY_POWER_MONITORING) > 0:
    gateway_id = next(iter(config.GATEWAY_POWER_MONITORING))
    if len(sys.argv) > 1:
        gateway_id = sys.argv[1] if sys.argv[1] in config.GATEWAY_POWER_MONITORING else gateway_id
    GATEWAY = config.GATEWAY_POWER_MONITORING[gateway_id]
    if all(k in GATEWAY for k in ("bus", "period_time", "period_monitor")):
        invalid = False
if invalid:
    raise Exception("Gateway ID input is missing, invalid format, or invalid gateway configuration")

# user login
address_auth = config.SERVER_LOCAL['address_auth']
address_resource = config.SERVER_LOCAL['address_resource']
auth = Auth(address_auth)
login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
resource = Resource(address_resource, login.access_tokens[0].access_token)

print("LOGIN:")
print("user_id       = {}".format(login.user_id))
print("auth_token    = {}".format(login.auth_token))
for token in login.access_tokens:
    print("api_id        = {}".format(token.api_id))
    print("access_token  = {}".format(token.access_token))
    print("refresh_token = {}".format(token.refresh_token))

# read devices associated with configured gateway
device_map: list[DeviceMap] = []
devices = resource.list_device_by_gateway(UUID(gateway_id))

for device in devices:
    if device.id == device.gateway_id: # filter out gateway
        continue
    address = 0x00
    resistors = [0.1, 0.1, 0.1]
    conv_avg = 0x00
    conv_time = 0x04
    for conf in device.configs:
        if conf.name == "smbus_address":
            address = conf.value
        elif conf.name == "resistor_0":
            resistors[0] = conf.value
        elif conf.name == "resistor_1":
            resistors[1] = conf.value
        elif conf.name == "resistor_2":
            resistors[2] = conf.value
        elif conf.name == "conversion_average":
            conv_avg = conf.value
        elif conf.name == "conversion_time":
            conv_time = conf.value
    for model_id in device.type.models:
        model = resource.read_model(model_id)
        if model.category == "DATA": break

    # Initialize INA3221 instance and data
    ina3221 = INA3221(address=address, bus=GATEWAY["bus"])
    data = INA3221Data(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    device_map.append(DeviceMap(device.id, model_id, device.type.name, ina3221, data))
    # Begin INA3221 sensor
    if not ina3221.begin():
        print("Could not connect. Fix and Reboot")
    # Set custom shunt resistors
    ina3221.set_shunt_resistor(0, resistors[0])
    ina3221.set_shunt_resistor(0, resistors[1])
    ina3221.set_shunt_resistor(0, resistors[2])
    # Set conversion configuration
    ina3221.set_average(conv_avg)
    ina3221.set_bus_voltage_conversion_time(conv_time)
    ina3221.set_shunt_voltage_conversion_time(conv_time)

# Show devices
print("DEVICES:")
for device in device_map:
    print(f"{device.id}    {device.model}    {device.type}")
print()

t_monitor = time.time()
t_monitor = t_monitor - (t_monitor % GATEWAY["period_monitor"])
t_logger = time.time()
t_logger = t_logger - (t_logger % GATEWAY["period_time"])


while True:

    now = datetime.now().replace(microsecond=0)
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Get received data from node
    for device in device_map:

        # Accumulate voltage and current measurement
        device.data.counter += 1
        device.data.voltage_0 += device.ina3221.get_bus_voltage(0)
        device.data.current_0 += device.ina3221.get_current(0)
        device.data.voltage_1 += device.ina3221.get_bus_voltage(1)
        device.data.current_1 += device.ina3221.get_current(1)
        device.data.voltage_2 += device.ina3221.get_bus_voltage(2)
        device.data.current_2 += device.ina3221.get_current(2)
        # print(f"{now_str}    {device.data.counter}")

        # Average accumulated voltage and current measurement within a period of time
        if time.time() >= (t_logger + GATEWAY["period_time"]):
            t_logger += GATEWAY["period_time"]
            voltage_0 = device.data.voltage_0 / device.data.counter
            current_0 = device.data.current_0 / device.data.counter
            voltage_1 = device.data.voltage_1 / device.data.counter
            current_1 = device.data.current_1 / device.data.counter
            voltage_2 = device.data.voltage_2 / device.data.counter
            current_2 = device.data.current_2 / device.data.counter
            device.data = INA3221Data(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

            # Create buffer with data from voltage and current average data
            try:
                data = [GATEWAY["period_time"], voltage_0, current_0, voltage_1, current_1, voltage_2, current_2]
                resource.create_buffer(device.id, device.model, now, data, config.STATUS['logger_power_end'])
                print(f"{now_str}    {voltage_0:6.3f}    {current_0:6.3f}    {voltage_1:6.3f}    {current_1:6.3f}    {voltage_2:6.3f}    {current_2:6.3f}")
            except Exception as error:
                print(error)

    # print(f"{now_str}    {t_monitor}    {t_logger}")

    t_monitor += GATEWAY["period_monitor"]
    while time.time() < t_monitor:
        pass
