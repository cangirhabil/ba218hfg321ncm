#!/bin/bash

# Nextcloud Setup Script for BACFuzz Testing
# This script sets up users and configurations for testing

echo "Setting up Nextcloud for BACFuzz testing..."

# Wait for Nextcloud to be ready
echo "Waiting for Nextcloud to be ready..."
until curl -f http://localhost:8084/ > /dev/null 2>&1; do
    echo "Waiting for Nextcloud..."
    sleep 5
done

echo "Nextcloud is ready!"

# Use docker exec to create users via OCC commands
CONTAINER_NAME="nextcloud-app-1"

echo "Creating test users..."

# Create test users with different roles
docker exec -u www-data $CONTAINER_NAME php occ user:add --password-from-env testuser <<< "testuser123"
docker exec -u www-data $CONTAINER_NAME php occ user:add --password-from-env editor <<< "editor123"
docker exec -u www-data $CONTAINER_NAME php occ user:add --password-from-env viewer <<< "viewer123"

# Create groups
docker exec -u www-data $CONTAINER_NAME php occ group:add editors
docker exec -u www-data $CONTAINER_NAME php occ group:add viewers

# Add users to groups
docker exec -u www-data $CONTAINER_NAME php occ group:adduser editors editor
docker exec -u www-data $CONTAINER_NAME php occ group:adduser viewers viewer

echo "Setting up file shares for testing..."

# Create some test files and folders as admin
docker exec -u www-data $CONTAINER_NAME php occ files:scan admin

# Create test folders for different users
mkdir -p /tmp/nextcloud_test_files
echo "This is admin's secret file" > /tmp/nextcloud_test_files/admin_secret.txt
echo "This is a shared file" > /tmp/nextcloud_test_files/shared_file.txt
echo "This is testuser's file" > /tmp/nextcloud_test_files/testuser_file.txt

# Copy files to Nextcloud data directory
docker cp /tmp/nextcloud_test_files/admin_secret.txt $CONTAINER_NAME:/var/www/html/data/admin/files/
docker cp /tmp/nextcloud_test_files/shared_file.txt $CONTAINER_NAME:/var/www/html/data/admin/files/
docker cp /tmp/nextcloud_test_files/testuser_file.txt $CONTAINER_NAME:/var/www/html/data/admin/files/

# Scan files again
docker exec -u www-data $CONTAINER_NAME php occ files:scan admin

echo "Setup complete!"
echo ""
echo "Available users for testing:"
echo "- admin:admin123 (Administrator)"
echo "- testuser:testuser123 (Regular user)"
echo "- editor:editor123 (Editor group member)"
echo "- viewer:viewer123 (Viewer group member)"
echo ""
echo "Nextcloud is available at: http://localhost:8084"
echo ""
echo "You can now run the fuzzer with:"
echo "./fuzzer-nextcloud.sh"

# Clean up temporary files
rm -rf /tmp/nextcloud_test_files