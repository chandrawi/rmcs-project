import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import time
from datetime import date, datetime, timedelta, timezone
from uuid import UUID
import grpc
import psycopg
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource, ModelSchema, DeviceSchema
import config


# Shift period in seconds and offset from 00:00:00 in seconds
DAY_IN_SEC = 86400
SHIFT_PERIOD = 43200
SHIFT_OFFSET = 21600

def getDateShift(timestamp: datetime) -> tuple[date, int]:
    t = timestamp.timestamp() - time.timezone - SHIFT_OFFSET
    dt = datetime.fromtimestamp(t, timezone.utc)
    if (t % DAY_IN_SEC) < SHIFT_PERIOD:
        return (dt.date(), 1)
    else:
        return (dt.date(), 2)

def execute(query, params):
    with psycopg.connect(config.DATABASE['url_external']) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)

def fetchone(query, params):
    with psycopg.connect(config.DATABASE['url_external']) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()

def create_running_hour_data(
        equipment_id: UUID, 
        timestamp: datetime, 
        active_energy: float, 
        apparent_energy: float, 
        frequency: float, 
        peak_current: float, 
        peak_voltage: float, 
        status: int
    ):
    query = """
        INSERT INTO running_hour_data (equipment_id, timestamp, active_energy, apparent_energy, frequency, peak_current, peak_voltage, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
    params = (equipment_id, timestamp, active_energy, apparent_energy, frequency, peak_current, peak_voltage, status)
    execute(query, params)

def create_running_hour_sensor(
        equipment_id: UUID, 
        date: date, 
        shift: int, 
        time_begin: datetime, 
        time_end: datetime,
        index: int
    ):
    query = """
        INSERT INTO running_hour_sensor (equipment_id, date, shift, time_begin, time_end, index) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """
    params = (equipment_id, date, shift, time_begin, time_end, index)
    execute(query, params)

def read_running_hour_data(
        equipment_id: UUID, 
        timestamp: datetime
    ):
    query = """
        SELECT equipment_id, timestamp
        FROM running_hour_data
        WHERE equipment_id=%s AND timestamp=%s;
        """
    params = (equipment_id, timestamp)
    return fetchone(query, params)

def read_running_hour_sensor(
        equipment_id: UUID, 
        time_begin: datetime, 
        time_end: datetime, 
    ):
    query = """
        SELECT equipment_id, timestamp
        FROM running_hour_sensor
        WHERE equipment_id=%s AND time_begin=%s AND time_end=%s;
        """
    params = (equipment_id, time_begin, time_end)
    return fetchone(query, params)

def transfer_external_server(model: ModelSchema, equipment_id: UUID, timestamp: datetime, data: list):
    if model.name == "running hour basic data":
        create_running_hour_data(equipment_id, timestamp, data[0], data[1], data[2], data[3], data[4], data[5])
    elif model.name == "running hour sensor":
        date, shift = getDateShift(timestamp)
        time_end = timestamp + timedelta(seconds=data[1])
        create_running_hour_sensor(equipment_id, date, shift, timestamp, time_end, data[0])
    else:
        print("Model is not recognized")

def check_external_server(model: ModelSchema, equipment_id: UUID, timestamp: datetime, data: list = []) -> bool:
    if model.name == "running hour basic data":
        if read_running_hour_data(equipment_id, timestamp) != None: return True
    elif model.name == "running hour sensor":
        time_end = timestamp + timedelta(seconds=data[0])
        if read_running_hour_sensor(equipment_id, timestamp, time_end) != None: return True
    return False


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
    print("{}: {}".format(device.id, device.name))
    device_map[device.id] = device.name


while True:

    # read buffers
    buffers = []
    try:
        buffers = resource.list_buffer_first(100, None, None, "EXTERNAL_OUTPUT")
    except grpc.RpcError as error:
        if error.code() == grpc.StatusCode.UNAUTHENTICATED:
            login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
            resource = Resource(address_resource, login.access_tokens[0].access_token)
            print("RELOGIN LOCAL")
        continue

    # create data from buffer
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

        # try to transfer data to external database
        external_exist = True
        transfer_next = False
        try:
            if buffer.model_id in model_map:
                transfer_next = transfer_external_server(model_map[buffer.model_id], buffer.device_id, buffer.timestamp, buffer.data)
        except Exception as error:
            print(error)
            # check if data on external server already exist
            try:
                external_exist = check_external_server(model_map[buffer.model_id], buffer.device_id, buffer.timestamp)
            except Exception as error:
                external_exist = False
                print(error)

        # delete or update status based on configuration only if data on external server exists
        if external_exist:
            try:
                if transfer_next:
                    resource.update_buffer(buffer.id, None, 23)
                else:
                    resource.delete_buffer(buffer.id)
            except grpc.RpcError as error:
                print(error)

    time.sleep(config.TIMING['transfer_sleep'])
