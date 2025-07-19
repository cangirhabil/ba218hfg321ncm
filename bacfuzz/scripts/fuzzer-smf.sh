#!/bin/bash

timestamp=$(date +%s)
project_name="app_smf"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

## Running WUT
PORT=8084               
TIMEOUT=5              
HOST="localhost"
TARGET_URL="http://${HOST}:${PORT}/" 

./running_WUT.sh $project_name $HOST $PORT $TARGET_URL

echo "RUNNING THE FUZZER"
cd $SCRIPT_DIR
source ../venv/bin/activate
cd ../fuzzer
python fuzzer.py --hour 24 --minute 0 --url $TARGET_URL --name ${project_name} --only-driver y --roles Admin StandardUser Anonymous |& tee ../"${project_name}-DRI-$(hostname)-${timestamp}.log"

echo "DELETE THE WUT"
cd $SCRIPT_DIR
cd "../../WUT/${project_name}"
docker compose down
sleep 20s

cd $SCRIPT_DIR
./running_WUT.sh $project_name $HOST $PORT $TARGET_URL

cd $SCRIPT_DIR
cd ../fuzzer
NODE_OPTIONS="--max-old-space-size=8192" python fuzzer.py --hour 24 --minute 0 --url $TARGET_URL --name ${project_name} --only-checker y --ignored-sql log --roles Admin StandardUser Anonymous |& tee ../"${project_name}-CHECK-$(hostname)-${timestamp}.log"

cd $SCRIPT_DIR
./system_stat.sh | tee ../stats/"${project_name}-${timestamp}.txt"

echo "DELETE THE WUT"
cd $SCRIPT_DIR
cd "../../WUT/${project_name}"
docker compose down
sleep 20s


## USER LIST: admin admin123
## USER LIST: standard_user user123

## CVE Attack Surface: GET http://localhost:8084/index.php?action=profile;u=2;area=showalerts;do=remove;aid=
## CVE Proof: DELETE FROM smf_user_alerts\n\t\tWHERE id_alert 
