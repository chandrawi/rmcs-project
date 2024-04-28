#!/bin/bash

# load variables from configuration file
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONF_FILE="${SCRIPT_DIR}/config.sh"
source $CONF_FILE

sleep $INITIAL_SLEEP

while :
do

	# run data logger scripts listed on configuration file
	for i in "${!LOGGER_SCRIPTS[@]}"; do
		if [[ ${LOGGER_SCRIPTS[$i]:0:1} = "/" ]]; then

			# append gateway ID as command argument
			SCRIPT_PATH="${BASE_PATH}${LOGGER_SCRIPTS[$i]}"
			SCRIPT_COMMAND=$SCRIPT_PATH
			regex='[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}$'
			if [[ ${LOGGER_SCRIPTS[$i+1]} =~ $regex ]]; then
				SCRIPT_COMMAND+=" ${LOGGER_SCRIPTS[$i+1]}"
			fi

			logger=$(pgrep -a python | grep -c $SCRIPT_PATH)
			if [ $logger -eq 0 ]
			then

				printf "rerun data logger script...\n"
				sudo $PYTHON_PATH $SCRIPT_COMMAND &

			fi
		fi
	done

	sleep $CHECK_DURATION_LOGGER

done
