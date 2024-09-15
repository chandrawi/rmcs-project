#!/bin/bash

# load variables from configuration file
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONF_FILE="${SCRIPT_DIR}/config.sh"
source $CONF_FILE

sleep $INITIAL_SLEEP

# turn on modem for the first time
sudo gpioset --mode=exit $MODEM_KEY_GPIO_CHIP $MODEM_KEY_GPIO_OFFSET=1

sleep $CHECK_INTERNET_CONNECTION_INTERVAL

while :
do

	# check connection to 1.1.1.1 (cloudflare) and main server
	# get number of successful ping
	CHECK_CF=$(ping -c 10 1.1.1.1 | egrep packet | cut -d" " -f4)
	CHECK_MS=$(ping -c 10 $SERVER_ADDRESS | egrep packet | cut -d" " -f4)

	# reset modem by turn off for 5 seconds
	DATE=$(date +"%Y-%m-%d %H:%M:%S")
	if [ $CHECK_CF -eq 0 ] && [ $CHECK_MS -eq 0 ]; then
		echo "$DATE    Reset modem..."
		sudo gpioset --mode=time --sec=5 $MODEM_KEY_GPIO_CHIP $MODEM_KEY_GPIO_OFFSET=0
		sudo gpioset --mode=exit $MODEM_KEY_GPIO_CHIP $MODEM_KEY_GPIO_OFFSET=1
	else
		echo "$DATE    Connected to internet"
	fi

	sleep $CHECK_INTERNET_CONNECTION_INTERVAL

done
