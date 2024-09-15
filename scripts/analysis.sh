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

			# append group ID and buffer number and offset as command arguments
			SCRIPT_PATH="${BASE_PATH}${ANALYSIS_SCRIPTS[$i]}"
			SCRIPT_COMMAND=$SCRIPT_PATH
			regex='^[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}$'
			if [[ ${ANALYSIS_SCRIPTS[$i+1]} =~ $regex ]]; then
				SCRIPT_COMMAND+=" ${ANALYSIS_SCRIPTS[$i+1]}"
			fi
			regex='^[[:digit:]]+$'
			if [[ ${ANALYSIS_SCRIPTS[$i+1]} =~ $regex ]]; then
				SCRIPT_COMMAND+=" ${ANALYSIS_SCRIPTS[$i+1]}"
			fi
			if [[ ${ANALYSIS_SCRIPTS[$i+2]} =~ $regex ]]; then
				SCRIPT_COMMAND+=" ${ANALYSIS_SCRIPTS[$i+2]}"
			fi
			if [[ ${ANALYSIS_SCRIPTS[$i+3]} =~ $regex ]]; then
				SCRIPT_COMMAND+=" ${ANALYSIS_SCRIPTS[$i+3]}"
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

	sleep $CHECK_ANALYSIS_INTERVAL

done
