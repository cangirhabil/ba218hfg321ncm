echo "🎯 osTicket OTONOM KURULUM SİSTEMİ - BacFuzz Hazır"
echo "================================================="
echo ""

# Check if Docker is available
if ! docker --version >/dev/null 2>&1; then
    echo "❌ Docker bulunamadı! Lütfen Docker'ı kurun."
    exit 1
fi
echo "✅ Docker mevcut"

# Check if osTicket-develop exists, if not download it
OSTICKET_DIR="../osTicket-develop"
if [ ! -d "$OSTICKET_DIR" ]; then
    echo ""
    echo "📥 osTicket kaynak kodu bulunamadı, indiriliyor..."
    cd ..
    
    # Remove only specific osTicket source directories (NOT the setup directory!)
    rm -rf osTicket-develop osTicket-master
    
    echo "   GitHub'dan osTicket indiriliyor..."
    if git clone https://github.com/osTicket/osTicket.git osTicket-develop; then
        echo "✅ osTicket kaynak kodu başarıyla indirildi"
    else
        echo "❌ osTicket indirme hatası!"
        exit 1
    fi
    
    cd osTicket
else
    echo "✅ osTicket kaynak kodu mevcut"
fi

echo ""
echo "🧹 Önceki kurulumu temizleniyor..."
# Cleanup first
docker compose down -v 2>/dev/null
rm -f /tmp/osticket_*
docker system prune -f >/dev/null 2>&1

echo ""
echo "🏗️  Docker container'ları oluşturuluyor ve başlatılıyor..."
docker compose up -d --build

echo ""
echo "⏳ Servisler başlatılıyor ve hazırlanıyor..."
sleep 25

# Wait for MySQL to be ready
echo "🗄️  Veritabanı hazırlanıyor..."
for i in {1..40}; do
    if docker exec osticket-db-1 mysqladmin ping -h localhost -u osticket -posticket123 >/dev/null 2>&1; then
        echo "✅ Veritabanı hazır!"
        break
    fi
    echo "   Veritabanı bekleniyor... ($i/40)"
    sleep 4
done

echo ""
echo "🔧 Fuzzer instrumentation hazırlanıyor..."
# Initialize fuzzer instrumentation
docker exec osticket-app-1 mkdir -p /var/www/fuzzer
docker exec osticket-app-1 touch /var/www/fuzzer/__fuzzer__startcov.php
docker exec osticket-app-1 touch /var/www/fuzzer/__fuzzer__stopcov.php
docker exec osticket-app-1 chown -R www-data:www-data /var/www/fuzzer/
echo "✅ Fuzzer instrumentation hazır"

# Wait for web server
echo ""
echo "🌐 Web sunucusu hazırlanıyor..."
for i in {1..40}; do
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8085/setup/ 2>/dev/null || echo "000")
    if [ "$response" = "200" ] || [ "$response" = "301" ] || [ "$response" = "302" ]; then
        echo "✅ Web sunucusu hazır! (HTTP $response)"
        break
    fi
    echo "   Web sunucusu bekleniyor... ($i/40) (HTTP $response)"
    sleep 4
done

if [ "$response" = "000" ]; then
    echo "❌ Web sunucusu başlatılamadı!"
    exit 1
fi

echo ""
echo "🚀 OTOMATİK KURULUM BAŞLATILIYOR..."
echo ""

# Create config file first
echo "📝 Konfigurasyon dosyası oluşturuluyor..."
if docker exec osticket-app-1 cp include/ost-sampleconfig.php include/ost-config.php 2>/dev/null; then
    docker exec osticket-app-1 chmod 666 include/ost-config.php
    echo "✅ Konfigurasyon dosyası hazır"
else
    echo "❌ Konfigurasyon dosyası oluşturulamadı!"
    exit 1
fi

# Step 1: Check prerequisites
echo ""
echo "🔍 Adım 1/2: Sistem gereksinimleri kontrol ediliyor..."
curl -X POST \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -c /tmp/osticket_cookies.txt \
  --data "s=prereq&submit=Continue" \
  "http://localhost:8085/setup/install.php" \
  -s -o /tmp/prereq_response.html

if [ $? -eq 0 ]; then
    echo "✅ Sistem gereksinimleri kontrolü tamamlandı"
else
    echo "❌ Sistem gereksinimleri kontrolü başarısız!"
fi

sleep 5

# Step 2: Submit installation
echo ""
echo "⚙️  Adım 2/2: osTicket kuruluyor..."
curl -X POST \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -b /tmp/osticket_cookies.txt \
  -c /tmp/osticket_cookies.txt \
  --data "s=install&name=osTicket+BacFuzz+System&email=system@osticket.local&fname=admin&lname=user&admin_email=admin@osticket.local&username=adminuser&passwd=admin123&passwd2=admin123&prefix=ost_&dbhost=db&dbname=osticket&dbuser=osticket&dbpass=osticket123" \
  "http://localhost:8085/setup/install.php" \
  -s -o /tmp/config_response.html

echo "✅ Kurulum isteği gönderildi, tamamlanması bekleniyor..."
sleep 20

echo ""
echo "🔍 KURULUM DOĞRULANIYOR..."

MAX_ATTEMPTS=20
for attempt in $(seq 1 $MAX_ATTEMPTS); do
    TABLES=$(docker exec osticket-db-1 mysql -u osticket -posticket123 -e "USE osticket; SHOW TABLES;" 2>/dev/null | grep "ost_" 2>/dev/null | wc -l | tr -d ' \n')
    
    echo "   Deneme $attempt/$MAX_ATTEMPTS: $TABLES veritabanı tablosu bulundu"
    
    if [ ! -z "$TABLES" ] && [ "$TABLES" -gt 25 ]; then
        echo ""
        echo "🎉 KURULUM BAŞARILI! ($TABLES tablo oluşturuldu)"
        
        # Final verification - test endpoints
        echo ""
        echo "🧪 Son kontroller yapılıyor..."
        
        main_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8085/ 2>/dev/null)
        admin_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8085/scp/login.php 2>/dev/null)
        
        echo "   Ana sayfa: HTTP $main_response"
        echo "   Admin paneli: HTTP $admin_response"
        
        if [ "$main_response" = "200" ] && [ "$admin_response" = "200" ]; then
            echo "✅ Tüm endpoint'ler çalışıyor"
        else
            echo "⚠️  Bazı endpoint'ler henüz hazır değil, ancak kurulum tamamlandı"
        fi
        
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
        echo "🚀 FUZZING İÇİN HAZIR!"
        echo "   Şimdi fuzzer_osticket.sh çalıştırabilirsiniz:"
        echo "   cd /Users/admin/Desktop/ba218hfg321ncm/bacfuzz/scripts"
        echo "   ./fuzzer_osticket.sh"
        echo ""
        echo "🛑 SİSTEMİ DURDURMAK İÇİN:"
        echo "   docker compose down"
        echo ""
        echo "✅ Kurulum tamamlandı!"
        
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
echo "🔧 Kurulum başarısız olduysa:"
echo "   1. Veritabanı bağlantısını kontrol edin:"
echo "      docker exec osticket-db-1 mysql -u osticket -posticket123 -e 'SHOW DATABASES;'"
echo "   2. Manuel kurulum: http://localhost:8085/setup/"
echo "   3. Yukarıdaki giriş bilgilerini kullanın"
echo ""
echo "🔄 Tekrar denemek için:"
echo "   docker compose down -v"
echo "   ./setup.sh"

exit 1