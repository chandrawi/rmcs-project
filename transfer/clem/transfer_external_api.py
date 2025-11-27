import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import time
import datetime
from uuid import UUID
import grpc
import requests
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource, ModelSchema, DeviceSchema, Tag
import config


# Shift period in seconds and offset from 00:00:00 in seconds
DAY_IN_SEC = 86400
SHIFT_PERIOD = 43200
SHIFT_OFFSET = 21600

def getDateShift(timestamp: datetime.datetime) -> tuple[datetime.date, int]:
    t = timestamp.timestamp() - time.timezone - SHIFT_OFFSET
    dt = datetime.datetime.fromtimestamp(t, datetime.timezone.utc)
    if (t % DAY_IN_SEC) < SHIFT_PERIOD:
        return (dt.date(), 1)
    else:
        return (dt.date(), 2)

def post_running_hour_sensor(
        serial_number: str, 
        date: datetime.date, 
        shift: int, 
        time_begin: datetime.datetime, 
        time_end: datetime.datetime,
        index: int
    ):
    payloads = {
        "date": date.strftime("%Y-%m-%d"),
        "shift": "shift_" + str(shift),
        "unique_code": str(serial_number),
        "hour_type": "jam_ke_" + str(index),
        "start": time_begin.strftime("%H:%M:%S"),
        "finish": time_end.strftime("%H:%M:%S")
    }
    headers = {
        "Authorization": "Bearer " + str(config.EXTERNAL_API["token"])
    }
    r = requests.post(config.EXTERNAL_API["url"], json=payloads, headers=headers)
    return r.status_code

def transfer_external_api(model: ModelSchema, serial_number: str, timestamp: datetime.datetime, data: list):
    if model.name == "running hour sensor":
        try:
            index = 1
            duration = data[0]
            if len(data) > 1:
                index = data[0] + 1
                duration = data[1]
            date, shift = getDateShift(timestamp)
            time_end = timestamp + datetime.timedelta(seconds=duration)
            return post_running_hour_sensor(serial_number, date, shift, timestamp, time_end, index)
        except Exception as error:
            print(error)
            return 0
    else:
        print("Model is not recognized")
        return 0


# user login on local server
address_auth = config.SERVER_LOCAL['address_auth']
address_resource = config.SERVER_LOCAL['address_resource']
auth = Auth(address_auth)
login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
resource = Resource(address_resource, login.access_tokens[0].access_token)

print("LOCAL LOGIN:")
print("user_id       = {}".format(login.user_id))
print("auth_token    = {}".format(login.auth_token))

# get raw and data models
models_data = resource.list_model_by_category("DATA")
models_analysis = resource.list_model_by_category("ANALYSIS")
model_map: dict[UUID, ModelSchema] = {}
print("MODEL")
for model in models_data:
    model_map[model.id] = model
    print("{}: {}".format(model.id, model.name))
for model in models_analysis:
    model_map[model.id] = model
    print("{}: {}".format(model.id, model.name))

# read devices on the gateways
devices: list[DeviceSchema] = []
for gateway_id in config.GATEWAYS:
    device_list = resource.list_device_by_gateway(UUID(gateway_id))
    for index, device in enumerate(device_list):
        if device.id == device.gateway_id:
            device_list.pop(index)
    devices = devices + device_list

print("DEVICES:")
device_map = {}
for device in devices:
    print("{}: {}  {}".format(device.id, device.serial_number, device.name))
    device_map[device.id] = device.serial_number


while True:

    # read buffers
    buffers = []
    try:
        buffers = resource.list_buffer_group_first(25, device_map.keys(), None, config.STATUS['transfer_external_api_begin'])
    except grpc.RpcError as error:
        if error.code() == grpc.StatusCode.UNAUTHENTICATED:
            login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
            resource = Resource(address_resource, login.access_tokens[0].access_token)
            print("RELOGIN LOCAL")
        # continue

    # create data from buffer
    for buffer in buffers:
        time_str = buffer.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print("{}    {}    {}".format(time_str, buffer.device_id, device_map[buffer.device_id]))

        # transfer data through external api
        code = 0
        try:
            if buffer.model_id in model_map:
                code = transfer_external_api(model_map[buffer.model_id], device_map[buffer.device_id], buffer.timestamp, buffer.data)
        except Exception as error:
            print(error)

        # print message
        time_str = buffer.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print("{}    {}    {}    {}".format(time_str, buffer.device_id, device_map[buffer.device_id], code))

        # delete or update status based on configuration only if response code is 201
        if code == 201:
            try:
                if config.STATUS['transfer_external_api_end'] == Tag.DELETE:
                    resource.delete_buffer(buffer.id)
                else:
                    resource.update_buffer(buffer.id, None, config.STATUS['transfer_external_api_end'])
            except grpc.RpcError as error:
                print(error)

    time.sleep(config.TIMING['transfer_sleep'])
