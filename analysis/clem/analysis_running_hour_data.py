import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from dataclasses import dataclass
import time
from datetime import datetime
from uuid import UUID
import math
import grpc
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource, BufferSchema
import config


@dataclass
class Device:
    serial_number: str
    aenergy_os: int
    vaenergy_os: int
    aenergy_coef: float
    vaenergy_coef: float
    ipeak_coef: float
    vpeak_coef: float
    clk_freq: float
    running_ths: float


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

# Get running hour raw data and basic data model
models = resource.list_model_by_name("running hour raw data")
model_raw = models[0]
models = resource.list_model_by_name("running hour basic data")
model_data = models[0]

# Get running hour devices
device_map: dict[UUID, Device] = {}
types = resource.list_type_by_name("running hour sensor")
type_id = types[0].id
devices = resource.list_device_by_type(type_id)
for device in devices:
    ae_os = None
    vae_os = None
    ae_c = None
    vae_c = None
    ip_c = None
    vp_c = None
    clk = None
    r_ths = None
    for conf in device.configs:
        if conf.name == "aenergy_offset":
            ae_os = conf.value
        elif conf.name == "vaenergy_offset":
            vae_os = conf.value
        elif conf.name == "aenergy_coefficient":
            ae_c = conf.value
        elif conf.name == "vaenergy_coefficient":
            vae_c = conf.value
        elif conf.name == "ipeak_coefficient":
            ip_c = conf.value
        elif conf.name == "vpeak_coefficient":
            vp_c = conf.value
        elif conf.name == "clock_frequency":
            clk = conf.value
        elif conf.name == "running_threshold":
            r_ths = conf.value
    # check for all necessary device config
    if ae_os != None and vae_os != None and ae_c != None and vae_c != None and ip_c != None and vp_c != None and clk != None and r_ths != None:
        device_map[device.id] = Device(device.serial_number, ae_os, vae_os, ae_c, vae_c, ip_c, vp_c, clk, r_ths)
if len(device_map) == 0:
    raise Exception("no device with specified type and config found")

print("RUNNING HOUR MODEL")
print("{}: {}".format(model_raw.id, model_raw.name))
print("{}: {}".format(model_data.id, model_data.name))
print("DEVICES")
for id, device in device_map.items():
    print("{}: {}".format(id, device.serial_number))

def get_u16_value(value0: int, value1: int, offset: int = 0) -> int:
    value = value0 * 256 + value1
    return (value - offset)

def get_i24_value(value0: int, value1: int, value2: int, offset: int = 0) -> int:
    value = value0 * 65536 + value1 * 256 + value2
    if value0 < 128:
        return (value - offset)
    else:
        return (value - 16777216 - offset)

def get_u24_value(value0: int, value1: int, value2: int, offset: int = 0) -> int:
    value = value0 * 65536 + value1 * 256 + value2
    return (value - offset)


while True:

    buffers = []
    try:
        # read buffer based on raw model
        buffers = resource.list_buffer_first(10, None, model_raw.id, "ANALYSIS_1")
    except grpc.RpcError as error:
        if error.code() == grpc.StatusCode.UNAUTHENTICATED:
            login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
            resource = Resource(address_resource, login.access_tokens[0].access_token)
            print("RELOGIN LOCAL")
        continue
    # wait some moment when buffer is unavailable
    if len(buffers) == 0:
        time.sleep(config.TIMING['analysis_sleep'])
        continue

    for buffer in buffers:

        # get a device schema based on buffer
        device = device_map[buffer.device_id]

        # get raw data from buffer
        aenergy_raw = 0
        vaenergy_raw = 0
        period_raw = 0
        ipeak_raw = 0
        vpeak_raw = 0
        if len(buffer.data) == 14:
            aenergy_raw = get_i24_value(buffer.data[0], buffer.data[1], buffer.data[2], device.aenergy_os)
            if aenergy_raw < 0 and (aenergy_raw - device.aenergy_os) > 0:
                aenergy_raw = 0
            vaenergy_raw = get_u24_value(buffer.data[3], buffer.data[4], buffer.data[5], device.vaenergy_os)
            if vaenergy_raw < 0:
                vaenergy_raw = 0
            period_raw = get_u16_value(buffer.data[6], buffer.data[7])
            ipeak_raw = get_u24_value(buffer.data[8], buffer.data[9], buffer.data[10])
            vpeak_raw = get_u24_value(buffer.data[11], buffer.data[12], buffer.data[13])

        # determine working status based on active energy
        if aenergy_raw > device.running_ths:
            status = 2
        # elif aenergy_raw > device.standby_ths:
        #     status = 1
        else:
            status = 1

        # calculate active and apparent energy, frequency, and peak current and voltage
        aenergy = aenergy_raw * device.aenergy_coef
        vaenergy = vaenergy_raw * device.vaenergy_coef
        if period_raw == 0:
            frequency = 0.0
        else:
            frequency = (device.clk_freq / 8.0) / period_raw
        ipeak = device.ipeak_coef * ipeak_raw
        vpeak = device.vpeak_coef * vpeak_raw

        # create data buffer for timestamp and counter and remove raw buffer
        data = [aenergy, vaenergy, frequency, ipeak, vpeak, status]
        time_str = buffer.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        try:
            print("{}    {}    {}".format(time_str, buffer.device_id, data))
            resource.create_buffer(buffer.device_id, model_data.id, buffer.timestamp, data, "TRANSFER_LOCAL")
            resource.update_buffer(buffer.id, None, "TRANSFER_LOCAL")
        except grpc.RpcError as error:
            print(error)
            # check if buffer already exist, delete if exists
            try:
                buffer = resource.read_buffer_by_time(buffer.device_id, model_data.id, buffer.timestamp)
                resource.delete_buffer(buffer.id)
                print("BUFFER ALREADY EXISTS")
            except grpc.RpcError as error:
                print(error)
