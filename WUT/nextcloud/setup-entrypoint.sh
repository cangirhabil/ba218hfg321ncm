#!/bin/bash

# Nextcloud Auto-Setup Entrypoint Script
# This script runs automatically when the container starts

set -e

echo "=== Nextcloud Auto-Setup Starting ==="

# Start the original entrypoint in background
echo "Starting Nextcloud..."
/entrypoint.sh apache2-foreground &
NEXTCLOUD_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    kill $NEXTCLOUD_PID 2>/dev/null || true
    wait $NEXTCLOUD_PID 2>/dev/null || true
}
trap cleanup EXIT

# Wait for Nextcloud to be ready
echo "Waiting for Nextcloud to be ready..."
TIMEOUT=300  # 5 minute timeout
COUNTER=0

until curl -f -s http://localhost/status.php > /dev/null 2>&1; do
    sleep 5
    COUNTER=$((COUNTER + 5))
    if [ $COUNTER -ge $TIMEOUT ]; then
        echo "ERROR: Nextcloud did not become ready within $TIMEOUT seconds!"
        exit 1
    fi
    echo "Nextcloud is not ready yet... ($COUNTER/$TIMEOUT seconds)"
done

echo "✓ Nextcloud started successfully!"

# Wait a bit more for full initialization
sleep 10

# Check if setup has already been completed
SETUP_FLAG="/var/www/html/data/.setup_completed"
if [ -f "$SETUP_FLAG" ]; then
    echo "Setup already completed, skipping user creation."
    # Keep the main process running
    wait $NEXTCLOUD_PID
    exit $?
fi

echo "Starting user setup..."

# Function: Create user
create_user() {
    local username=$1
    local password=$2
    local displayname=$3
    
    echo "  → Creating user $username..."
    
    # Check if user already exists
    if runuser -u www-data -- php occ user:list | grep -q "^  - $username:"; then
        echo "    $username already exists, deleting..."
        runuser -u www-data -- php occ user:delete $username 2>/dev/null || true
    fi
    
    # Create new user
    echo "$password" | runuser -u www-data -- sh -c "export OC_PASS=\$(cat) && php occ user:add --password-from-env --display-name='$displayname' $username"
    
    if [ $? -eq 0 ]; then
        echo "    ✓ $username created successfully"
    else
        echo "    ✗ Failed to create $username"
        return 1
    fi
}

# Change to nextcloud directory
cd /var/www/html

# Wait for admin user to be available
echo "Checking admin user..."
ADMIN_TIMEOUT=60
ADMIN_COUNTER=0
until runuser -u www-data -- php occ user:list | grep -q admin; do
    sleep 2
    ADMIN_COUNTER=$((ADMIN_COUNTER + 2))
    if [ $ADMIN_COUNTER -ge $ADMIN_TIMEOUT ]; then
        echo "ERROR: Admin user not found within timeout!"
        exit 1
    fi
    echo "Waiting for admin user... ($ADMIN_COUNTER/$ADMIN_TIMEOUT seconds)"
done

echo "✓ Admin user is ready!"

# Create test users
echo "Creating test users..."
create_user "testuser" "TestUser2024!" "Test User"
create_user "editor" "EditorPass2024!" "Editor User"
create_user "viewer" "ViewerPass2024!" "Viewer User"
create_user "admin_test" "AdminTest2024!" "Admin Test User"

# Create groups
echo "Creating groups..."
runuser -u www-data -- php occ group:add editors 2>/dev/null || echo "  editors group already exists"
runuser -u www-data -- php occ group:add viewers 2>/dev/null || echo "  viewers group already exists"
runuser -u www-data -- php occ group:add admins 2>/dev/null || echo "  admins group already exists"

# Add users to groups
echo "Adding users to groups..."
runuser -u www-data -- php occ group:adduser editors editor || true
runuser -u www-data -- php occ group:adduser viewers viewer || true
runuser -u www-data -- php occ group:adduser admin admin_test || true

echo "Creating test files..."

# Create test files in admin directory
mkdir -p /var/www/html/data/admin/files/test_files

# Create test files
cat > /var/www/html/data/admin/files/test_files/admin_secret.txt << 'EOF'
This is admin's secret file
EOF

cat > /var/www/html/data/admin/files/test_files/shared_file.txt << 'EOF'
This is a shared file
EOF

cat > /var/www/html/data/admin/files/test_files/testuser_file.txt << 'EOF'
This is testuser's file
EOF

cat > /var/www/html/data/admin/files/test_files/editor_file.txt << 'EOF'
This is editor's file
EOF

# Fix file ownership
chown -R www-data:www-data /var/www/html/data/admin/files/test_files

# Scan files
echo "Scanning files..."
runuser -u www-data -- php occ files:scan admin

# Mark setup as completed
touch "$SETUP_FLAG"

echo ""
echo "=== AUTO-SETUP COMPLETED! ==="
echo ""
echo "📋 Created Test Users:"
echo "   👤 admin       : admin123        (Administrator)"
echo "   👤 testuser    : TestUser2024!   (Regular user)"
echo "   👤 editor      : EditorPass2024! (Editor group member)"
echo "   👤 viewer      : ViewerPass2024! (Viewer user)"
echo "   👤 admin_test  : AdminTest2024!  (Admin group member)"
echo ""
echo "🌐 Nextcloud URL: http://localhost:8084"
echo "✅ Setup completed automatically!"
echo ""

# Keep the main Nextcloud process running
wait $NEXTCLOUD_PID