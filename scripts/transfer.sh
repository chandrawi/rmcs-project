#!/bin/bash

# load variables from configuration file
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONF_FILE="${SCRIPT_DIR}/config.sh"
source $CONF_FILE

sleep $INITIAL_SLEEP

while :
do

	# run transfer scripts listed on configuration file
	for i in "${!TRANSFER_SCRIPTS[@]}"; do
		if [[ ${TRANSFER_SCRIPTS[$i]:0:1} = "/" ]]; then

			# append buffer number and offset as command arguments
			SCRIPT_PATH="${BASE_PATH}${TRANSFER_SCRIPTS[$i]}"
			SCRIPT_COMMAND=$SCRIPT_PATH
			regex='^[[:digit:]]+$'
			if [[ ${TRANSFER_SCRIPTS[$i+1]} =~ $regex ]]; then
				SCRIPT_COMMAND+=" ${TRANSFER_SCRIPTS[$i+1]}"
			fi
			if [[ ${TRANSFER_SCRIPTS[$i+2]} =~ $regex ]]; then
				SCRIPT_COMMAND+=" ${TRANSFER_SCRIPTS[$i+2]}"
			fi

			number=$(pgrep -a python | grep -c "$SCRIPT_COMMAND")
			if [ $number -eq 0 ]
			then

				DATE=$(date +"%Y-%m-%d %H:%M:%S")
				echo "$DATE    rerun transfer script...\n"
				sudo $PYTHON_PATH $SCRIPT_COMMAND &

			fi
		fi
	done

	sleep $CHECK_TRANSFER_INTERVAL

done
