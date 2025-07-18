# Google Play Review Scraper

Google Play Store'dan uygulama yorumlarını çeken modüler ve okunabilir Python kodu.

## Özellikler

- 📱 Herhangi bir Google Play uygulamasından yorum çekme
- 🌍 Çoklu dil ve ülke desteği
- ⏰ Zaman aralığı filtreleme (varsayılan: son 1 yıl)
- 📊 Detaylı yorum istatistikleri
- 💾 TXT ve JSON formatlarında kaydetme
- 🔧 Modüler ve genişletilebilir kod yapısı
- 🎯 Komut satırı ve interaktif mod desteği

## Kurulum

1. Repository'yi klonlayın:
```bash
git clone <repository-url>
cd google_play_reviews
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

### Komut Satırı Kullanımı

Temel kullanım:
```bash
python main.py com.sozlerkosku.beste5v2 tr
```

Gelişmiş kullanım:
```bash
python main.py com.sozlerkosku.beste5v2 tr --months 6 --count 2000
```

### Parametreler

- `app_id`: Google Play uygulama kimliği (örn: `com.sozlerkosku.beste5v2`)
- `language`: Dil kodu (örn: `tr`, `en`, `de`)
- `--months`: Kaç ay geriye gidileceği (varsayılan: 12)
- `--count`: Maksimum çekilecek yorum sayısı (varsayılan: 1000)
- `--country`: Ülke kodu (varsayılan: `tr`)
- `--no-json`: JSON backup dosyası oluşturma
- `--stats-only`: Sadece istatistikleri göster, dosya kaydetme

### İnteraktif Mod

Parametre vermeden çalıştırırsanız interaktif mod başlar:
```bash
python main.py
```

## Örnek Kullanımlar

### Temel Örnekler

```bash
# Türkçe yorumları çek (son 1 yıl)
python main.py com.sozlerkosku.beste5v2 tr

# İngilizce yorumları çek (son 6 ay)
python main.py com.whatsapp tr --months 6

# Maksimum 500 yorum çek
python main.py com.instagram.android en --count 500

# Sadece istatistikleri göster
python main.py com.spotify.music tr --stats-only
```

### Gelişmiş Örnekler

```bash
# Son 2 yıl, 3000 yorum, JSON backup olmadan
python main.py com.sozlerkosku.beste5v2 tr --months 24 --count 3000 --no-json

# ABD pazarından İngilizce yorumlar
python main.py com.netflix.mediaclient en --country us --months 12
```

## Çıktı Dosyaları

Scraper iki tür dosya oluşturur:

1. **TXT Dosyası** (`appid_language.txt`): Okunabilir format
2. **JSON Dosyası** (`appid_language.json`): Programatik kullanım için

### TXT Dosyası Formatı

```
Google Play Reviews Export
Generated on: 2024-01-15 14:30:25
Total reviews: 245
================================================================================

Review #1
Review ID: gp:AOqpTOF...
User: Kullanıcı Adı
Rating: 5/5
Date: 2024-01-10 12:30:00
Thumbs Up: 3
Content:
Çok güzel bir uygulama, herkese tavsiye ederim!
Developer Reply: Teşekkürler!
Reply Date: 2024-01-11 09:15:00
--------------------------------------------------------------------------------
```

### JSON Dosyası Formatı

```json
{
  "export_date": "2024-01-15T14:30:25.123456",
  "total_reviews": 245,
  "reviews": [
    {
      "reviewId": "gp:AOqpTOF...",
      "userName": "Kullanıcı Adı",
      "content": "Çok güzel bir uygulama!",
      "score": 5,
      "thumbsUpCount": 3,
      "at": "2024-01-10T12:30:00",
      "replyContent": "Teşekkürler!",
      "repliedAt": "2024-01-11T09:15:00"
    }
  ]
}
```

## Proje Yapısı

```
google_play_reviews/
├── config.py          # Konfigürasyon ayarları
├── utils.py           # Yardımcı fonksiyonlar
├── scraper.py         # Ana scraper sınıfı
├── main.py            # Ana çalıştırma scripti
├── requirements.txt   # Python bağımlılıkları
├── README.md          # Bu dosya
└── reviews/           # Çıktı dosyaları (otomatik oluşturulur)
    ├── app_id_tr.txt
    └── app_id_tr.json
```

## Konfigürasyon

`config.py` dosyasından varsayılan ayarları değiştirebilirsiniz:

```python
class Config:
    DEFAULT_MONTHS_BACK = 12    # Varsayılan zaman aralığı (ay)
    DEFAULT_COUNT = 1000        # Varsayılan maksimum yorum sayısı
    DEFAULT_LANGUAGE = "tr"     # Varsayılan dil
    DEFAULT_COUNTRY = "tr"      # Varsayılan ülke
```

## İstatistikler

Scraper otomatik olarak şu istatistikleri hesaplar:

- Toplam yorum sayısı
- Ortalama puan
- Puan dağılımı (1-5 yıldız)
- En eski ve en yeni yorum tarihleri
- Developer yanıtı olan yorumlar
- Yanıt oranı

## Hata Yönetimi

Scraper şu durumları ele alır:

- Geçersiz uygulama kimliği
- Ağ bağlantı sorunları
- Rate limiting
- Geçersiz dil/ülke kodları
- Dosya yazma hataları

## Geliştirici Notları

### Modüler Yapı

- `config.py`: Tüm konfigürasyon ayarları
- `utils.py`: Dosya işlemleri, tarih utilities, validasyon
- `scraper.py`: Ana scraping logic
- `main.py`: CLI interface ve örnek kullanım

### Genişletme

Yeni özellikler eklemek için:

1. `Config` sınıfına yeni ayarlar ekleyin
2. `utils.py`'ye yardımcı fonksiyonlar ekleyin
3. `GooglePlayReviewScraper` sınıfını genişletin
4. `main.py`'de CLI parametrelerini güncelleyin

## Yasal Uyarılar

- Google Play Store'un kullanım şartlarına uygun şekilde kullanın
- Rate limiting'e dikkat edin
- Kişisel verileri koruyun
- Ticari kullanım için Google'ın politikalarını kontrol edin

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/new-feature`)
3. Commit yapın (`git commit -am 'Add new feature'`)
4. Push yapın (`git push origin feature/new-feature`)
5. Pull Request açın

## Sorun Bildirme

Sorun bildirmek için GitHub Issues kullanın. 