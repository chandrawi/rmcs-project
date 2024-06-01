import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import uuid
from rmcs_api_client.auth import Auth
from rmcs_api_client.resource import Resource, DataType
import config

from utility.model_device_lews import MODELS, TYPES, GATEWAY, DEVICES, GROUPS
# from utility.model_device_clem import MODELS, TYPES, GATEWAY, DEVICES, GROUPS


# admin login
address_auth = config.SERVER_LOCAL['address_auth']
address_resource = config.SERVER_LOCAL['address_resource']
auth = Auth(address_auth)
login = auth.user_login(config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password'])
resource = Resource(address_resource, login.access_tokens[0].access_token)

# create data model and add data types and configs
model_map = {}
for key, model in MODELS.items():
    model_id = resource.create_model(uuid.uuid4(), model.data_type, model.category, model.name, model.description)
    for index, configs in enumerate(model.configs):
        for conf in configs:
            resource.create_model_config(model_id, index, conf.name, conf.value, conf.category)
    model_map[key] = model_id

# create type
type_map = {}
for key, type_ in TYPES.items():
    type_id = resource.create_type(uuid.uuid4(), type_.name, type_.description)
    for model_key in type_.models:
        model_id = model_map[model_key]
        resource.add_type_model(type_id, model_id)
    type_map[key] = type_id

# create gateway
gateway_map = {}
gateway_id = uuid.uuid4()
type_id = type_map[GATEWAY.type]
resource.create_gateway(gateway_id, type_id, GATEWAY.serial_number, GATEWAY.name, GATEWAY.description)
for conf in GATEWAY.configs:
    resource.create_gateway_config(gateway_id, conf.name, conf.value, conf.category)
gateway_map[GATEWAY.serial_number] = gateway_id

# create devices
device_map = {}
for device in DEVICES:
    device_id = uuid.uuid4()
    type_id = type_map[device.type]
    resource.create_device(device_id, gateway_id, type_id, device.serial_number, device.name, device.description)
    for conf in device.configs:
        resource.create_device_config(device_id, conf.name, conf.value, conf.category)
    device_map[device.serial_number] = device_id

# create groups
group_map = {}
for group in GROUPS:
    group_id = uuid.uuid4()
    resource.create_group_device(group_id, group.name, group.category, group.description)
    for member in group.members:
        if member in device_map:
            resource.add_group_device_member(group_id, device_map[member])
    group_map[group.name] = group_id

print("LOGIN:")
print("user_id       = {}".format(login.user_id))
print("auth_token    = {}".format(login.auth_token))
for token in login.access_tokens:
    print("api_id        = {}".format(token.api_id))
    print("access_token  = {}".format(token.access_token))
    print("refresh_token = {}".format(token.refresh_token))
print("MODELS:")
for name in model_map:
    print("{}: {}".format(model_map[name], name))
print("TYPES:")
for name in type_map:
    print("{}: {}".format(type_map[name], name))
print("GATEWAY:")
for name in gateway_map:
    print("{}: {}".format(gateway_map[name], name))
print("DEVICES:")
for name in device_map:
    print("{}: {}".format(device_map[name], name))
print("GROUP:")
for name in group_map:
    print("{}: {}".format(group_map[name], name))
