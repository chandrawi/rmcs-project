import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from dataclasses import dataclass
from typing import List, Dict
import time
from datetime import datetime
from uuid import UUID
import math
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource, BufferSchema
import config


@dataclass
class Device:
    serial_number: str
    coefficient: float

# user login on local server
address_auth = config.SERVER_LOCAL['address_auth']
address_resource = config.SERVER_LOCAL['address_resource']
auth = Auth(address_auth)
login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
resource = Resource(address_resource, login.access_tokens[0].access_token)

print("LOCAL LOGIN:")
print("user_id       = {}".format(login.user_id))
print("auth_token    = {}".format(login.auth_token))
for token in login.access_tokens:
    print("api_id        = {}".format(token.api_id))
    print("access_token  = {}".format(token.access_token))
    print("refresh_token = {}".format(token.refresh_token))

# get model of accelerometer raw and data
models = resource.list_model_by_name("rain gauge raw data")
model_raw = models[0]
models = resource.list_model_by_name("rain gauge data")
model_data = models[0]

# get rain gauge devices
device_map: Dict[UUID, Device] = {}
types = resource.list_type_by_name("rain gauge")
type_id = types[0].id
devices = resource.list_device_by_type(type_id)
for device in devices:
    coefficient = None
    for conf in device.configs:
        if conf.name == "coefficient":
            coefficient = conf.value
    # check for all necessary device config
    if coefficient != None:
        device_map[device.id] = Device(device.serial_number, coefficient)

print("RAIN GAUGE MODEL")
print("{}: {}".format(model_raw.id, model_raw.name))
print("{}: {}".format(model_data.id, model_data.name))
print("DEVICES")
for device in devices:
    print("{}: {}".format(device.id, device.serial_number))

def get_i16_value(u16_value: int, offset: int) -> int:
    if u16_value < 32768:
        return (u16_value - offset)
    else:
        return (u16_value - 65536 - offset)


while True:

    # read buffer based on raw model
    buffers = resource.list_buffer_first(10, None, model_raw.id, "ANALYSIS_1")
    # wait some moment when buffer is unavailable
    if len(buffers) == 0:
        time.sleep(config.TIMING['analysis_sleep'])
        continue

    for buffer in buffers:
        device = device_map[buffer.device_id]

        # calculate rain fall
        rain_yesterday = get_i16_value(buffer.data[0], 0) * device.coefficient
        rain_daily = get_i16_value(buffer.data[1], 0) * device.coefficient
        rain_last_hour = get_i16_value(buffer.data[2], 0) * device.coefficient
        rain_hourly = get_i16_value(buffer.data[3], 0) * device.coefficient

        # create data buffer for rain gauge and remove raw buffer
        data = [rain_yesterday, rain_daily, rain_last_hour, rain_hourly]
        time_str = buffer.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        try:
            print("{}    {}    {}".format(time_str, buffer.device_id, data))
            resource.create_buffer(buffer.device_id, model_data.id, buffer.timestamp, data, "TRANSFER_LOCAL")
            resource.update_buffer(buffer.id, None, "TRANSFER_LOCAL")
        except Exception as error:
            print(error)
