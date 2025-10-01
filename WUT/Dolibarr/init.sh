#!/bin/bash

# Dolibarr Auto-Setup Init Script
# This script runs automatically via shared entrypoint.sh and handles Dolibarr-specific setup

set -e

echo "🎯 Dolibarr AUTONOMOUS INSTALLATION SYSTEM - BacFuzz Ready"
echo "================================================="

# First, run the shared entrypoint setup tasks
echo "Running shared setup tasks..."
mkdir -p /shared-tmpfs/{branch_statements,coverage-reports,exception-reports,error-reports,mysql-error-reports,shell-error-reports,unserialize-error-reports,pathtraversal-error-reports,xxe-error-reports}
chmod -R 777 /shared-tmpfs/
chown -R www-data:www-data /var/www/ /shared-tmpfs/{branch_statements,coverage-reports,exception-reports,error-reports,mysql-error-reports,shell-error-reports,unserialize-error-reports,pathtraversal-error-reports,xxe-error-reports}

# Wait for database
if [ "${REQUIRES_DB:-0}" -gt 0 ]; then
    echo "Waiting for database..."
    while ! mysqladmin ping -h"db" --silent; do
        echo "Waiting for db"
        sleep 1
    done
    echo "✅ DB appears online!"
fi

# Run loc counter
if [ -f /loc_counter.sh ]; then
    echo "Counting the LoC..."
    /loc_counter.sh
fi

# Configure pcov
sed -e "s|pcov.directory=.*|pcov.directory=${FUZZER_COVERAGE_PATH}|" -i ${PHP_INI_DIR}/php.ini

# Start Apache in background
echo "🚀 Starting Apache web server..."
/usr/sbin/apache2ctl -D FOREGROUND &
APACHE_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    kill $APACHE_PID 2>/dev/null || true
    wait $APACHE_PID 2>/dev/null || true
}
trap cleanup EXIT

# Wait for web server to be ready
echo "🌐 Waiting for web server..."
TIMEOUT=120
COUNTER=0

until curl -f -s http://localhost/ > /dev/null 2>&1; do
    sleep 5
    COUNTER=$((COUNTER + 5))
    if [ $COUNTER -ge $TIMEOUT ]; then
        echo "❌ Web server was not ready within $TIMEOUT seconds!"
        exit 1
    fi
    echo "   Waiting for web server... ($COUNTER/$TIMEOUT seconds)"
done

echo "✅ Web server is ready!"

# Check if setup has already been completed
SETUP_FLAG="/var/www/documents/.setup_completed"
if [ -f "$SETUP_FLAG" ]; then
    echo "✅ Setup already completed, skipping installation."
    # Keep Apache running
    wait $APACHE_PID
    exit $?
fi

echo "🔧 Starting Dolibarr automatic installation..."

# Wait a bit more for full initialization
sleep 10

# Create directories if they don't exist
mkdir -p /var/www/documents
mkdir -p /var/www/html/conf
chown -R www-data:www-data /var/www/documents /var/www/html/conf

# Database connection details
DB_HOST="${DOLI_DB_HOST:-db}"
DB_USER="${DOLI_DB_USER:-dolibarr}"
DB_PASS="${DOLI_DB_PASSWORD:-dolibarr123}"
DB_NAME="${DOLI_DB_NAME:-dolibarr}"
ADMIN_LOGIN="${DOLI_ADMIN_LOGIN:-admin}"
ADMIN_PASS="${DOLI_ADMIN_PASSWORD:-admin123}"

# Wait for database tables to be created
echo "📝 Waiting for database to be ready..."
DB_COUNTER=0
until mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "SELECT 1;" > /dev/null 2>&1; do
    sleep 5
    DB_COUNTER=$((DB_COUNTER + 5))
    if [ $DB_COUNTER -ge 60 ]; then
        echo "⚠️  Database connection timeout, but continuing..."
        break
    fi
done

# Create Dolibarr configuration file
echo "📝 Creating Dolibarr configuration..."
cat > /var/www/html/conf/conf.php << 'EOF'
<?php
$dolibarr_main_url_root='http://localhost:8086';
$dolibarr_main_document_root='/var/www/html';
$dolibarr_main_url_root_alt='/custom';
$dolibarr_main_document_root_alt='/var/www/html/custom';
$dolibarr_main_data_root='/var/www/documents';
$dolibarr_main_db_host='db';
$dolibarr_main_db_port='3306';
$dolibarr_main_db_name='dolibarr';
$dolibarr_main_db_prefix='llx_';
$dolibarr_main_db_user='dolibarr';
$dolibarr_main_db_pass='dolibarr123';
$dolibarr_main_db_type='mysqli';
$dolibarr_main_db_character_set='utf8';
$dolibarr_main_db_collation='utf8_unicode_ci';
$dolibarr_main_authentication='dolibarr';
$dolibarr_main_prod='0';
$dolibarr_main_force_https='0';
$dolibarr_main_restrict_os_commands='mysqldump, mysql, pg_dump, pgrestore';
$dolibarr_nocsrfcheck='0';
$dolibarr_mailing_limit_sendbyweb='0';
$dolibarr_mailing_limit_sendbycli='0';
EOF

