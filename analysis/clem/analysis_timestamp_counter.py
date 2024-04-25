import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from dataclasses import dataclass
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

# User login on local server
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

# Get testing raw data and timestamp and counter model
models = resource.list_model_by_name("6 bytes testing")
model_raw = models[0]
models = resource.list_model_by_name("timestamp and counter")
model_data = models[0]

# Get testing devices
device_map: dict[UUID, Device] = {}
types = resource.list_type_by_name("timestamp and counter")
type_id = types[0].id
devices = resource.list_device_by_type(type_id)
for device in devices:
    device_map[device.id] = Device(device.serial_number)

print("TESTING MODEL")
print("{}: {}".format(model_raw.id, model_raw.name))
print("{}: {}".format(model_data.id, model_data.name))
print("DEVICES")
for device in devices:
    print("{}: {}".format(device.id, device.serial_number))

def get_i16_value(value0: int, value1: int) -> int:
    value = value0 * 256 + value1
    if value0 < 128:
        return value
    else:
        return (value - 65536)

def get_i32_value(value0: int, value1: int, value2: int, value3: int) -> int:
    value = value0 * 16777216 + value1 * 65536 + value2 * 256 + value3
    if value0 < 128:
        return value
    else:
        return (value - 4294967296)


while True:

    # read buffer based on raw model
    buffers = resource.list_buffer_first(10, None, model_raw.id, "ANALYSIS_1")
    # wait some moment when buffer is unavailable
    if len(buffers) == 0:
        time.sleep(config.TIMING['analysis_sleep'])
        continue

    for buffer in buffers:
        device = device_map[buffer.device_id]

        # calculate timestamp and counter
        timestamp = get_i32_value(buffer.data[0], buffer.data[1], buffer.data[2], buffer.data[3])
        counter = get_i16_value(buffer.data[4], buffer.data[5])

        # create data buffer for timestamp and counter and remove raw buffer
        data = [timestamp, counter]
        time_str = buffer.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        try:
            print("{}    {}    {}".format(time_str, buffer.device_id, data))
            resource.create_buffer(buffer.device_id, model_data.id, buffer.timestamp, data, "TRANSFER_LOCAL")
            resource.delete_buffer(buffer.id)
        except Exception as error:
            print(error)
