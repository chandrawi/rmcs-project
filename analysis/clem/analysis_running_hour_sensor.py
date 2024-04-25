import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from dataclasses import dataclass
import time
from datetime import datetime, timedelta
from uuid import UUID
import math
import grpc
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource
import config


# Running status enum value and running hour sensor analysis flag
RUNNING_STATUS = 2

@dataclass
class Device:
    serial_number: str
    period_time: int
    min_running_time: int
    max_interlude_time: int


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

# Get running hour basic data and sensor and working parameter command model
models = resource.list_model_by_name("running hour basic data")
model_data = models[0]
models = resource.list_model_by_name("running hour sensor")
model_sensor = models[0]
models = resource.list_model_by_name("working parameter command")
model_command = models[0]

# Get running hour devices
device_map: dict[UUID, Device] = {}
types = resource.list_type_by_name("running hour sensor")
type_id = types[0].id
devices = resource.list_device_by_type(type_id)
for device in devices:
    period = None
    min_rt = None
    max_it = None
    for conf in device.configs:
        if conf.name == "period_time":
            period = conf.value
        elif conf.name == "min_running_time":
            min_rt = conf.value
        elif conf.name == "max_interlude_time":
            max_it = conf.value
    # check for all necessary device config
    if period != None and min_rt != None and max_it != None:
        device_map[device.id] = Device(device.serial_number, period, min_rt, max_it)
if len(device_map) == 0:
    raise Exception("no device with specified type and config found")

print("RUNNING HOUR MODEL")
print("{}: {}".format(model_data.id, model_data.name))
print("{}: {}".format(model_sensor.id, model_sensor.name))
print("{}: {}".format(model_command.id, model_command.name))
print("DEVICES")
for id, device in device_map.items():
    print("{}: {}".format(id, device.serial_number))


while True:

    command = None
    try:
        # read buffer command with running hour sensor analysis status (ANALYSIS_2)
        command = resource.read_buffer_first(None, model_command.id, "ANALYSIS_2")
    except grpc.RpcError as error:
        if error.code() == grpc.StatusCode.UNAUTHENTICATED:
            login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
            resource = Resource(address_resource, login.access_tokens[0].access_token)
            print("RELOGIN LOCAL")
        # wait some moment when buffer is unavailable
        else:
            time.sleep(config.TIMING['analysis_sleep'])
        continue

    if command != None:

        # Get all running hour basic data of a device between begin and end working shift
        # device_ids = list(device_map.keys())
        shift_period = int(command.data[0])
        begin = command.timestamp
        end = begin + timedelta(seconds = shift_period)
        data_basic = resource.list_data_by_range_time(command.device_id, model_data.id, begin, end)
        data_status: dict[int, bool] = {}

        # Create data status map between delta time and status
        # True is running and False is standby or breakdown
        for data in data_basic:
            delta = data.timestamp - begin
            data_status[delta.seconds] = False
            if data.data[5] == RUNNING_STATUS:
                data_status[delta.seconds] = True

        # Filling empty data with False (standby or brekdown status)
        data_complete: dict[int, bool] = {}
        for i in range(0, shift_period + device.period_time, device.period_time):
            if i in data_status:
                data_complete[i] = data_status[i]
            else:
                data_complete[i] = False

        # Filter data with maximum interlude period
        # False data between True will be corrected to True
        data_filter: dict[int, bool] = {}
        for key in data_complete:
            data_filter[key] = data_complete[key]
            if not data_complete[key]:
                lowest = key - device.max_interlude_time
                if lowest < 0: lowest = 0
                highest = key + device.max_interlude_time
                if highest > shift_period: highest = shift_period
                low_check = False
                high_check = False
                for k in range(lowest, key, device.period_time):
                    if data_complete[k]:
                        low_check = True
                        break
                for k in range(highest, key, 0 - device.period_time):
                    if data_complete[k]:
                        high_check = True
                        break
                if low_check and high_check:
                    data_filter[key] = True

        # Transform data to list of running hour period
        running_periods: list[tuple[int]] = []
        start = 0
        stop = 0
        for key in data_filter:
            if data_filter[key]:
                stop = key
                if key == shift_period:
                    running_periods.append((start, stop))
            else:
                if stop - start > 0:
                    running_periods.append((start, stop))
                start = key

        # Filter data with minimum running period
        for i, running_period in enumerate(running_periods):
            if running_period[1] - running_period[0] < device.min_running_time:
                running_periods.pop(i)

        # for i in data_complete:
        #     original_status = None
        #     if i in data_status:
        #         original_status = data_status[i]
        #     print("{:8d}    {}\t{}\t{}".format(i, original_status, data_complete[i], data_filter[i]))

        print(command.device_id)
        print("CONFIGURATION:")
        print("    begin time      : {}".format(begin))
        print("    end time        : {}".format(end))
        print("    sampling period : {} s".format(device.period_time))
        print("    max interlude   : {} s".format(device.max_interlude_time))
        print("    min running     : {} s".format(device.min_running_time))
        print("RESULT:")
        if len(running_periods) == 0:
            print("    no running period detected")
        for running_period in running_periods:
            print("    start: {:4d}    stop: {:4d}".format(running_period[0], running_period[1]))

        # Create running hour buffer
        for index, running_period in enumerate(running_periods):
            timestamp = begin + timedelta(seconds=running_period[0])
            period = running_period[1] - running_period[0]
            time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            try:
                print("{}    {}    {}".format(time_str, command.device_id, period))
                resource.create_buffer(command.device_id, model_sensor.id, timestamp, [index, period], "TRANSFER_LOCAL")
            except grpc.RpcError as error:
                print(error)
                # check if buffer already exist, update if exists
                try:
                    buffer = resource.read_buffer_by_time(command.device_id, model_sensor.id, timestamp)
                    resource.update_buffer(buffer.id, [period], "TRANSFER_LOCAL")
                    print("BUFFER ALREADY EXISTS")
                except grpc.RpcError as error:
                    print(error)
                continue

        # Delete command
        try:
            print("{}    {}".format(command.timestamp, command.device_id))
            resource.delete_buffer(command.id)
        except grpc.RpcError as error:
            print(error)
