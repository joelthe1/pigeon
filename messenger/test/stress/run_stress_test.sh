#!/bin/bash
########################################################################################
# NEEDS SUDO PRIVILEGES
#
# Stress test for Pigeon messenger.
# Uses `nping` which is sub-program of `nmap`.
# For installing on Mac try: `brew install nmap`
#
# This script takes no. of requests to be sent as
# argument and reports the time it took as well as
# the number of meesages received by Pigeon and the
# difference/mismatch, if any.
# 
# e.g. usage:
# % bash stress.sh 12000
# 
########################################################################################
echo "Starting Pigeon stress test"

COUNT=$1
UDP_HOST=127.0.0.1
UDP_PORT=9089
SLEEP=3
PIGEON_HOME=/Users/fox/dev/workspace/ased/pigeon

# Truncate output.log file
cat /dev/null > "$PIGEON_HOME/output.log"

# Blast UDP messages
sudo nping --data-string="Stress test message" --rate=$COUNT --count=$COUNT -H -N --udp --dest-port $UDP_PORT $UDP_HOST

sleep $SLEEP
echo
echo -n "> Received by Pigeon:"
cat $PIGEON_HOME/output.log | wc -l
echo
