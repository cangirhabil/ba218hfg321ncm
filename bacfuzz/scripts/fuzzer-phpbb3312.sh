#!/bin/bash

timestamp=$(date +%s)
project_name="napp_phpBB3312"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

## Running WUT
PORT=8081               
TIMEOUT=5              
HOST="localhost"
TARGET_URL="http://${HOST}:${PORT}" 

./running_WUT.sh $project_name $HOST $PORT $TARGET_URL

echo "RUNNING THE FUZZER"
cd $SCRIPT_DIR
source ../venv/bin/activate
cd ../fuzzer
python fuzzer.py --hour 8 --minute 0 --url $TARGET_URL --name ${project_name} --only-driver y --roles Admin Member Anonymous |& tee ../"${project_name}-DRI-$(hostname)-${timestamp}.log"

echo "DELETE THE WUT"
cd $SCRIPT_DIR
cd "../../WUT/${project_name}"
docker compose down
sleep 20s

cd $SCRIPT_DIR
./running_WUT.sh $project_name $HOST $PORT $TARGET_URL

cd $SCRIPT_DIR
cd ../fuzzer
NODE_OPTIONS="--max-old-space-size=8192" python fuzzer.py --hour 24 --minute 0 --url $TARGET_URL --name ${project_name} --only-checker y --roles Admin Member Anonymous |& tee ../"${project_name}-CHECK-$(hostname)-${timestamp}.log"

echo "DELETE THE WUT"
cd $SCRIPT_DIR
cd "../../WUT/${project_name}"
docker compose down
sleep 20s

## USER LIST: admin admin123
## USER LIST: manager manager123
## USER LIST: author author123
## USER LIST: subscriber subscriber123
## USER LIST: customer customer123
