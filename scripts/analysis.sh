#!/bin/bash

sleep 15

while :
do

	analysis_sin=$(pgrep -a python | grep -c /opt/rmcs-project/analysis/lews/analysis_soil_inclinometer.py)
	if [ $analysis_sin -eq 0 ]
	then

		printf "rerun soil inclinometer analysis script...\n"
		sudo /opt/rmcs-project/.venv/bin/python /opt/rmcs-project/analysis/lews/analysis_soil_inclinometer.py &

	fi

	analysis_pie=$(pgrep -a python | grep -c /opt/rmcs-project/analysis/lews/analysis_piezometer.py)
	if [ $analysis_pie -eq 0 ]
	then

		printf "rerun piezometer analysis script...\n"
		sudo /opt/rmcs-project/.venv/bin/python /opt/rmcs-project/analysis/lews/analysis_piezometer.py &

	fi

	analysis_rag=$(pgrep -a python | grep -c /opt/rmcs-project/analysis/lews/analysis_rain_gauge.py)
	if [ $analysis_rag -eq 0 ]
	then

		printf "rerun rain gauge analysis script...\n"
		sudo /opt/rmcs-project/.venv/bin/python /opt/rmcs-project/analysis/lews/analysis_rain_gauge.py &

	fi

	analysis_rhd=$(pgrep -a python | grep -c /opt/rmcs-project/analysis/clem/analysis_running_hour_data.py)
	if [ $analysis_rhd -eq 0 ]
	then

		printf "rerun running hour data analysis script...\n"
		/opt/rmcs-project/.venv/bin/python /opt/rmcs-project/analysis/clem/analysis_running_hour_data.py &

	fi

	analysis_twpa=$(pgrep -a python | grep -c /opt/rmcs-project/analysis/clem/timing_working_parameter_analysis.py)
	if [ $analysis_twpa -eq 0 ]
	then

		printf "rerun timing working parameter analysis script...\n"
		/opt/rmcs-project/.venv/bin/python /opt/rmcs-project/analysis/clem/timing_working_parameter_analysis.py &

	fi

	analysis_rhs=$(pgrep -a python | grep -c /opt/rmcs-project/analysis/clem/analysis_running_hour_sensor.py)
	if [ $analysis_rhs -eq 0 ]
	then

		printf "rerun running hour sensor analysis script...\n"
		/opt/rmcs-project/.venv/bin/python /opt/rmcs-project/analysis/clem/analysis_running_hour_sensor.py &

	fi

	sleep 5

done
