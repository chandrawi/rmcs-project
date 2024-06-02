#!/bin/bash

# load variables from configuration file
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONF_FILE="${SCRIPT_DIR}/config.sh"
source $CONF_FILE

# get variables from argument to replace configuration variables
while getopts u:p:b:e:t:d:D:M:a:r:X flag
do
	case "${flag}" in
		u) DB_URL=${OPTARG};;
		p) INPUT_PERIOD=${OPTARG};;
		b) INPUT_BEGIN=${OPTARG};;
		e) INPUT_END=${OPTARG};;
		t) BACKUP_TABLE=${OPTARG};;
		d) BACKUP_DIRECTORY=${OPTARG};;
		D) GROUP_DEVICE=${OPTARG};;
		M) GROUP_MODEL=${OPTARG};;
		a) ADD_STATUS=${OPTARG};;
		r) REPLACE_STATUS=${OPTARG};;
		X) DELETE_FLAG=1;;
	esac
done

# get period from argument if exists
if [[ $INPUT_PERIOD =~ ^[0-9]+$ ]]; then
	BACKUP_PERIOD=$INPUT_PERIOD
fi
# calculate begin and end datetime based on period
TZ=$(date +%z)
OFFSET=$((0 ${TZ:0:1} (${TZ:1:2} * 3600 + ${TZ:3:2} * 60)))
EPOCH=$(($(date +%s) + OFFSET))
END_SEC=$((EPOCH - (EPOCH % BACKUP_PERIOD) - OFFSET))
BEGIN_SEC=$((END_SEC - BACKUP_PERIOD))
# get begin and end datetime from arguments if meet the format
regex='[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}([-+][0-9]{4})?$'
if [[ $INPUT_BEGIN =~ $regex && $INPUT_END =~ $regex ]]; then
	BEGIN_SEC=$(date -d$INPUT_BEGIN +%s)
	END_SEC=$(date -d$INPUT_END +%s)
fi
BEGIN=$(date +'%Y-%m-%dT%H:%M:%S%z' -d "@$BEGIN_SEC")
END=$(date +'%Y-%m-%dT%H:%M:%S%z' -d "@$END_SEC")

# construct select query with between begin and end datetime filter
COLUMNS="\"device_id\",\"model_id\",\"timestamp\",\"data\""
COL_TS="\"timestamp\""
PREFIX="data"
if [[ $ADD_STATUS =~ ^[0-9]+$ ]]; then
	COLUMNS="\"device_id\",\"model_id\",\"timestamp\",\"data\",$ADD_STATUS AS \"status\""
	PREFIX="buffer"
fi
if [ $BACKUP_TABLE = "data_buffer" ]; then
	COLUMNS="\"device_id\",\"model_id\",\"timestamp\",\"data\",\"status\""
	if [[ $REPLACE_STATUS =~ ^[0-9]+$ ]]; then
		COLUMNS="\"device_id\",\"model_id\",\"timestamp\",\"data\",$REPLACE_STATUS AS \"status\""
	fi
	PREFIX="buffer"
elif [ $BACKUP_TABLE = "data_slice" ]; then
	COLUMNS="\"device_id\",\"model_id\",\"timestamp_begin\",\"timestamp_end\",\"name\",\"description\""
	COL_TS="\"timestamp_begin\""
	PREFIX="slice"
fi
QUERY="SELECT $COLUMNS FROM \"$BACKUP_TABLE\" WHERE $COL_TS >= '$BEGIN' AND $COL_TS < '$END'"

# get variables to construct a query if device or model group id match uuid pattern
FILTER_FLAG=0
regex='[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}$'
if [[ $GROUP_MODEL =~ $regex ]]; then
	FILTER_FLAG=1
	COL_ID=model_id
	TB_GROUP=group_model
	TB_MAP=group_model_map
	SUFFIX=$GROUP_MODEL
fi
if [[ $GROUP_DEVICE =~ $regex ]]; then
	FILTER_FLAG=2
	COL_ID=device_id
	TB_GROUP=group_device
	TB_MAP=group_device_map
	SUFFIX=$GROUP_DEVICE
fi
# run a select query to get list of devices or models
if [[ FILTER_FLAG -gt 0 ]]; then
	RESULT=($(psql $DB_URL -AXqtc "SELECT \"${COL_ID}\" FROM \"${TB_GROUP}\" INNER JOIN \"${TB_MAP}\" USING (\"group_id\");"))
# construct where clause query with array of devices or models
	if [[ ${#RESULT[@]} -gt 0 ]]; then
		FILTER_ID="("
		for res in "${RESULT[@]}"; do FILTER_ID+="'${res}',"; done
		FILTER_ID="${FILTER_ID:0:$((${#FILTER_ID}-1))})"
		QUERY+=" AND \"${COL_ID}\" IN ${FILTER_ID}"
	fi
fi
QUERY+=" ORDER BY $COL_TS ASC"
echo $QUERY

# create backup directory and prepare backup file output path
BACKUP_DIRECTORY+="/$PREFIX"
mkdir -p $BACKUP_DIRECTORY
DATETIME=$(date +'%Y-%m-%d_%H-%M-%S_%z' -d "@$BEGIN_SEC")
BACKUP_PATH="${BACKUP_DIRECTORY}/${PREFIX}_${DATETIME}"
if [[ FILTER_FLAG -gt 0 ]]; then BACKUP_PATH+="_${SUFFIX}"; fi
BACKUP_PATH+=".csv"
echo $BACKUP_PATH

# run copy command to a csv file for select query result on data or data_buffer table
psql $DB_URL -c "\copy ($QUERY) to '$BACKUP_PATH' with (format csv, header true);"

# delete data after backup if delete flag is true
if [[ $DELETE_FLAG -eq 1 ]]; then
	QUERY="DELETE FROM \"$BACKUP_TABLE\" WHERE $COL_TS >= '$BEGIN' AND $COL_TS < '$END'"
	if [[ ${#RESULT[@]} -gt 0 ]]; then
		QUERY+=" AND \"${COL_ID}\" IN ${FILTER_ID}"
	fi
	psql $DB_URL -c "$QUERY"
fi
