import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from rmcs_api_client.auth import Auth
import random
import uuid
from uuid import UUID
import config


PROCEDURES_ADMIN = [
    "read_model", "create_model", "update_model", "delete_model", "change_model_type",
    "read_model_config", "create_model_config", "update_model_config", "delete_model_config", 
    "read_device", "create_device", "update_device", "delete_device",
    "read_device_config", "create_device_config", "update_device_config", "delete_device_config", 
    "read_type", "create_type", "update_type", "delete_type", "change_type_model",
    "read_group", "create_group", "update_group", "delete_group", "change_group_member",
    "read_data", "get_data_model", "read_data_with_model", "create_data", "delete_data",
    "read_buffer", "create_buffer", "update_buffer", "delete_buffer",
    "read_slice", "create_slice", "update_slice", "delete_slice",
    "read_log", "create_log", "update_log", "delete_log"
]
PROCEDURES_USER = [
    "read_model", "read_model_config", "read_device", "read_device_config", "read_type", "read_group",
    "read_data", "read_buffer", "read_slice", "read_log"
]
PROCEDURES = set(PROCEDURES_ADMIN + PROCEDURES_USER)
USER_ADMIN = [config.SERVER_LOCAL['admin_name'], config.SERVER_LOCAL['admin_password']]
USER_USER = [config.SERVER_LOCAL['user_name'], config.SERVER_LOCAL['user_password']]
ROLES = {
    "admin": [PROCEDURES_ADMIN, USER_ADMIN, False, True, 2147483647, 2147483647],
    "user": [PROCEDURES_USER, USER_USER, True, False, 2147483647, 2147483647]
}


# root login
address_auth = config.SERVER_LOCAL['address_auth']
auth = Auth(address_auth)
login = auth.user_login("root", config.SERVER_LOCAL['root_password'])
auth = Auth(address_auth, login.auth_token)

# create API and procedures
api_id = auth.create_api(
    id=UUID(config.API['id']),
    name=config.API['name'],
    address=address_auth,
    category=config.API['category'],
    description="",
    password=config.API['password'],
    access_key=random.randbytes(32)
)
proc_map = {}
for proc_name in PROCEDURES:
    proc_id = auth.create_procedure(uuid.uuid4(), api_id, proc_name, "")
    proc_map[proc_name] = proc_id

# create roles and link it to procedures
role_map = {}
for role in ROLES:
    role_id = auth.create_role(
        id=uuid.uuid4(),
        api_id=api_id,
        name=role,
        multi=ROLES[role][2],
        ip_lock=ROLES[role][3],
        access_duration=ROLES[role][4],
        refresh_duration=ROLES[role][5]
    )
    role_map[role] = role_id
    for proc_name in ROLES[role][0]:
        auth.add_role_access(role_id, proc_map[proc_name])

# create users and link it to a role
user_map = {}
for role in ROLES:
    user_id = auth.create_user(
        id=uuid.uuid4(),
        name=ROLES[role][1][0],
        email="",
        phone="",
        password=ROLES[role][1][1]
    )
    auth.add_user_role(user_id, role_map[role])
    user_map[ROLES[role][1][0]] = [user_id, role]

print("API_ID:")
print(api_id)
print("PROCEDURES:")
for name in proc_map:
    print("{}: {}".format(proc_map[name], name))
print("ROLES:")
for name in role_map:
    print("{}: {}".format(role_map[name], name))
print("USERS:")
for name in user_map:
    print("{}: {}, {}".format(user_map[name][0], name, user_map[name][1]))
