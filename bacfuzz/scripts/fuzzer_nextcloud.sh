#!/bin/bash

timestamp=$(date +%s)
project_name="nextcloud"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

## Running WUT
PORT=8084               
TIMEOUT=5              
HOST="localhost"
TARGET_URL="http://${HOST}:${PORT}/" 

./running_WUT.sh $project_name $HOST $PORT $TARGET_URL

echo "RUNNING THE FUZZER - DRIVER PHASE"
cd $SCRIPT_DIR
source ../venv/bin/activate
cd ../fuzzer
python fuzzer.py --hour 0 --minute 5 --url $TARGET_URL --name ${project_name} --only-driver y --roles Admin User Editor Viewer Anonymous 2>&1 | tee ../"${project_name}-DRI-$(hostname)-${timestamp}.log"

echo "DELETE THE WUT"
cd $SCRIPT_DIR
cd "../../WUT/${project_name}"
docker compose down
sleep 20s

echo "RUNNING AGAIN THE WUT"
cd $SCRIPT_DIR
./running_WUT.sh $project_name $HOST $PORT $TARGET_URL

echo "RUNNING THE FUZZER - CHECKER PHASE"
cd $SCRIPT_DIR
source ../venv/bin/activate
cd ../fuzzer
NODE_OPTIONS="--max-old-space-size=8192" python fuzzer.py --hour 0 --minute 5 --url $TARGET_URL --name ${project_name} --only-checker y --roles Admin User Editor Viewer Anonymous --config ../configs/config-nextcloud.yaml 2>&1 | tee ../"${project_name}-CHECK-$(hostname)-${timestamp}.log"

echo "COLLECTING SYSTEM STATISTICS"
cd $SCRIPT_DIR
./system_stat.sh | tee ../stats/"${project_name}-${timestamp}.txt"

echo "DELETE THE WUT"
cd $SCRIPT_DIR
cd "../../WUT/${project_name}"
docker compose down
sleep 20s

echo "FUZZING COMPLETED FOR NEXTCLOUD"

## USER CREDENTIALS:
## admin: admin123
## testuser: testuser123.  
## editor: editor1234.
## viewer: viewer123.