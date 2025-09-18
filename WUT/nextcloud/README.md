# Nextcloud BACFuzz Test Environment

Bu klasör Nextcloud'u BACFuzz ile test etmek için gerekli dosyaları içerir.

## Dosyalar

- `docker-compose.yaml`: Nextcloud, MariaDB ve Redis servislerini içeren Docker Compose dosyası
- `setup.sh`: Test kullanıcıları ve dosyaları oluşturan kurulum scripti
- `../bacfuzz/auto_login/app_nextcloud.py`: Otomatik giriş scripti
- `../bacfuzz/scripts/fuzzer-nextcloud.sh`: BACFuzz test scripti

## Kullanım

### 1. Nextcloud'u Başlatma

```bash
cd WUT/nextcloud
docker compose up -d
```

### 2. Kurulum ve Yapılandırma

Nextcloud tamamen başladıktan sonra (yaklaşık 2-3 dakika):

```bash
./setup.sh
```

### 3. Manuel Kurulum (İsteğe bağlı)

Tarayıcıdan http://localhost:8084 adresine giderek:
- Admin kullanıcısı: `admin` / `admin123`
- Kurulum sihirbazını tamamlayın

### 4. BACFuzz Testini Çalıştırma

```bash
cd ../../bacfuzz/scripts
./fuzzer-nextcloud.sh
```

## Test Kullanıcıları

- **admin** (admin123): Yönetici yetkili
- **testuser** (testuser123): Normal kullanıcı
- **editor** (editor123): Düzenleyici grubu üyesi
- **viewer** (viewer123): Görüntüleyici grubu üyesi
- **Anonymous**: Giriş yapmamış kullanıcı

## Port

Nextcloud Port: **8084**

## BACFuzz Test Rolleri

- Admin: Tüm yönetici işlemleri
- User: Normal kullanıcı işlemleri
- Editor: Düzenleme yetkileri
- Viewer: Sadece görüntüleme yetkileri
- Anonymous: Yetkisiz erişim testleri

## Temizlik

```bash
docker compose down
docker system prune -f
```

## Notlar

- İlk başlatmada Nextcloud'un tamamen hazır olması 2-3 dakika sürebilir
- Setup script'i çalıştırmadan önce Nextcloud'un tamamen yüklendiğinden emin olun
- Test dosyaları otomatik olarak oluşturulur ve kullanıcılar arasında paylaşım testleri için kullanılır