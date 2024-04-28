import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import time
from datetime import datetime
from uuid import UUID
import psycopg
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource, ModelSchema, DeviceSchema
import config


def execute(query, params):
    with psycopg.connect(config.DATABASE['url_external']) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)

def fetchone(query, params):
    with psycopg.connect(config.DATABASE['url_external']) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()

def create_soil_inclinometer(
        device_id: UUID, 
        timestamp: datetime, 
        acceleration_x: float, 
        acceleration_y: float, 
        acceleration_z: float, 
        angle_x: float, 
        angle_z: float, 
        displacement_x: float, 
        displacement_z: float
    ):
    query = """
        INSERT INTO data_soil_inclinometer (id, timestamp, acceleration_x, acceleration_y, acceleration_z, angle_x, angle_z, displacement_x, displacement_z) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    params = (device_id, timestamp, acceleration_x, acceleration_y, acceleration_z, angle_x, angle_z, displacement_x, displacement_z)
    execute(query, params)

def read_soil_inclinometer(
        device_id: UUID, 
        timestamp: datetime
    ):
    query = """
        SELECT id, timestamp, acceleration_x, acceleration_y, acceleration_z, angle_x, angle_z, displacement_x, displacement_z
        FROM data_soil_inclinometer
        WHERE id=%s AND timestamp=%s;
        """
    params = (device_id, timestamp)
    return fetchone(query, params)

def create_piezometer(
        device_id: UUID, 
        timestamp: datetime, 
        pressure: float, 
        depth: float
    ):
    query = """
        INSERT INTO data_piezometer (id, timestamp, pressure, depth) 
        VALUES (%s, %s, %s, %s);
        """
    params = (device_id, timestamp, pressure, depth)
    execute(query, params)

def read_piezometer(
        device_id: UUID, 
        timestamp: datetime
    ):
    query = """
        SELECT id, timestamp, pressure, depth
        FROM data_piezometer
        WHERE id=%s AND timestamp=%s;
        """
    params = (device_id, timestamp)
    return fetchone(query, params)

def create_rain_gauge(
        device_id: UUID, 
        timestamp: datetime, 
        rain_yesterday: float, 
        rain_today: float, 
        rain_last_hour: float, 
        rain_hourly: float
    ):
    query = """
        INSERT INTO data_rain_gauge (id, timestamp, rain_yesterday, rain_today, rain_last_hour, rain_hourly) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """
    params = (device_id, timestamp, rain_yesterday, rain_today, rain_last_hour, rain_hourly)
    execute(query, params)

def read_rain_gauge(
        device_id: UUID, 
        timestamp: datetime
    ):
    query = """
        SELECT id, timestamp, rain_yesterday, rain_today, rain_last_hour, rain_hourly
        FROM data_rain_gauge
        WHERE id=%s AND timestamp=%s;
        """
    params = (device_id, timestamp)
    return fetchone(query, params)

def create_environment_sensor(
        device_id: UUID, 
        timestamp: datetime, 
        temperature: float, 
        humidity: float, 
        pressure: float
    ):
    query = """
        INSERT INTO data_environment_sensor (id, timestamp, temperature, humidity, pressure) 
        VALUES (%s, %s, %s, %s, %s);
        """
    params = (device_id, timestamp, temperature, humidity, pressure)
    execute(query, params)

def read_environment_sensor(
        device_id: UUID, 
        timestamp: datetime
    ):
    query = """
        SELECT id, timestamp, temperature, humidity, pressure
        FROM data_environment_sensor
        WHERE id=%s AND timestamp=%s;
        """
    params = (device_id, timestamp)
    return fetchone(query, params)

def transfer_external_server(model: ModelSchema, device_id: UUID, timestamp: datetime, data: list):
    if model.name == "XZ-axis soil inclinometer":
        return create_soil_inclinometer(device_id, timestamp, data[0], data[1], data[2], data[3], data[4], data[5], data[6])
    elif model.name == "piezometer data":
        return create_piezometer(device_id, timestamp, data[0], data[1])
    elif model.name == "rain gauge data":
        return create_rain_gauge(device_id, timestamp, data[0], data[1], data[2], data[3])
    elif model.name == "environment sensor data":
        return create_environment_sensor(device_id, timestamp, data[0], data[1], data[2])

def check_external_server(model: ModelSchema, device_id: UUID, timestamp: datetime):
    if model.name == "XZ-axis soil inclinometer":
        if read_soil_inclinometer(device_id, timestamp) != None: return True
    elif model.name == "piezometer data":
        if read_piezometer(device_id, timestamp) != None: return True
    elif model.name == "rain gauge data":
        if read_rain_gauge(device_id, timestamp) != None: return True
    elif model.name == "environment sensor data":
        if read_environment_sensor(device_id, timestamp) != None: return True
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
models_raw = resource.list_model_by_category("RAW")
models_data = resource.list_model_by_category("DATA")
model_data_map: dict[UUID, ModelSchema] = {}
model_raw_map: dict[UUID, ModelSchema] = {}
print("RAW MODEL")
for model in models_raw:
    model_raw_map[model.id] = model
    print("{}: {}".format(model.id, model.name))
print("DATA MODEL")
for model in models_data:
    model_data_map[model.id] = model
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
    buffers = resource.list_buffer_first(10, None, None, config.STATUS['transfer_external_db_begin'])

    # create data from buffer
    for buffer in buffers:

        # check if a buffer has associated device
        try:
            time_str = buffer.timestamp.strftime("%Y-%m-%d %H:%M:%S %z")
            if buffer.device_id not in device_map:
                resource.delete_buffer(buffer.id)
                continue
            if buffer.model_id in model_data_map:
                print("{}    {}    DATA   {}".format(time_str, buffer.device_id, device_map[buffer.device_id]))
            else:
                print("{}    {}    RAW    {}".format(time_str, buffer.device_id, device_map[buffer.device_id]))
        except Exception as error:
            print(error)

        # try to transfer data to external database only for buffer data
        external_exist = False
        try:
            if buffer.model_id in model_data_map:
                transfer_external_server(model_data_map[buffer.model_id], buffer.device_id, buffer.timestamp, buffer.data)
                external_exist = True
        except Exception as error:
            print(error)
            # check if data on external server already exist
            try:
                external_exist = check_external_server(model_data_map[buffer.model_id], buffer.device_id, buffer.timestamp)
            except Exception as error:
                print(error)

        # delete buffer only if data on local and data on external server exists
        if external_exist:
            try:
                if config.STATUS['transfer_external_db_end'] == "DELETE":
                    resource.delete_buffer(buffer.id)
                else:
                    resource.update_buffer(buffer.id, None, config.STATUS['transfer_external_db_end'])
            except Exception as error:
                print(error)

    time.sleep(config.TIMING['transfer_sleep'])
