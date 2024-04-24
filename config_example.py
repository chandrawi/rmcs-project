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

GATEWAYS = [
    "00000000-0000-0000-0000-000000000000"
]

TIMING = {
    "transfer_sleep": 1,
    "analysis_sleep": 1,
    "max_drift": 0.5
}
