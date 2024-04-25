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
from rmcs_api_client.resource import Resource
import config


# Period time contants
SHIFT_PERIOD = 43200
SHIFT_OFFSET = 21600
DAY_PERIOD = 86400
WEEK_PERIOD = 604800
MONTH_28_PERIOD = 2419200
MONTH_29_PERIOD = 2505600
MONTH_30_PERIOD = 2592000
MONTH_31_PERIOD = 2678400
QUARTER_1_PERIOD = 7776000
QUARTER_1_LEAP_PERIOD = 7862400
QUARTER_2_PERIOD = 7862400
QUARTER_3_PERIOD = 7948800
QUARTER_4_PERIOD = 7948800
YEAR_PERIOD = 31536000
YEAR_LEAP_PERIOD = 31622400

# Wait data complete time
WAIT_COMPLETE_TIME = 120

@dataclass
class Device:
    serial_number: str
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

# Get working parameter command model
models = resource.list_model_by_name("working parameter command")
model_command = models[0]

# Get running hour devices
device_map: dict[UUID, Device] = {}
types = resource.list_type_by_name("running hour sensor")
type_id = types[0].id
devices = resource.list_device_by_type(type_id)
for device in devices:
    min_rt = None
    max_it = None
    for conf in device.configs:
        if conf.name == "min_running_time":
            min_rt = conf.value
        elif conf.name == "max_interlude_time":
            max_it = conf.value
    # check for all necessary device config
    if min_rt != None and max_it != None:
        device_map[device.id] = Device(device.serial_number, min_rt, max_it)
if len(device_map) == 0:
    raise Exception("no device with specified type and config found")


while True:

    t = time.time() - time.timezone

    # Trigger running hour sensor analysis every end of shift plus wait complete time
    t_os = t - SHIFT_OFFSET
    if int(t_os % SHIFT_PERIOD) == WAIT_COMPLETE_TIME:

        # Calculate analysis begin time
        begin_t = t_os - (t_os % SHIFT_PERIOD) + SHIFT_OFFSET - SHIFT_PERIOD + time.timezone
        begin = datetime.fromtimestamp(begin_t)

        # Create command buffer for registered devices with running hour sensor status (ANALYSIS_2) and shift period as data
        for device_id in device_map:
            data = [SHIFT_PERIOD]
            print("{}    {}    {}".format(begin, device_id, data))
            try:
                resource.create_buffer(device_id, model_command.id, begin, data, "ANALYSIS_2")
            except grpc.RpcError as error:
                print(error)
                if error.code() == grpc.StatusCode.UNAUTHENTICATED:
                    login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
                    resource = Resource(address_resource, login.access_tokens[0].access_token)
                    print("RELOGIN LOCAL")
                    resource.create_buffer(device_id, model_command.id, begin, data)

    # wait some moment
    time.sleep(config.TIMING['analysis_sleep'])
