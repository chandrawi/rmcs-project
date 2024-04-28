#!/bin/bash

# load variables from configuration file
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONF_FILE="${SCRIPT_DIR}/config.sh"
source $CONF_FILE

sleep $INITIAL_SLEEP

while :
do

	# run analysis scripts listed on configuration file
	for i in "${!ANALYSIS_SCRIPTS[@]}"; do
		if [[ ${ANALYSIS_SCRIPTS[$i]:0:1} = "/" ]]; then

			SCRIPT_COMMAND="${BASE_PATH}${ANALYSIS_SCRIPTS[$i]}"

			logger=$(pgrep -a python | grep -c $SCRIPT_COMMAND)
			if [ $logger -eq 0 ]
			then

				printf "rerun transfer script...\n"
				sudo $PYTHON_PATH $SCRIPT_COMMAND &

			fi
		fi
	done

	sleep $CHECK_DURATION_LOGGER

done
