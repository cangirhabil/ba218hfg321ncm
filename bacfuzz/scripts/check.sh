# !/bin/bash

server="localhost"
if nc -z $server 8098 2>/dev/null; then
    echo "$server ✓"
else
    echo "$server ✗"
fi

find ./my_dir -amin +10 -type f -delete
find . -amin +10 -type f -delete

grep -o -i ",200," 151_137.csv | wc -l
grep -o -i ",500," app_phpBB-201_1848.csv | wc -l

#https://www.simplified.guide/apache/log-post
docker logs app_wordpress-web-wordpress-1 --follow 2>&1 | tee wp.log

java -jar -Xmx8G zap-2.16.0.jar

