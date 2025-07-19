#!/bin/bash

# Usage: ./loc_counter.sh [directory] [output_file]
# If no directory is given, defaults to /var/www/html
# If no output file is given, defaults to /shared-tmpfs/php_loc_report.txt

TARGET_DIR="${1:-/var/www/html}"
OUTPUT_FILE="${2:-/shared-tmpfs/php_loc_report.txt}"
#OUTPUT_FILE="/shared-tmpfs/php_loc_report.txt"

# Handle case where input is explicitly an empty string
if [ -z "$1" ]; then
    TARGET_DIR="/var/www/html"
fi

if [ -z "$2" ]; then
    OUTPUT_FILE="/shared-tmpfs/php_loc_report.txt"
fi

echo "Scanning all files under: $TARGET_DIR"
echo "Analyzing content to determine language..."

echo "Multi-language LOC Report" > "$OUTPUT_FILE"
echo "Directory scanned: $TARGET_DIR" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

declare -A LANG_COUNTS

# Count total number of files
TOTAL_FILES=$(find "$TARGET_DIR" -type f | wc -l)
echo "Total number of files: $TOTAL_FILES" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Function to count lines excluding blank lines and comment lines
count_loc() {
    local file="$1"
    local lang="$2"
    local count

    count=$(grep -vE '^\s*$' "$file" | \
            grep -vE '^\s*//|^\s*/\*|^\s*\*|^\s*\*/' | \
            wc -l)

    LANG_COUNTS[$lang]=$((LANG_COUNTS[$lang] + count))
}

# Traverse all readable files
while IFS= read -r -d '' file; do
    # Only process text files
    if file "$file" | grep -qE 'ASCII text|UTF-8 text'; then
        # Detect language by content
        if grep -q "<?php" "$file"; then
            count_loc "$file" "PHP"
        elif grep -q "<script" "$file"; then
            count_loc "$file" "JavaScript"
        elif grep -q "<style" "$file"; then
            count_loc "$file" "CSS"
        elif grep -q "<html" "$file"; then
            count_loc "$file" "HTML"
        fi
    fi
done < <(find "$TARGET_DIR" -type f -readable -print0)

# Output LOC per language
TOTAL_LOC=0
for lang in "${!LANG_COUNTS[@]}"; do
    echo "Total $lang LOC (excluding blanks/comments): ${LANG_COUNTS[$lang]}" >> "$OUTPUT_FILE"
    TOTAL_LOC=$((TOTAL_LOC + LANG_COUNTS[$lang]))
done

echo "" >> "$OUTPUT_FILE"
echo "Grand Total LOC: $TOTAL_LOC" >> "$OUTPUT_FILE"

echo "Report saved to $OUTPUT_FILE"
