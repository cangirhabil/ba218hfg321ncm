#!/bin/bash

# osTicket Auto-Setup Entrypoint Script
# This script runs automatically when the container starts

set -e

echo "🎯 osTicket OTONOM KURULUM SİSTEMİ - BacFuzz Hazır"
echo "================================================="

# Start the original entrypoint in background
echo "🚀 osTicket başlatılıyor..."
apache2-foreground &
OSTICKET_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    kill $OSTICKET_PID 2>/dev/null || true
    wait $OSTICKET_PID 2>/dev/null || true
}
trap cleanup EXIT

# Wait for web server to be ready
echo "🌐 Web sunucusu hazırlanıyor..."
TIMEOUT=300  # 5 minute timeout
COUNTER=0

until curl -f -s http://localhost/setup/ > /dev/null 2>&1; do
    sleep 5
    COUNTER=$((COUNTER + 5))
    if [ $COUNTER -ge $TIMEOUT ]; then
        echo "❌ Web sunucusu $TIMEOUT saniye içinde hazır olmadı!"
        exit 1
    fi
    echo "   Web sunucusu bekleniyor... ($COUNTER/$TIMEOUT seconds)"
done

echo "✅ Web sunucusu hazır!"

# Check if setup has already been completed
SETUP_FLAG="/var/www/html/.setup_completed"
if [ -f "$SETUP_FLAG" ]; then
    echo "✅ Kurulum zaten tamamlanmış, atlaniyor."
    # Keep the main process running
    wait $OSTICKET_PID
    exit $?
fi

echo "🔧 osTicket otomatik kurulum başlatılıyor..."

# Wait a bit more for full initialization
sleep 10

echo "🔧 Fuzzer instrumentation hazırlanıyor..."
# Initialize fuzzer instrumentation
mkdir -p /var/www/fuzzer
touch /var/www/fuzzer/__fuzzer__startcov.php
touch /var/www/fuzzer/__fuzzer__stopcov.php
chown -R www-data:www-data /var/www/fuzzer/
echo "✅ Fuzzer instrumentation hazır"

echo "📝 Konfigurasyon dosyası oluşturuluyor..."
if cp include/ost-sampleconfig.php include/ost-config.php 2>/dev/null; then
    chmod 666 include/ost-config.php
    echo "✅ Konfigurasyon dosyası hazır"
else
    echo "❌ Konfigurasyon dosyası oluşturulamadı!"
    exit 1
fi

# Step 1: Check prerequisites
echo "🔍 Adım 1/2: Sistem gereksinimleri kontrol ediliyor..."
curl -X POST \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -c /tmp/osticket_cookies.txt \
  --data "s=prereq&submit=Continue" \
  "http://localhost/setup/install.php" \
  -s -o /tmp/prereq_response.html

if [ $? -eq 0 ]; then
    echo "✅ Sistem gereksinimleri kontrolü tamamlandı"
else
    echo "❌ Sistem gereksinimleri kontrolü başarısız!"
fi

sleep 5

# Step 2: Submit installation
echo "⚙️  Adım 2/2: osTicket kuruluyor..."
curl -X POST \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -b /tmp/osticket_cookies.txt \
  -c /tmp/osticket_cookies.txt \
  --data "s=install&name=osTicket+BacFuzz+System&email=system@osticket.local&fname=admin&lname=user&admin_email=admin@osticket.local&username=adminuser&passwd=admin123&passwd2=admin123&prefix=ost_&dbhost=db&dbname=osticket&dbuser=osticket&dbpass=osticket123" \
  "http://localhost/setup/install.php" \
  -s -o /tmp/config_response.html

echo "✅ Kurulum isteği gönderildi, tamamlanması bekleniyor..."
sleep 20

echo "🔍 KURULUM DOĞRULANIYOR..."

MAX_ATTEMPTS=20
for attempt in $(seq 1 $MAX_ATTEMPTS); do
    # Check database tables
    TABLES=$(mysql -h db -u osticket -posticket123 -e "USE osticket; SHOW TABLES;" 2>/dev/null | grep "ost_" 2>/dev/null | wc -l | tr -d ' \n' || echo "0")
    
    echo "   Deneme $attempt/$MAX_ATTEMPTS: $TABLES veritabanı tablosu bulundu"
    
    if [ ! -z "$TABLES" ] && [ "$TABLES" -gt 25 ]; then
        echo "🎉 KURULUM BAŞARILI! ($TABLES tablo oluşturuldu)"
        
        # Final verification - test endpoints
        echo "🧪 Son kontroller yapılıyor..."
        
        main_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ 2>/dev/null)
        admin_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/scp/login.php 2>/dev/null)
        
        echo "   Ana sayfa: HTTP $main_response"
        echo "   Admin paneli: HTTP $admin_response"
        
        if [ "$main_response" = "200" ] && [ "$admin_response" = "200" ]; then
            echo "✅ Tüm endpoint'ler çalışıyor"
        else
            echo "⚠️  Bazı endpoint'ler henüz hazır değil, ancak kurulum tamamlandı"
        fi
        
        # Mark setup as completed
        touch "$SETUP_FLAG"
        
        echo ""
        echo "================================================="
        echo "🎯 osTicket BacFuzz Sistemi HAZIR!"
        echo "================================================="
        echo ""
        echo "📍 ERİŞİM BİLGİLERİ:"
        echo "   🌐 Ana Site: http://localhost:8085"
        echo "   🔧 Admin Paneli: http://localhost:8085/scp/login.php"
        echo "   🎫 Yeni Bilet: http://localhost:8085/"
        echo ""
        echo "🔑 ADMİN GİRİŞ BİLGİLERİ:"
        echo "   👤 Kullanıcı adı: adminuser"
        echo "   🔒 Şifre: admin123"
        echo ""
        echo "✅ Auto-Setup tamamlandı!"
        
        # Keep the main osTicket process running
        wait $OSTICKET_PID
        exit 0
    fi
    
    if [ $attempt -lt $MAX_ATTEMPTS ]; then
        sleep 6
    fi
done

echo ""
echo "❌ OTOMATİK KURULUM ZAMAN AŞIMI"
echo ""
echo "📊 DEBUG BİLGİLERİ:"
echo "   Bulunan veritabanı tablosu: $TABLES"
if [ -f /tmp/config_response.html ]; then
    echo "   Kurulum yanıt boyutu: $(wc -c < /tmp/config_response.html) bytes"
fi

echo ""
echo "⚠️  Manuel kurulum gerekebilir: http://localhost:8085/setup/"
echo "   Yukarıdaki giriş bilgilerini kullanın"

# Keep the main process running even if setup failed
wait $OSTICKET_PID