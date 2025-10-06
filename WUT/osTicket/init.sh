#!/bin/bash

# osTicket Auto-Setup Entrypoint Script
# This script runs automatically when the container starts
# It handles the shared entrypoint setup AND osTicket-specific installation

set -e

echo "🎯 osTicket AUTONOMOUS INSTALLATION SYSTEM - BacFuzz Ready"
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

# Function to handle signals and cleanup
cleanup() {
    echo "Received shutdown signal, stopping Apache..."
    kill -TERM $APACHE_PID 2>/dev/null || true
    wait $APACHE_PID 2>/dev/null || true
    echo "Apache stopped gracefully"
    exit 0
}

# Trap SIGTERM and SIGINT for graceful shutdown
trap cleanup SIGTERM SIGINT

# Wait for web server to be ready
echo "🌐 Waiting for web server..."
TIMEOUT=120
COUNTER=0

until curl -f -s http://localhost/setup/ > /dev/null 2>&1; do
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
SETUP_FLAG="/var/www/html/.setup_completed"
if [ -f "$SETUP_FLAG" ]; then
    echo "✅ Setup already completed, skipping installation."
    # Keep Apache running
    wait $APACHE_PID
    exit $?
fi

echo "🔧 Starting osTicket automatic installation..."

# Wait a bit more for full initialization
sleep 10

cd /var/www/html

echo "📝 Creating configuration file..."
if cp include/ost-sampleconfig.php include/ost-config.php 2>/dev/null; then
    chmod 666 include/ost-config.php
    chown www-data:www-data include/ost-config.php
    echo "✅ Configuration file ready"
else
    echo "❌ Failed to create configuration file!"
    exit 1
fi

# Step 1: Check prerequisites
echo "🔍 Step 1/2: Checking system requirements..."
curl -X POST \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -c /tmp/osticket_cookies.txt \
  --data "s=prereq&submit=Continue" \
  "http://localhost/setup/install.php" \
  -s -o /tmp/prereq_response.html

if [ $? -eq 0 ]; then
    echo "✅ System requirements check completed"
else
    echo "❌ System requirements check failed!"
fi

sleep 5

# Step 2: Submit installation
echo "⚙️  Step 2/2: Installing osTicket..."
curl -X POST \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -b /tmp/osticket_cookies.txt \
  -c /tmp/osticket_cookies.txt \
  --data "s=install&name=osTicket+BacFuzz+System&email=system@osticket.local&fname=admin&lname=user&admin_email=admin@osticket.local&username=adminuser&passwd=admin123&passwd2=admin123&prefix=ost_&dbhost=db&dbname=osticket&dbuser=osticket&dbpass=osticket123" \
  "http://localhost/setup/install.php" \
  -s -o /tmp/config_response.html

echo "✅ Installation request sent, waiting for completion..."
sleep 20

echo "🔍 VERIFYING INSTALLATION..."

MAX_ATTEMPTS=20
for attempt in $(seq 1 $MAX_ATTEMPTS); do
    # Check database tables
    TABLES=$(mysql -h db -u osticket -posticket123 -e "USE osticket; SHOW TABLES;" 2>/dev/null | grep "ost_" 2>/dev/null | wc -l | tr -d ' \n' || echo "0")
    
    echo "   Attempt $attempt/$MAX_ATTEMPTS: $TABLES database tables found"
    
    if [ ! -z "$TABLES" ] && [ "$TABLES" -gt 25 ]; then
        echo "🎉 INSTALLATION SUCCESSFUL! ($TABLES tables created)"
        
        # Final verification - test endpoints
        echo "🧪 Performing final checks..."
        
        main_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ 2>/dev/null)
        admin_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/scp/login.php 2>/dev/null)
        
        echo "   Main page: HTTP $main_response"
        echo "   Admin panel: HTTP $admin_response"
        
        if [ "$main_response" = "200" ] && [ "$admin_response" = "200" ]; then
            echo "✅ All endpoints are working"
        else
            echo "⚠️  Some endpoints are not ready yet, but installation is complete"
        fi
        
        # Mark setup as completed
        touch "$SETUP_FLAG"
        
        echo ""
        echo "================================================="
        echo "🎯 osTicket BacFuzz System READY!"
        echo "================================================="
        echo ""
        echo "📍 ACCESS INFORMATION:"
        echo "   🌐 Main Site: http://localhost:8085"
        echo "   🔧 Admin Panel: http://localhost:8085/scp/login.php"
        echo "   🎫 New Ticket: http://localhost:8085/"
        echo ""
        echo "🔑 ADMIN LOGIN INFORMATION:"
        echo "   👤 Username: adminuser"
        echo "   🔒 Password: admin123"
        echo ""
        echo "✅ Auto-Setup completed!"
        
        # Keep Apache running
        wait $APACHE_PID
        exit 0
    fi
    
    if [ $attempt -lt $MAX_ATTEMPTS ]; then
        sleep 6
    fi
done

echo ""
echo "❌ AUTOMATIC INSTALLATION TIMEOUT"
echo ""
echo "📊 DEBUG INFORMATION:"
echo "   Database tables found: $TABLES"
if [ -f /tmp/config_response.html ]; then
    echo "   Installation response size: $(wc -c < /tmp/config_response.html) bytes"
fi

echo ""
echo "⚠️  Manual installation may be required: http://localhost:8085/setup/"
echo "   Use the login information above"

# Keep Apache running even if setup failed
wait $APACHE_PID
