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
		t) TAG_FILTER=${OPTARG};;
		r) REPLACE_TAG=${OPTARG};;
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
COLUMNS="\"device_id\",\"model_id\",\"timestamp\",\"tag\",\"data\""
COL_TS="\"timestamp\""
PREFIX="data"
if [[ $REPLACE_TAG =~ ^[0-9]+$ ]]; then
	COLUMNS="\"device_id\",\"model_id\",\"timestamp\",$REPLACE_TAG AS \"tag\",\"data\""
fi
QUERY="SELECT $COLUMNS FROM \"$BACKUP_TABLE\" WHERE \"timestamp\" >= '$BEGIN' AND \"timestamp\" < '$END'"
if [ $BACKUP_TABLE = "data_buffer" ]; then
	PREFIX="buffer"
elif [ $BACKUP_TABLE = "data_slice" ]; then
	COLUMNS="\"device_id\",\"model_id\",\"timestamp_begin\",\"timestamp_end\",\"name\",\"description\""
	COL_TS="\"timestamp_begin\""
	QUERY="SELECT $COLUMNS FROM \"$BACKUP_TABLE\" WHERE \"timestamp_begin\" >= '$BEGIN' AND \"timestamp_end\" <= '$END'"
	PREFIX="slice"
fi

# get variables to construct a query if device or model group id match uuid pattern
MODEL_IDS=""
DEVICE_IDS=""
SUFFIX=""
regex='[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}$'
if [[ $GROUP_MODEL =~ $regex ]]; then
	SUFFIX+="_M_$GROUP_MODEL"
	# run a select query to get list of devices or models
	RESULT=($(psql $DB_URL -AXqtc "SELECT \"model_id\" FROM \"group_model\" INNER JOIN \"group_model_map\" USING (\"group_id\") WHERE \"group_id\"='${GROUP_MODEL}';"))
	# construct where clause query with array of devices or models
	if [[ ${#RESULT[@]} -gt 0 ]]; then
		for res in "${RESULT[@]}"; do MODEL_IDS+="'${res}',"; done
		MODEL_IDS="${MODEL_IDS:0:$((${#MODEL_IDS}-1))}"
		QUERY+=" AND \"model_id\" IN (${MODEL_IDS})"
	fi
fi
if [[ $GROUP_DEVICE =~ $regex ]]; then
	SUFFIX+="_D_$GROUP_DEVICE"
	# run a select query to get list of devices or models
	RESULT=($(psql $DB_URL -AXqtc "SELECT \"device_id\" FROM \"group_device\" INNER JOIN \"group_device_map\" USING (\"group_id\") WHERE \"group_id\"='${GROUP_DEVICE}';"))
	# construct where clause query with array of devices or models
	if [[ ${#RESULT[@]} -gt 0 ]]; then
		for res in "${RESULT[@]}"; do DEVICE_IDS+="'${res}',"; done
		DEVICE_IDS="${DEVICE_IDS:0:$((${#DEVICE_IDS}-1))}"
		QUERY+=" AND \"device_id\" IN (${DEVICE_IDS})"
	fi
fi

# add tag filter to query
TAGS=""
if [[ $TAG_FILTER =~ ^[0-9]+$ && $BACKUP_TABLE != "data_slice" ]]; then
	TAGS="$TAG_FILTER"
	if [[ -n "$MODEL_IDS" ]]; then
		RESULT=($(psql $DB_URL -AXqtc "SELECT \"members\" FROM \"model_tag\" WHERE \"model_id\" IN (${MODEL_IDS}) AND \"tag\"=${TAG_FILTER};"))
		if [[ ${#RESULT[@]} -gt 0 ]]; then
			for res in "${RESULT[@]}"; do
				hex="${res#\\x}"
				for ((i=0; i<${#hex}; i+=2)); do part="${hex:i:2}"; TAGS+=",$((16#$part))"; done
			done
		fi
	fi
	QUERY+=" AND \"tag\" IN (${TAGS})"
fi
QUERY+=" ORDER BY $COL_TS ASC"

# create backup directory and prepare backup file output path
BACKUP_DIRECTORY+="/$PREFIX"
mkdir -p $BACKUP_DIRECTORY
DATETIME=$(date +'%Y-%m-%d_%H-%M-%S_%z' -d "@$BEGIN_SEC")
BACKUP_PATH="${BACKUP_DIRECTORY}/${PREFIX}_${DATETIME}${SUFFIX}.csv"
echo $BACKUP_PATH

# run copy command to a csv file for select query result on data or data_buffer table
echo $QUERY
psql $DB_URL -c "\copy ($QUERY) to '$BACKUP_PATH' with (format csv, header true);"

# delete data after backup if delete flag is true
if [[ $DELETE_FLAG -eq 1 ]]; then
	QUERY="DELETE FROM \"$BACKUP_TABLE\" WHERE $COL_TS >= '$BEGIN' AND $COL_TS < '$END'"
	if [[ -n "$MODEL_IDS" ]]; then
		QUERY+=" AND \"model_id\" IN (${MODEL_IDS})"
	fi
	if [[ -n "$DEVICE_IDS" ]]; then
		QUERY+=" AND \"device_id\" IN (${DEVICE_IDS})"
	fi
	if [[ -n "$TAGS" ]]; then
		QUERY+=" AND \"tag\" IN (${TAGS})"
	fi
	echo $QUERY
	psql $DB_URL -c "$QUERY;"
fi
