import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from dataclasses import dataclass
from smbus2 import SMBus
from bme280 import BME280
import time
from datetime import datetime
from uuid import UUID
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource
import config


@dataclass
class DeviceMap:
    id: UUID
    model: UUID
    type: str

# Get default gateway ID or ID from input argument and then get corresponding configurations from config file
invalid = True
if len(config.GATEWAY_ENVIRONMENT) > 0:
    gateway_id = next(iter(config.GATEWAY_ENVIRONMENT))
    if len(sys.argv) > 1:
        gateway_id = sys.argv[1] if sys.argv[1] in config.GATEWAY_ENVIRONMENT else gateway_id
    GATEWAY = config.GATEWAY_ENVIRONMENT[gateway_id]
    if all(k in GATEWAY for k in ("bus", "period_time")):
        if "frequency" not in GATEWAY: GATEWAY['address'] = 0x76
        invalid = False
if invalid:
    raise Exception("Gateway ID input is missing, invalid format, or invalid gateway configuration")

# Initialise the BME280
bus = SMBus(GATEWAY['bus'])
bme280 = BME280(i2c_dev=bus, i2c_addr=GATEWAY['address'])

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
    if device.id != device.gateway_id: # filter out gateway
        for model_id in device.type.models:
            model = resource.read_model(model_id)
            if model.category == "DATA":
                device_map.append(DeviceMap(device.id, model_id, device.type.name))
for device in device_map:
    print(device)


# read temperature, pressure, and humidity for the first time
for device in device_map:
    bme280.get_temperature()
    bme280.get_humidity()
    bme280.get_pressure()
time.sleep(0.1)

while True:

    if int(time.time()) % GATEWAY["period_time"] != 0:
        continue
    now = datetime.now().replace(microsecond=0)
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Get received data from node
    for device in device_map:

        try:
            # get temperature, humidity, and pressure from sensor
            temperature = bme280.get_temperature()
            humidity = bme280.get_humidity()
            pressure = bme280.get_pressure()
            data = [temperature, humidity, pressure]
            print("{0}    {1}    {2}".format(now_str, device.id, data))

            # Create buffer with data from request data
            resource.create_buffer(device.id, device.model, now, data, config.STATUS['logger_environment_end'])

        except Exception as error:
            print(error)

    while int(time.time()) % GATEWAY["period_time"] == 0:
        pass
