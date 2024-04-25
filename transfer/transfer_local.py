import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from dataclasses import dataclass
import time
from datetime import datetime
from uuid import UUID
import grpc
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource, DeviceSchema
import config


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

# Get RAW, DATA, and ANALISYS models
models = resource.list_model_by_category("RAW")
models_raw: dict[UUID, str] = {}
for model in models:
    models_raw[model.id] = model.name
models = resource.list_model_by_category("DATA")
models_data: dict[UUID, str] = {}
for model in models:
    models_data[model.id] = model.name
models = resource.list_model_by_category("ANALYSIS")
models_analysis: dict[UUID, str] = {}
for model in models:
    models_analysis[model.id] = model.name

# read devices on the gateways
devices: list[DeviceSchema] = []
for gateway_id in config.GATEWAYS:
    device_list = resource.list_device_by_gateway(UUID(gateway_id))
    for index, device in enumerate(device_list):
        if device.id == device.gateway_id:
            device_list.pop(index)
    devices = devices + device_list

print("RAW MODELS:")
for model_id, model_name in models_raw.items():
    print("{}: {}".format(model_id, model_name))
print("DATA MODELS:")
for model_id, model_name in models_data.items():
    print("{}: {}".format(model_id, model_name))
print("ANALYSIS MODELS:")
for model_id, model_name in models_analysis.items():
    print("{}: {}".format(model_id, model_name))
print("DEVICES:")
device_map = {}
for device in devices:
    print("{}: {}".format(device.id, device.name))
    device_map[device.id] = device.name


while True:

    buffers = []
    try:
        buffers = resource.list_buffer_first(100, None, None, "TRANSFER_LOCAL")
    except grpc.RpcError as error:
        if error.code() == grpc.StatusCode.UNAUTHENTICATED:
            login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
            resource = Resource(address_resource, login.access_tokens[0].access_token)
            print("RELOGIN LOCAL")
        continue

    for buffer in buffers:

        # check if a buffer has associated device
        try:
            time_str = buffer.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if buffer.device_id not in device_map:
                resource.delete_buffer(buffer.id)
                continue
            print("{}    {}    {}".format(time_str, buffer.device_id, device_map[buffer.device_id]))
        except grpc.RpcError as error:
            print(error)

        # try to create data on local database
        renew_flag = False
        try:
            resource.create_data(buffer.device_id, buffer.model_id, buffer.timestamp, buffer.data)
        except grpc.RpcError as error:
            print(error)
            # check if data already exist
            try:
                resource.read_data(buffer.device_id, buffer.model_id, buffer.timestamp)
                renew_flag = True
            except grpc.RpcError as error:
                print(error)

        # renew data when create data error and old data exists
        if renew_flag:
            try:
                resource.delete_data(buffer.device_id, buffer.model_id, buffer.timestamp)
                resource.create_data(buffer.device_id, buffer.model_id, buffer.timestamp, buffer.data)
            except grpc.RpcError as error:
                print(error)

        # delete buffer only if data on local exists for raw model 
        # or update status to transfer server for data and analysis buffer
        try:
            if buffer.model_id in models_raw:
                resource.delete_buffer(buffer.id)
            else:
                resource.update_buffer(buffer.id, None, "TRANSFER_SERVER")
        except grpc.RpcError as error:
            print(error)

    time.sleep(config.TIMING['transfer_sleep'])
