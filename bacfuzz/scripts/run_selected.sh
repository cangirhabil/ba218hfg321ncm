#!/bin/bash

# User-provided list of script names (without .sh extension)
# Example: "script1 script2 script3"
scripts_to_run="dvwa xvwa CVE_2025_0843 CVE_2025_3537 CVE_2024_55232 CVE_2024_40480 CVE_2025_0802 CVE_2023_46449 CVE_2024_3139 CVE_2024_9082 CVE_2024_7658"
# scripts_to_run="CVE_2024_3139 CVE_2024_9082 CVE_2024_7658"

# Convert to array
IFS=' ' read -r -a script_array <<< "$scripts_to_run"

# Loop through each script
for script_base in "${script_array[@]}"; do
    script="fuzzer-${script_base}.sh"
    if [[ -f "$script" && -x "$script" ]]; then
        echo "Running: $script"
        ./"$script"
    else
        echo "Skipping: $script (not found or not executable)"
    fi
done
