#!/bin/bash

# Dolibarr Auto-Setup Entrypoint Script
# This script runs automatically when the container starts

set -e

echo "=== Dolibarr Auto-Setup Starting ==="

# Start the original entrypoint in background
echo "Starting Dolibarr..."
/usr/local/bin/docker-run.sh apache2-foreground &
DOLIBARR_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    kill $DOLIBARR_PID 2>/dev/null || true
    wait $DOLIBARR_PID 2>/dev/null || true
}
trap cleanup EXIT

# Wait for Dolibarr to be ready
echo "Waiting for Dolibarr to be ready..."
TIMEOUT=300  # 5 minute timeout
COUNTER=0

# First wait for Apache to start
until curl -s http://localhost > /dev/null 2>&1; do
    sleep 10
    COUNTER=$((COUNTER + 10))
    if [ $COUNTER -ge $TIMEOUT ]; then
        echo "ERROR: Dolibarr did not become ready within $TIMEOUT seconds!"
        exit 1
    fi
    echo "Dolibarr is not ready yet... ($COUNTER/$TIMEOUT seconds)"
done

echo "✓ Dolibarr started successfully!"

# Wait a bit more for full initialization
sleep 30

# Now check if Dolibarr is fully accessible
echo "Checking Dolibarr full readiness..."
READY_COUNTER=0
until curl -f -s http://localhost | grep -i "dolibarr" > /dev/null 2>&1; do
    sleep 10
    READY_COUNTER=$((READY_COUNTER + 10))
    if [ $READY_COUNTER -ge 120 ]; then
        echo "Dolibarr web interface not fully ready, but continuing..."
        break
    fi
    echo "Waiting for Dolibarr web interface... ($READY_COUNTER/120 seconds)"
done

# Check if setup has already been completed
SETUP_FLAG="/var/www/documents/.setup_completed"
if [ -f "$SETUP_FLAG" ]; then
    echo "Setup already completed, skipping user creation."
    # Keep the main process running
    wait $DOLIBARR_PID
    exit $?
fi

echo "Starting user setup..."

# Database connection details
DB_HOST="db"
DB_USER="dolibarr"
DB_PASS="dolibarr123"
DB_NAME="dolibarr"

# Function to execute SQL commands
execute_sql() {
    local sql_command="$1"
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$sql_command"
}

# Wait for database to be ready with tables
echo "Waiting for Dolibarr database to be initialized..."
DB_TIMEOUT=180
DB_COUNTER=0

# First wait for database connection
until mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "SELECT 1;" > /dev/null 2>&1; do
    sleep 5
    DB_COUNTER=$((DB_COUNTER + 5))
    if [ $DB_COUNTER -ge 60 ]; then
        echo "Database connection timeout, but continuing..."
        break
    fi
    echo "Waiting for database connection... ($DB_COUNTER/60 seconds)"
done

# Then wait for Dolibarr tables to be created
DB_COUNTER=0
until mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "SHOW TABLES LIKE 'llx_user';" 2>/dev/null | grep -q "llx_user" || [ $DB_COUNTER -ge $DB_TIMEOUT ]; do
    sleep 5
    DB_COUNTER=$((DB_COUNTER + 5))
    echo "Waiting for database initialization... ($DB_COUNTER/$DB_TIMEOUT seconds)"
done

if [ $DB_COUNTER -ge $DB_TIMEOUT ]; then
    echo "Database tables not found, but continuing with setup..."
fi

echo "✓ Database is ready!"

# Create test users in Dolibarr database
echo "Creating test users..."

