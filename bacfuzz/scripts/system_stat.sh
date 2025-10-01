#!/bin/bash

# Memory Usage
echo "=== Memory Usage ==="
free -h | grep -v + | grep -v Swap

# Detailed Memory Info (optional)
echo -e "\n=== Detailed Memory Info ==="
cat /proc/meminfo | grep -E 'MemTotal|MemFree|MemAvailable|Buffers|Cached'

# CPU Usage
echo -e "\n=== CPU Usage ==="
top -bn1 | grep "Cpu(s)" | \
    sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | \
    awk '{print 100 - $1"%"}'

# Per-core CPU Usage (optional)
echo -e "\n=== Per-Core CPU Usage ==="
mpstat -P ALL 1 1 | grep -v "Average"

# Top Processes by CPU
echo -e "\n=== Top 5 Processes by CPU Usage ==="
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 6

# Top Processes by Memory
echo -e "\n=== Top 5 Processes by Memory Usage ==="
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head -n 6

## WUT File Statistics
if [ -f /var/tmp/p312304/Phuzz_WUT/shared-tmpfs/php_loc_report.txt ]; then
	echo -e "\n=== WUT File Statistics ==="
	cat /var/tmp/p312304/Phuzz_WUT/shared-tmpfs/php_loc_report.txt
fi
