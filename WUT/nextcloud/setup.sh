#!/bin/bash

# Nextcloud Installation and User Creation Script
# This script installs the project and adds users through the project interface

set -e  # Stop script on error

echo "=== Nextcloud Project Installation and User Setup ==="

# Stop and clean existing containers
echo "Cleaning existing containers..."
docker-compose down -v --remove-orphans 2>/dev/null || true

# Clean docker volumes
echo "Cleaning docker volumes..."
docker volume prune -f || true

# Start the project
echo "Starting Nextcloud project..."
docker-compose up -d

echo "Waiting for containers to start..."
sleep 30

# Wait for Nextcloud to be ready
echo "Waiting for Nextcloud to be ready..."
TIMEOUT=300  # 5 minute timeout
COUNTER=0

until curl -f -s http://localhost:8084/status.php > /dev/null 2>&1; do
    sleep 5
    COUNTER=$((COUNTER + 5))
    if [ $COUNTER -ge $TIMEOUT ]; then
        echo "ERROR: Nextcloud did not become ready within $TIMEOUT seconds!"
        exit 1
    fi
    echo "Nextcloud is not ready yet... ($COUNTER/$TIMEOUT seconds)"
done

echo "✓ Nextcloud started successfully!"

# Determine container name
CONTAINER_NAME="nextcloud-app-1"

# Check if container is running
if ! docker ps | grep -q $CONTAINER_NAME; then
    echo "ERROR: $CONTAINER_NAME container is not running!"
    docker-compose logs app
    exit 1
fi

echo "Container status checked: ✓"

# Complete Nextcloud installation
echo "Completing Nextcloud installation..."
sleep 10

# Check if admin user exists
echo "Checking admin user..."
if ! docker exec -u www-data $CONTAINER_NAME php occ user:list | grep -q admin; then
    echo "Admin user not found, manual installation may be required."
    echo "Please go to http://localhost:8084 and complete the installation."
    echo "Admin user credentials: admin / admin123"
    read -p "Press Enter after completing the installation..."
fi

echo "✓ Admin user is ready!"

# Create test users
echo "Creating test users..."

# Function: Create user
create_user() {
    local username=$1
    local password=$2
    local displayname=$3
    
    echo "  → Creating user $username..."
    
    # Check if user already exists
    if docker exec -u www-data $CONTAINER_NAME php occ user:list | grep -q "^  - $username:"; then
        echo "    $username already exists, deleting..."
        docker exec -u www-data $CONTAINER_NAME php occ user:delete $username 2>/dev/null || true
    fi
    
    # Create new user
    echo "$password" | docker exec -i -u www-data $CONTAINER_NAME sh -c "export OC_PASS=\$(cat) && php occ user:add --password-from-env --display-name='$displayname' $username"
    
    if [ $? -eq 0 ]; then
        echo "    ✓ $username created successfully"
    else
        echo "    ✗ Failed to create $username"
        return 1
    fi
}

# Create users
create_user "testuser" "TestUser2024!" "Test User"
create_user "editor" "EditorPass2024!" "Editor User"
create_user "viewer" "ViewerPass2024!" "Viewer User"
create_user "admin_test" "AdminTest2024!" "Admin Test User"

# Create groups
echo "Creating groups..."
docker exec -u www-data $CONTAINER_NAME php occ group:add editors 2>/dev/null || echo "  editors group already exists"
docker exec -u www-data $CONTAINER_NAME php occ group:add viewers 2>/dev/null || echo "  viewers group already exists"
docker exec -u www-data $CONTAINER_NAME php occ group:add admins 2>/dev/null || echo "  admins group already exists"

# Add users to groups
echo "Adding users to groups..."
docker exec -u www-data $CONTAINER_NAME php occ group:adduser editors editor
docker exec -u www-data $CONTAINER_NAME php occ group:adduser viewers viewer
docker exec -u www-data $CONTAINER_NAME php occ group:adduser admin admin_test

echo "Creating test files..."

# Create temp directory
mkdir -p /tmp/nextcloud_test_files

# Create test files
echo "This is admin's secret file" > /tmp/nextcloud_test_files/admin_secret.txt
echo "This is a shared file" > /tmp/nextcloud_test_files/shared_file.txt
echo "This is testuser's file" > /tmp/nextcloud_test_files/testuser_file.txt
echo "This is editor's file" > /tmp/nextcloud_test_files/editor_file.txt

# Copy files to admin directory
echo "Copying test files..."
docker exec $CONTAINER_NAME mkdir -p /var/www/html/data/admin/files/test_files
docker cp /tmp/nextcloud_test_files/. $CONTAINER_NAME:/var/www/html/data/admin/files/test_files/

# Fix file ownership
docker exec $CONTAINER_NAME chown -R www-data:www-data /var/www/html/data/admin/files/test_files

# Scan files
echo "Scanning files..."
docker exec -u www-data $CONTAINER_NAME php occ files:scan admin

# Clean up temp files
rm -rf /tmp/nextcloud_test_files

echo ""
echo "=== INSTALLATION COMPLETED! ==="
echo ""
echo "📋 Created Test Users:"
echo "   👤 admin       : admin123        (Administrator)"
echo "   👤 testuser    : TestUser2024!   (Regular user)"
echo "   👤 editor      : EditorPass2024! (Editor group member)"
echo "   👤 viewer      : ViewerPass2024! (Viewer group member)"
echo "   👤 admin_test  : AdminTest2024!  (Admin group member)"
echo ""
echo "🌐 Nextcloud URL: http://localhost:8084"
echo ""
echo "🔧 Available commands:"
echo "   • User list:        docker exec -u www-data nextcloud-app-1 php occ user:list"
echo "   • Group list:       docker exec -u www-data nextcloud-app-1 php occ group:list"
echo "   • Stop project:     docker-compose down"
echo "   • View logs:        docker-compose logs -f"
echo ""
echo "✨ To run the fuzzer: ./fuzzer-nextcloud.sh"