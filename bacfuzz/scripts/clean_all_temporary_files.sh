#!/bin/bash

# List of folders to clean
FOLDERS=(
    "../data"
    "../log"
    "../result"
    "../screenshots"
)

# Loop through each folder
for FOLDER in "${FOLDERS[@]}"; do
    if [ -d "$FOLDER" ]; then
        echo "Cleaning contents of: $FOLDER"
        
        # Delete all files and subdirectories within the folder
        find "$FOLDER" -mindepth 1 -delete
    else
        echo "Warning: $FOLDER does not exist or is not a directory."
    fi
done

echo "Folder contents deleted."
