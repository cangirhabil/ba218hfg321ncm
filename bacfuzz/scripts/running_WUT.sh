#!/bin/bash

## ./running_WUT.sh <<project_name>> <<host>> <<port number>> <<target url>>

project_name=$1
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

## Running WUT
PORT=$3               
TIMEOUT=5              
HOST=$2
TARGET_URL=$4 

echo "RUNNING THE WUT"
cd $SCRIPT_DIR
cd ../../WUT/${project_name}
docker compose up --detach --force-recreate
while true; do
        if nc -z -w "$TIMEOUT" "$HOST" "$PORT"; then
            if command -v curl &> /dev/null; then
        	response=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET_URL" --max-time "$TIMEOUT")
        	if [ "$response" -eq "200" ]; then
            		echo "Service on $HOST:$PORT is fully ready."
            		break
            	elif  [ "$response" -eq "301" ] || [ "$response" -eq "302" ]; then
            		echo "Service on $HOST:$PORT is fully ready."
            		break
            	fi
            fi
        fi
        echo "server is NOT ready on port $PORT. Retrying in $RETRY_INTERVAL seconds..."
        sleep 5s
done

echo "server is READY on port $PORT"