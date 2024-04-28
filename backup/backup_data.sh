#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONF_FILE="${SCRIPT_DIR}/config.sh"
source $CONF_FILE

EPOCH=$(date +%s)
END_SEC=$((EPOCH - (EPOCH % BACKUP_PERIOD)))
BEGIN_SEC=$((END_SEC - BACKUP_PERIOD))
END=$(date +'%Y-%m-%d %H:%M:%S %z' -d "@$END_SEC")
BEGIN=$(date +'%Y-%m-%d %H:%M:%S %z' -d "@$BEGIN_SEC")
echo $BEGIN
echo $END

COLUMNS="\"device_id\",\"model_id\",\"timestamp\",\"data\""
if [ $BACKUP_TABLE = "data_buffer" ]; then
	COLUMNS="\"device_id\",\"model_id\",\"timestamp\",\"data\",\"status\""
fi
QUERY="SELECT $COLUMNS FROM \"$BACKUP_TABLE\" WHERE \"timestamp\" >= '$BEGIN' AND \"timestamp\" < '$END'"

FILTER_FLAG=0
if [[ $GROUP_MODEL =~ [[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12} ]]; then
	FILTER_FLAG=1
	COL_ID=model_id
	TB_GROUP=group_model
	TB_MAP=group_model_map
fi
if [[ $GROUP_DEVICE =~ [[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12} ]]; then
	FILTER_FLAG=1
	COL_ID=device_id
	TB_GROUP=group_device
	TB_MAP=group_device_map
fi
if [[ FILTER_FLAG -eq 1 ]]; then
	RESULT=($(psql $DB_URL -AXqtc "SELECT \"${COL_ID}\" FROM \"${TB_GROUP}\" INNER JOIN \"${TB_MAP}\" USING (\"group_id\");"))
	if [[ ${#RESULT[@]} -gt 0 ]]; then
		FILTER_ID="("
		for res in "${RESULT[@]}"; do FILTER_ID+="'${res}',"; done
		FILTER_ID="${FILTER_ID:0:$((${#FILTER_ID}-1))})"
		QUERY+=" AND \"${COL_ID}\" IN ${FILTER_ID}"
	fi
fi
echo $QUERY

PREFIX="data"
if [ $BACKUP_TABLE = "data_buffer" ]; then
	PREFIX="buffer"
fi
BACKUP_PATH+="/$PREFIX"
mkdir -p $BACKUP_PATH

psql $DB_URL -c "\copy ($QUERY) to '${BACKUP_PATH}/${PREFIX}_${BEGIN_SEC}.csv' with (format csv, header true);"