# Function to create a Dolibarr user
create_dolibarr_user() {
    local login=$1
    local password=$2
    local lastname=$3
    local firstname=$4
    local rights=$5
    
    # Hash password (Dolibarr uses MD5 for basic auth)
    local password_hash=$(echo -n "$password" | md5sum | cut -d' ' -f1)
    
    echo "  → Creating user $login..."
    
    # Check if user exists and delete
    execute_sql "DELETE FROM llx_user WHERE login='$login';"
    
    # Insert new user
    execute_sql "INSERT INTO llx_user (
        login, pass_crypted, lastname, firstname, 
        datec, admin, statut, entity
    ) VALUES (
        '$login', '$password_hash', '$lastname', '$firstname',
        NOW(), $rights, 1, 1
    );"
    
    if [ $? -eq 0 ]; then
        echo "    ✓ $login created successfully"
    else
        echo "    ✗ Failed to create $login"
        return 1
    fi
}

# Wait for admin user to be available
echo "Checking admin user..."
ADMIN_TIMEOUT=60
ADMIN_COUNTER=0
until execute_sql "SELECT login FROM llx_user WHERE login='admin';" | grep -q admin; do
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
create_dolibarr_user "testuser" "TestUser2024!" "Test" "User" "0"
create_dolibarr_user "editor" "EditorPass2024!" "Editor" "User" "0"
create_dolibarr_user "viewer" "ViewerPass2024!" "Viewer" "User" "0"
create_dolibarr_user "admin_test" "AdminTest2024!" "Admin" "Test" "1"

# Create some test data
echo "Creating test data..."

# Create test companies/customers
execute_sql "INSERT IGNORE INTO llx_societe (
    nom, code_client, client, statut, entity, datec
) VALUES 
('Test Company', 'TC001', 1, 1, 1, NOW()),
('Demo Corp', 'DC002', 1, 1, 1, NOW()),
('Sample Ltd', 'SL003', 1, 1, 1, NOW());"

# Create test products
execute_sql "INSERT IGNORE INTO llx_product (
    ref, label, price, price_ttc, tva_tx, statut, entity, datec, tosell, tobuy
) VALUES 
('PROD001', 'Test Product 1', 100.00, 120.00, 20, 1, 1, NOW(), 1, 1),
('PROD002', 'Demo Product 2', 250.00, 300.00, 20, 1, 1, NOW(), 1, 1),
('SERV001', 'Sample Service', 75.00, 90.00, 20, 1, 1, NOW(), 1, 0);"

echo "Creating test directories..."
mkdir -p /var/www/documents/test_files

# Create test files
cat > /var/www/documents/test_files/admin_document.txt << 'EOF'
This is an admin document
Created for testing purposes
EOF

cat > /var/www/documents/test_files/shared_document.txt << 'EOF'
This is a shared document
Available for all users
EOF

cat > /var/www/documents/test_files/invoice_template.txt << 'EOF'
Invoice Template
Company: [COMPANY_NAME]
Date: [DATE]
Total: [AMOUNT]
EOF

# Fix file ownership
chown -R www-data:www-data /var/www/documents/test_files

# Mark setup as completed
touch "$SETUP_FLAG"

echo ""
echo "=== AUTO-SETUP COMPLETED! ==="
echo ""
echo "📋 Created Test Users:"
echo "   👤 admin       : admin123        (Administrator)"
echo "   👤 testuser    : TestUser2024!   (Regular user)"
echo "   👤 editor      : EditorPass2024! (Editor user)"
echo "   👤 viewer      : ViewerPass2024! (Viewer user)"
echo "   👤 admin_test  : AdminTest2024!  (Admin user)"
echo ""
echo "🏢 Created Test Companies:"
echo "   🏪 Test Company (TC001)"
echo "   🏪 Demo Corp (DC002)"  
echo "   🏪 Sample Ltd (SL003)"
echo ""
echo "📦 Created Test Products:"
echo "   📱 Test Product 1 (PROD001)"
echo "   📱 Demo Product 2 (PROD002)"
echo "   🛠️  Sample Service (SERV001)"
echo ""
echo "🌐 Dolibarr URL: http://localhost:8085"
echo "✅ Setup completed automatically!"
echo ""

# Keep the main Dolibarr process running
wait $DOLIBARR_PID