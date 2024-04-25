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
class DeviceMap:
    id: UUID
    serial_number: str
    offset_x: int
    offset_y: int
    offset_z: int
    position: int
    space: int

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

# get model of raw accelerometer and soil inclinometer data
models = resource.list_model_by_name("3-axis 16-bit accelerometer")
model_raw = models[0]
models = resource.list_model_by_name("XZ-axis soil inclinometer")
model_data = models[0]

# get soil inclinometer group and devices
devices_map: List[DeviceMap] = []
group = resource.read_group_device(UUID(config.SOIL_INCLINOMETER_GROUP_ID))
if group.name == "soil inclinometer":
    if len(group.devices) == 0: 
        raise Exception("Group has no device")
    for device_id in group.devices:
        device = resource.read_device(device_id)
        offset_x = None
        offset_y = None
        offset_z = None
        space = None
        position = None
        for conf in device.configs:
            if conf.name == "offset-X":
                offset_x = conf.value
            elif conf.name == "offset-Y":
                offset_y = conf.value
            elif conf.name == "offset-Z":
                offset_z = conf.value
            elif conf.name == "space":
                space = conf.value
            elif conf.name == "position":
                position = conf.value
        # check for all necessary device config
        if offset_x != None and offset_y != None and offset_z != None and space != None and position != None:
            device_map = DeviceMap(device_id, device.serial_number, offset_x, offset_y, offset_z, position, space)
            devices_map.append(device_map)
# rearrange devices based on position
number = len(devices_map)
devices: List[DeviceMap] = []
for i in range(number):
    for device in devices_map:
        if device.position == (i + 1):
            devices.append(device)
            break

print("SOIL INCLINOMETER MODEL")
print("{}: {}".format(model_raw.id, model_raw.name))
print("{}: {}".format(model_data.id, model_data.name))
print("SOIL INCLINOMETER GROUP")
print(group.id)
print("DEVICES")
for device in devices:
    print("{}: {}".format(device.id, device.serial_number))

def get_i16_value(u16_value: int, offset: int) -> int:
    if u16_value < 32768:
        return (u16_value - offset)
    else:
        return (u16_value - 65536 - offset)


while True:

    # read buffers based on raw model limited by device number
    buffers = resource.list_buffer_first(number, None, model_raw.id, "ANALYSIS_1")
    # wait some moment when available buffers lower than device number
    if number > len(buffers):
        time.sleep(config.TIMING['analysis_sleep'])
        continue

    # check buffers validity, all buffer set member must have same timestamp
    buffer_set: List[BufferSchema] = []
    timestamp = buffers[0].timestamp
    valid = True
    for buffer in buffers:
        if buffer.timestamp == timestamp:
            buffer_set.append(buffer)
        else:
            valid = False
            break
    if not valid:
        # remove some first buffers if buffer set invalid
        for buffer in buffer_set:
            try:
                resource.update_buffer(buffer.id, None, "TRANSFER_LOCAL")
            except Exception as error:
                print(error)
        continue

    # rearrange buffers based on device arrangement
    buffers: List[BufferSchema] = []
    timestamp = buffer_set[0].timestamp
    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    for device in devices:
        for buffer in buffer_set:
            if buffer.device_id == device.id:
                buffers.append(buffer)
                break

    # Calculate acceleration, angle, and displacement
    displacement_x = 0.0
    displacement_z = 0.0
    last_angle_x = 0.0
    last_angle_z = 0.0

    for i in range(number):
        ax = get_i16_value(buffers[i].data[0], devices[i].offset_x)
        ay = get_i16_value(buffers[i].data[1], devices[i].offset_y)
        az = get_i16_value(buffers[i].data[2], devices[i].offset_z) + 4096

        angle_x = math.atan(ax / math.sqrt(ay * ay + az * az))
        angle_z = math.atan(az / math.sqrt(ax * ax + ay * ay))

        if i > 0:
            displacement_x = displacement_x + devices[i].space * math.sin((last_angle_x + angle_x) / 2)
            displacement_z = displacement_z + devices[i].space * math.sin((last_angle_z + angle_z) / 2)
        last_angle_x = angle_x
        last_angle_z = angle_z

        # create data buffer for soil inclinometer and remove raw buffer
        data = [ax/4096.0, ay/4096.0, az/4096.0, angle_x, angle_z, displacement_x, displacement_z]
        try:
            print("{}    {}    {}".format(time_str, devices[i].id, data))
            resource.create_buffer(devices[i].id, model_data.id, buffers[i].timestamp, data, "TRANSFER_LOCAL")
            resource.update_buffer(buffers[i].id, None, "TRANSFER_LOCAL")
        except Exception as error:
            print(error)
