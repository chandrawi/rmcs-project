DATABASE = {
    "url_auth" : "postgres://postgres:password@127.0.0.1:5432/test_rmcs_auth",
    "url_resource" : "postgres://postgres:password@127.0.0.1:5432/test_rmcs_resource",
    "url_external": "postgres://postgres:password@127.0.0.1:5432/defaultdb"
}

SERVER_LOCAL = {
    "address_auth": "127.0.0.1:9001",
    "address_resource": "127.0.0.1:9002",
    "root_password": "r0ot_P4s5w0rd",
    "admin_name": "administrator",
    "admin_password": "Adm1n_P4s5w0rd",
    "user_name": "gundala",
    "user_password": "Us3r_P4s5w0rd"
}

SERVER_MAIN = {
    "address_auth": "api.gundala.co.id:9001",
    "address_resource": "api.gundala.co.id:9002",
    "admin_name": "administrator",
    "admin_password": "Adm1n_P4s5w0rd",
}

API = {
    "id": "00000000-0000-0000-0000-000000000000",
    "name": "clem",
    "category": "resource",
    "password": "Ap1_P4s5w0rd"
}

GATEWAY_MODBUS = {
    "00000000-0000-0000-0000-000000000000": {
        "period_time": 60,
        "serial_port": "/dev/ttyS0"
    }
}

GATEWAY_LORA = {
    "00000000-0000-0000-0000-000000000000": {
        "spi": (3, 0),
        "cs": (4, 6),
        "reset": (4,1),
        "busy": (4, 3),
        "frequency": 915000000,
        "sf": 8,
        "bw": 125000,
        "cr": 5
    }
}

GATEWAYS = []
for k in GATEWAY_MODBUS: GATEWAYS.append(k)
for k in GATEWAY_LORA: GATEWAYS.append(k)

TIMING = {
    "transfer_sleep": 1,
    "analysis_sleep": 1,
    "max_drift": 0.5
}

STATUS = {
    "logger_modbus_end": "ANALYSIS_1",
    "logger_lora_end": "ANALYSIS_1",
    "transfer_local_raw": "DELETE",
    "transfer_local_end": "TRANSFER_SERVER",
    "transfer_server_end": "DELETE",
    "transfer_external_db_begin": "EXTERNAL_OUTPUT",
    "transfer_external_db_end": "DELETE",
    "transfer_external_db_next": 23,
    "transfer_external_api_begin": 23,
    "transfer_external_api_end": "DELETE"
}

EXTERNAL_API = {
    "token": "CUNeYi2wBCFKtsC4CbVbiOnoeYY89yKC",
    "url": "http://batubara.koneksi.cloud:8080/api/v1/report-start-finish"
}
