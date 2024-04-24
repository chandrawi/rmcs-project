import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from dataclasses import dataclass
import time
from datetime import datetime
from uuid import UUID
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource
from pymodbus.client import ModbusSerialClient
import config


@dataclass
class DeviceMap:
    slave_id: int
    id: UUID
    model: UUID
    type: str

# create client object
client = ModbusSerialClient(config.GATEWAY_MODBUS['serial_port'], baudrate=9600)
# connect to device
client.connect()

# user login
address_auth = config.SERVER_LOCAL['address_auth']
address_resource = config.SERVER_LOCAL['address_resource']
auth = Auth(address_auth)
login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
resource = Resource(address_resource, login.access_tokens[0].access_token)

print("LOGIN:")
print("user_id       = {}".format(login.user_id))
print("auth_token    = {}".format(login.auth_token))
for token in login.access_tokens:
    print("api_id        = {}".format(token.api_id))
    print("access_token  = {}".format(token.access_token))
    print("refresh_token = {}".format(token.refresh_token))

# read devices associated with configured gateway
device_map: list[DeviceMap] = []
devices = resource.list_device_by_gateway(UUID(config.GATEWAY_MODBUS['id']))
for device in devices:
    if device.id != device.gateway_id: # filter out gateway
        slave_id = None
        for conf in device.configs:
            if conf.name == "slave_id":
                slave_id = conf.value
        for model_id in device.type.models:
            model = resource.read_model(model_id)
            if model.category == "RAW" and slave_id != None:
                device_map.append(DeviceMap(slave_id, device.id, model_id, device.type.name))
for device in device_map:
    print(device)

while True:

    if int(time.time()) % config.GATEWAY_MODBUS["period_time"] != 0:
        continue
    now = datetime.now().replace(microsecond=0)
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Get received data from node
    for device in device_map:
        client.connect()

        try:
            # Request data to the modbus device based on its type
            data = []
            if device.type == "soil inclinometer":
                rr = client.read_input_registers(slave=device.slave_id, address=0x00, count=3)
                data = rr.registers
            elif device.type == "piezometer":
                rr = client.read_input_registers(slave=device.slave_id, address=0x10, count=6)
                data = [rr.registers[0], rr.registers[1], rr.registers[3], rr.registers[4]]
            elif device.type == "rain gauge":
                rr = client.read_holding_registers(slave=device.slave_id, address=0x00, count=10)
                data = [rr.registers[2], rr.registers[0], rr.registers[5], rr.registers[4]]
            elif device.type == "environment sensor":
                rr = client.read_input_registers(slave=device.slave_id, address=0x00, count=3)
                data = rr.registers
            else:
                continue
            print("{0}    {1}  {2:3d}    {3}".format(now_str, device.id, device.slave_id, data))

            # Create buffer with data from request data
            resource.create_buffer(device.id, device.model, now, data, "ANALYSIS_1")

        except Exception as error:
            print(error)

        finally:
            client.close()

    while int(time.time()) % config.GATEWAY_MODBUS["period_time"] == 0:
        pass