chmod 640 /var/www/html/conf/conf.php
chown www-data:www-data /var/www/html/conf/conf.php

echo "✅ Configuration file created"

# Run Dolibarr installation via web interface
echo "⚙️  Installing Dolibarr database..."

# Step 1: Trigger installation
curl -s -X POST "http://localhost/install/step1.php" \
  -d "testpost=ok" \
  -d "action=set" \
  > /dev/null

sleep 5

# Step 2: Create database tables
curl -s -X POST "http://localhost/install/step2.php" \
  -d "action=set" \
  > /dev/null

sleep 10

# Step 3: Create admin user
curl -s -X POST "http://localhost/install/step5.php" \
  -d "action=set" \
  -d "login=${ADMIN_LOGIN}" \
  -d "pass=${ADMIN_PASS}" \
  -d "pass_verif=${ADMIN_PASS}" \
  > /dev/null

echo "✅ Installation request completed"

# Verify installation
echo "🔍 Verifying installation..."
sleep 10

# Check database tables
TABLES=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "SHOW TABLES LIKE 'llx_%';" 2>/dev/null | wc -l | tr -d ' \n' || echo "0")

echo "   Database tables found: $TABLES"

if [ ! -z "$TABLES" ] && [ "$TABLES" -gt 50 ]; then
    echo "🎉 INSTALLATION SUCCESSFUL! ($TABLES tables created)"
    
    # Create test users for BacFuzz
    echo "👥 Creating test users..."
    
    # Function to create Dolibarr user
    create_dolibarr_user() {
        local username=$1
        local password=$2
        local firstname=$3
        local lastname=$4
        local admin_flag=$5
        
        echo "  → Creating user $username..."
        
        # Check if user already exists
        USER_EXISTS=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -se "SELECT COUNT(*) FROM llx_user WHERE login='$username';" 2>/dev/null || echo "0")
        
        if [ "$USER_EXISTS" -gt 0 ]; then
            echo "    $username already exists, skipping..."
            return 0
        fi
        
        # Generate bcrypt hash using PHP (filter only the hash line starting with $2y)
        PASSWORD_HASH=$(php -d error_reporting=0 -d display_errors=0 -r "echo password_hash('$password', PASSWORD_BCRYPT);" 2>&1 | grep -E '^\$2y\$')
        
        # Get current timestamp
        CURRENT_DATE=$(date '+%Y-%m-%d %H:%M:%S')
        
        # Insert user into database
        mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" <<-EOSQL 2>/dev/null
			INSERT INTO llx_user (
			    entity, login, pass_crypted, lastname, firstname,
			    admin, employee, statut, datec
			) VALUES (
			    1, '$username', '$PASSWORD_HASH', '$lastname', '$firstname',
			    $admin_flag, 1, 1, '$CURRENT_DATE'
			);
		EOSQL
        
        if [ $? -eq 0 ]; then
            echo "    ✓ $username created successfully"
        else
            echo "    ✗ Failed to create $username"
            return 1
        fi
    }
    
    # Create test users
    create_dolibarr_user "testuser" "TestUser2024!" "Test" "User" "0"
    create_dolibarr_user "editor" "EditorPass2024!" "Editor" "User" "0"
    create_dolibarr_user "viewer" "ViewerPass2024!" "Viewer" "User" "0"
    
    echo "✅ Test users created successfully"
    
    # Mark setup as completed
    touch "$SETUP_FLAG"
    
    echo ""
    echo "================================================="
    echo "🎯 Dolibarr BacFuzz System READY!"
    echo "================================================="
    echo ""
    echo "📍 ACCESS INFORMATION:"
    echo "   🌐 Main Site: http://localhost:8086"
    echo ""
    echo "🔑 USER CREDENTIALS:"
    echo "   👤 admin      : admin123         (Administrator)"
    echo "   👤 testuser   : TestUser2024!    (Regular User)"
    echo "   � editor     : EditorPass2024!  (Editor)"
    echo "   👤 viewer     : ViewerPass2024!  (Viewer)"
    echo ""
    echo "✅ Auto-Setup completed!"
else
    echo "⚠️  Installation may not be complete. Tables found: $TABLES"
    echo "   You may need to complete installation manually at http://localhost:8086/install/"
fi

# Keep Apache running
wait $APACHE_PID
