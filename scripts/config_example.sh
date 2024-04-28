#!/bin/bash

BASE_PATH=/opt/rmcs-project
PYTHON_PATH="$BASE_PATH/.venv/bin/python"

INITIAL_SLEEP=15
CHECK_DURATION_LOGGER=5
CHECK_DURATION_ANALYSIS=5
CHECK_DURATION_TRANSFER=5

LOGGER_SCRIPTS=(
	/data_logger/logger_modbus.py 00000000-0000-0000-0000-000000000000
)

ANALYSIS_SCRIPTS=(
)

TRANSFER_SCRIPTS=(
	/transfer/transfer_local.py
)