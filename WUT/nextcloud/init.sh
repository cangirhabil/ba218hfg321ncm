#!/bin/bash

# NextCloud Auto-Setup Init Script
# This script runs automatically via the shared entrypoint.sh

set -e

echo "=== NextCloud Auto-Setup Starting ==="

# Wait for database to be ready
echo "Waiting for database..."
while ! mysqladmin ping -h"db" --silent; do
    echo "Waiting for db"
    sleep 2
done
echo "✓ Database is ready!"

# Wait for Redis to be ready
echo "Waiting for Redis..."
until redis-cli -h redis -a redis123 ping 2>/dev/null | grep -q "PONG"; do
    echo "Waiting for Redis..."
    sleep 2
done
echo "✓ Redis is ready!"

# Check if NextCloud is already installed
if [ -f /var/www/html/config/config.php ]; then
    echo "NextCloud already installed, checking users..."
    
    cd /var/www/html
    
    # Check if setup flag exists
    SETUP_FLAG="/var/www/html/data/.setup_completed"
    if [ -f "$SETUP_FLAG" ]; then
        echo "✓ Setup already completed, skipping user creation."
        exit 0
    fi
else
    echo "Installing NextCloud..."
    
    # Install NextCloud
    cd /var/www/html
    sudo -u www-data php occ maintenance:install \
        --database "mysql" \
        --database-name "nextcloud" \
        --database-user "nextcloud" \
        --database-pass "nextcloud123" \
        --database-host "db" \
        --admin-user "admin" \
        --admin-pass "admin123"
    
    # Configure Redis
    sudo -u www-data php occ config:system:set redis host --value="redis"
    sudo -u www-data php occ config:system:set redis port --value="6379"
    sudo -u www-data php occ config:system:set redis password --value="redis123"
    sudo -u www-data php occ config:system:set memcache.locking --value="\OC\Memcache\Redis"
    sudo -u www-data php occ config:system:set memcache.distributed --value="\OC\Memcache\Redis"
    
    # Set trusted domains
    sudo -u www-data php occ config:system:set trusted_domains 0 --value="localhost"
    sudo -u www-data php occ config:system:set trusted_domains 1 --value="127.0.0.1"
    
    echo "✓ NextCloud installed successfully!"
fi

# Function: Create user
create_user() {
    local username=$1
    local password=$2
    local displayname=$3
    
    echo "  → Creating user $username..."
    
    # Check if user already exists
    if sudo -u www-data php occ user:list | grep -q "^  - $username:"; then
        echo "    $username already exists, skipping..."
        return 0
    fi
    
    # Create new user
    echo "$password" | sudo -u www-data sh -c "export OC_PASS=\$(cat) && php occ user:add --password-from-env --display-name='$displayname' $username"
    
    if [ $? -eq 0 ]; then
        echo "    ✓ $username created successfully"
    else
        echo "    ✗ Failed to create $username"
        return 1
    fi
}

# Create test users
echo "Creating test users..."
create_user "testuser" "TestUser2024!" "Test User"
create_user "editor" "EditorPass2024!" "Editor User"
create_user "viewer" "ViewerPass2024!" "Viewer User"

# Create groups
echo "Creating groups..."
sudo -u www-data php occ group:add editors 2>/dev/null || echo "  editors group already exists"
sudo -u www-data php occ group:add viewers 2>/dev/null || echo "  viewers group already exists"
sudo -u www-data php occ group:add admins 2>/dev/null || echo "  admins group already exists"
sudo -u www-data php occ group:add users 2>/dev/null || echo "  admins group already exists"

# Add users to groups
echo "Adding users to groups..."
sudo -u www-data php occ group:adduser editors editor 2>/dev/null || true
sudo -u www-data php occ group:adduser viewers viewer 2>/dev/null || true
sudo -u www-data php occ group:adduser users testuser 2>/dev/null || true

echo "Creating test files..."

# Create test files in admin directory
mkdir -p /var/www/html/data/admin/files/test_files

# Create test files
cat > /var/www/html/data/admin/files/test_files/admin_secret.txt << 'EOF'
This is admin's secret file - only admin should access this!
EOF

cat > /var/www/html/data/admin/files/test_files/shared_file.txt << 'EOF'
This is a shared file that can be accessed by multiple users
EOF

cat > /var/www/html/data/admin/files/test_files/public_document.txt << 'EOF'
This is a public document available to all users
EOF

cat > /var/www/html/data/admin/files/test_files/confidential.txt << 'EOF'
CONFIDENTIAL: This file contains sensitive information
EOF

# Fix file ownership
chown -R www-data:www-data /var/www/html/data/admin/files/test_files

# Scan files
echo "Scanning files..."
sudo -u www-data php occ files:scan admin

# Mark setup as completed
SETUP_FLAG="/var/www/html/data/.setup_completed"
touch "$SETUP_FLAG"

echo ""
echo "=== AUTO-SETUP COMPLETED! ==="
echo ""
echo "📋 Created Test Users:"
echo "   👤 admin       : admin123        (Administrator)"
echo "   👤 testuser    : TestUser2024!   (Regular user)"
echo "   👤 editor      : EditorPass2024! (Editor group member)"
echo "   👤 viewer      : ViewerPass2024! (Viewer group member)"
echo ""
echo "📁 Groups Created:"
echo "   👥 editors"
echo "   👥 viewers"
echo "   👥 admins"
echo "   👥 users"
echo ""
echo "📄 Test Files Created:"
echo "   - admin_secret.txt"
echo "   - shared_file.txt"
echo "   - public_document.txt"
echo "   - confidential.txt"
echo ""
echo "🌐 NextCloud URL: http://localhost:8084"
echo "✅ Setup completed automatically!"
echo ""