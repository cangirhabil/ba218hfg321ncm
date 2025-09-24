#!/bin/bash

echo "🎯 osTicket FULLY AUTOMATED Installation (Fixed Version)..."

# Cleanup first
docker compose down -v 2>/dev/null
rm -f /tmp/osticket_*

echo "Starting containers..."
docker compose up -d

echo "Waiting for services to initialize..."
sleep 15

# Wait for MySQL to be ready
echo "Waiting for database..."
for i in {1..30}; do
    if docker exec osticket-db-1 mysqladmin ping -h localhost -u osticket -posticket123 >/dev/null 2>&1; then
        echo "  Database ready!"
        break
    fi
    echo "  Database not ready, waiting... ($i/30)"
    sleep 2
done

# Wait for web server
echo "Waiting for web server..."
for i in {1..20}; do
    if curl -s http://localhost:8085/setup/ >/dev/null 2>&1; then
        echo "  Web server ready!"
        break
    fi
    echo "  Web server not ready, waiting... ($i/20)"
    sleep 2
done

echo ""
echo "🚀 STARTING AUTOMATED INSTALLATION..."

# Create config file first
echo "  Creating configuration file..."
docker exec osticket-app-1 cp include/ost-sampleconfig.php include/ost-config.php
docker exec osticket-app-1 chmod 666 include/ost-config.php

# Step 1: Check prerequisites
echo "  Step 1/3: Checking prerequisites..."
curl -X POST \
  -H "User-Agent: Mozilla/5.0" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -c /tmp/osticket_cookies.txt \
  --data "s=prereq&submit=Continue" \
  "http://localhost:8085/setup/install.php" \
  -s -o /tmp/prereq_response.html

sleep 3

# Step 2: Submit installation directly (skip config step)
echo "  Step 2/2: Installing osTicket..."
curl -X POST \
  -H "User-Agent: Mozilla/5.0" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "s=install&name=osTicket+BacFuzz+System&email=system@osticket.local&fname=admin&lname=user&admin_email=admin@osticket.local&username=adminuser&passwd=admin123&passwd2=admin123&prefix=ost_&dbhost=db&dbname=osticket&dbuser=osticket&dbpass=osticket123" \
  "http://localhost:8085/setup/install.php" \
  -s -o /tmp/config_response.html

echo "  Installation submitted, waiting for completion..."
sleep 10

# Verify installation by checking database tables
echo ""
echo "🔍 Verifying installation..."

MAX_ATTEMPTS=15
for attempt in $(seq 1 $MAX_ATTEMPTS); do
    TABLES=$(docker exec osticket-db-1 mysql -u osticket -posticket123 -e "USE osticket; SHOW TABLES;" 2>/dev/null | grep "ost_" 2>/dev/null | wc -l | tr -d ' \n')
    
    echo "  Attempt $attempt/$MAX_ATTEMPTS: Found $TABLES database tables"
    
    if [ ! -z "$TABLES" ] && [ "$TABLES" -gt 25 ]; then
        echo ""
        echo "🎉 INSTALLATION SUCCESSFUL! ($TABLES tables created)"
        echo ""
        echo "📍 ACCESS INFORMATION:"
        echo "   🌐 Main Site: http://localhost:8085"
        echo "   🔧 Admin Panel: http://localhost:8085/scp/login.php"
        echo "   🎫 New Ticket: http://localhost:8085/"
        echo ""
        echo "🔑 ADMIN CREDENTIALS:"
        echo "   👤 Username: adminuser"
        echo "   🔒 Password: admin123"
        echo ""
        echo "✅ osTicket is ready for BacFuzz testing!"
        exit 0
    fi
    
    if [ $attempt -lt $MAX_ATTEMPTS ]; then
        sleep 5
    fi
done

echo ""
echo "❌ AUTOMATIC INSTALLATION TIMEOUT"
echo "   Check installation manually at: http://localhost:8085/setup/"
echo ""

# Show debug info
echo "📊 DEBUG INFORMATION:"
echo "Database tables found: $TABLES"
if [ -f /tmp/config_response.html ]; then
    echo "Configuration response size: $(wc -c < /tmp/config_response.html) bytes"
fi

echo ""
echo "🔧 If installation failed, you may need to:"
echo "   1. Check database connection: docker exec osticket-db-1 mysql -u osticket -posticket123 -e 'SHOW DATABASES;'"
echo "   2. Manually complete at: http://localhost:8085/setup/"
echo "   3. Use credentials above"

exit 1