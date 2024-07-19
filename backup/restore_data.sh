#!/bin/bash

# load variables from configuration file
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONF_FILE="${SCRIPT_DIR}/config.sh"
source $CONF_FILE

# get variables from argument to replace configuration variables
while getopts t:d flag
do
	case "${flag}" in
		t) BACKUP_TABLE=${OPTARG};;
		d) BACKUP_DIRECTORY=${OPTARG};;
	esac
done

# get columns and backup directory
COLUMNS="\"device_id\",\"model_id\",\"timestamp\",\"data\""
PREFIX="data"
if [ $BACKUP_TABLE = "data_buffer" ]; then
	COLUMNS="\"device_id\",\"model_id\",\"timestamp\",\"data\",\"status\""
	PREFIX="buffer"
elif [ $BACKUP_TABLE = "data_slice" ]; then
	COLUMNS="\"device_id\",\"model_id\",\"timestamp_begin\",\"timestamp_end\",\"name\",\"description\""
	PREFIX="slice"
fi
BACKUP_DIRECTORY+="/$PREFIX"

# prepare restore commands for each files in backup directory
COMMANDS=()
for file in "$BACKUP_DIRECTORY"/*; do
	if [ -f "$file" ]; then
		COMMANDS+=("\copy \"$BACKUP_TABLE\"($COLUMNS) FROM '$file' DELIMITER ',' CSV HEADER;")
	fi
done

# restore data
for command in "${COMMANDS[@]}"; do
	psql $DB_URL -c "$command"
done
