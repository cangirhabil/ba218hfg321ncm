#!/bin/bash

echo "=== Nextcloud Test Kullanıcıları Kurulum Scripti ==="

# Nextcloud'un hazır olmasını bekle
echo "Nextcloud'un hazır olmasını bekleniyor..."
until curl -s http://localhost:8084/login > /dev/null; do
    sleep 2
    echo "Nextcloud henüz hazır değil, bekleniyor..."
done
echo "Nextcloud hazır!"

# Admin ile test kullanıcıları oluştur
echo "Test kullanıcıları oluşturuluyor..."

echo "1. testuser oluşturuluyor..."
docker exec nextcloud-app-1 php occ user:add --password-from-env testuser
echo "testuser123." | docker exec -i nextcloud-app-1 sh -c 'export OC_PASS=$(cat) && php occ user:add --password-from-env testuser'

echo "2. editor oluşturuluyor..."
echo "editor1234." | docker exec -i nextcloud-app-1 sh -c 'export OC_PASS=$(cat) && php occ user:add --password-from-env editor'

echo "3. viewer oluşturuluyor..."
echo "viewer123." | docker exec -i nextcloud-app-1 sh -c 'export OC_PASS=$(cat) && php occ user:add --password-from-env viewer'

echo "Kullanıcılar oluşturuldu!"
echo ""
echo "=== Test Kullanıcıları ==="
echo "Admin: admin / admin123"
echo "User:  testuser / testuser123."
echo "Editor: editor / editor1234."
echo "Viewer: viewer / viewer123."
echo ""
echo "Manuel olarak http://localhost:8084/login adresine gidip bu bilgilerle giriş yapabilirsiniz."
echo "Her rol için giriş yapıp login state'lerini oluşturmak için:"
echo "1. Browser'da http://localhost:8084/login'e gidin"
echo "2. Yukarıdaki bilgilerle giriş yapın"
echo "3. Her kullanıcı için storage state dosyaları oluşturulacak"