#!/bin/bash

sleep 15

while :
do

	logger_modbus=$(pgrep -a python | grep -c /opt/rmcs-project/data_logger/logger_modbus.py)
	if [ $logger_modbus -eq 0 ]
	then

		printf "rerun data logger script...\n"
		sudo /opt/rmcs-project/.venv/bin/python /opt/rmcs-project/data_logger/logger_modbus.py &

	fi

	logger_lora=$(pgrep -a python | grep -c /opt/rmcs-project/data_logger/logger_lora.py)
	if [ $logger_lora -eq 0 ]
	then

		printf "rerun data logger script...\n"
		sudo /opt/rmcs-project/.venv/bin/python /opt/rmcs-project/data_logger/logger_lora.py &

	fi

	sleep 5

done
