#!/bin/bash

sleep 15

while :
do

	transfer_local=$(pgrep -a python | grep -c /home/gundala/rmcs-server/transfer/transfer_local.py)
	if [ $transfer_local -eq 0 ]
	then

		printf "rerun transfer local script...\n"
		/home/gundala/rmcs-server/.venv/bin/python /home/gundala/rmcs-server/transfer/transfer_local.py &

	fi

	transfer_first=$(pgrep -a python | grep -c /opt/rmcs-project/transfer/transfer_server_first.py)
	if [ $transfer_first -eq 0 ]
	then

		printf "rerun transfer server first script...\n"
		/opt/rmcs-project/.venv/bin/python /opt/rmcs-project/transfer/transfer_server_first.py &

	fi

	transfer_last=$(pgrep -a python | grep -c /opt/rmcs-project/transfer/transfer_server_last.py)
	if [ $transfer_last -eq 0 ]
	then

		printf "rerun transfer server last script...\n"
		/opt/rmcs-project/.venv/bin/python /opt/rmcs-project/transfer/transfer_server_last.py &

	fi

	transfer_ext_db=$(pgrep -a python | grep -c /home/gundala/rmcs-server/transfer/clem/transfer_external_db.py)
	if [ $transfer_ext_db -eq 0 ]
	then

		printf "rerun transfer external database script...\n"
		/home/gundala/rmcs-server/.venv/bin/python /home/gundala/rmcs-server/transfer/clem/transfer_external_db.py &

	fi

	transfer_ext_api=$(pgrep -a python | grep -c /home/gundala/rmcs-server/transfer/clem/transfer_external_api.py)
	if [ $transfer_ext_api -eq 0 ]
	then

		printf "rerun transfer external api script...\n"
		/home/gundala/rmcs-server/.venv/bin/python /home/gundala/rmcs-server/transfer/clem/transfer_external_api.py &

	fi

	sleep 5

done
