#!/usr/bin/env python3
"""
Example usage script for Google Play Review Scraper
Bu script, scraper'ın farklı kullanım örneklerini gösterir.
"""

from scraper import GooglePlayReviewScraper
from config import Config


def example_basic_usage():
    """Temel kullanım örneği"""
    print("=== TEMEL KULLANIM ÖRNEĞİ ===")
    
    # Scraper'ı başlat
    scraper = GooglePlayReviewScraper(
        app_id="com.sozlerkosku.beste5v2",
        language="tr"
    )
    
    # Yorumları çek (son 1 yıl)
    reviews = scraper.scrape_reviews()
    
    # İstatistikleri göster
    if reviews:
        stats = scraper.get_review_stats(reviews)
        scraper.print_stats(stats)
        
        # Dosyalara kaydet
        scraper.export_reviews(reviews)
    
    print("\n" + "="*60 + "\n")


def example_custom_parameters():
    """Özel parametrelerle kullanım örneği"""
    print("=== ÖZEL PARAMETRELER ÖRNEĞİ ===")
    
    # Özel ayarlarla scraper başlat
    scraper = GooglePlayReviewScraper(
        app_id="com.whatsapp",
        language="en",
        country="us"
    )
    
    # Son 6 ay, maksimum 500 yorum
    reviews = scraper.scrape_reviews(
        months_back=6,
        count=500
    )
    
    if reviews:
        stats = scraper.get_review_stats(reviews)
        scraper.print_stats(stats)
        
        # Sadece TXT dosyası kaydet (JSON olmadan)
        scraper.export_reviews(reviews, save_json=False)
    
    print("\n" + "="*60 + "\n")


def example_multiple_apps():
    """Birden fazla uygulama için kullanım örneği"""
    print("=== ÇOKLU UYGULAMA ÖRNEĞİ ===")
    
    # Çekilecek uygulamaların listesi
    apps = [
        {"app_id": "com.instagram.android", "language": "tr"},
        {"app_id": "com.spotify.music", "language": "tr"},
        {"app_id": "com.netflix.mediaclient", "language": "en"}
    ]
    
    for app in apps:
        try:
            print(f"\nProcessing: {app['app_id']} ({app['language']})")
            
            scraper = GooglePlayReviewScraper(
                app_id=app["app_id"],
                language=app["language"]
            )
            
            # Son 3 ay, 200 yorum
            reviews = scraper.scrape_reviews(
                months_back=3,
                count=200
            )
            
            if reviews:
                stats = scraper.get_review_stats(reviews)
                print(f"Found {len(reviews)} reviews for {app['app_id']}")
                scraper.export_reviews(reviews)
            else:
                print(f"No reviews found for {app['app_id']}")
                
        except Exception as e:
            print(f"Error processing {app['app_id']}: {e}")
    
    print("\n" + "="*60 + "\n")


def example_statistics_only():
    """Sadece istatistik gösterme örneği"""
    print("=== SADECE İSTATİSTİK ÖRNEĞİ ===")
    
    scraper = GooglePlayReviewScraper(
        app_id="com.sozlerkosku.beste5v2",
        language="tr"
    )
    
    # Yorumları çek ama dosya kaydetme
    reviews = scraper.scrape_reviews(months_back=12, count=100)
    
    if reviews:
        # Sadece istatistikleri göster
        stats = scraper.get_review_stats(reviews)
        scraper.print_stats(stats)
        
        # Ek istatistikler
        print("\nEK İSTATİSTİKLER:")
        print(f"Ortalama yorum uzunluğu: {sum(len(r.get('content', '')) for r in reviews) / len(reviews):.1f} karakter")
        
        # En çok beğenilen yorumlar
        top_reviews = sorted(reviews, key=lambda x: x.get('thumbsUpCount', 0), reverse=True)[:3]
        print("\nEn çok beğenilen yorumlar:")
        for i, review in enumerate(top_reviews, 1):
            print(f"{i}. {review.get('thumbsUpCount', 0)} beğeni - {review.get('content', '')[:50]}...")
    
    print("\n" + "="*60 + "\n")


def example_error_handling():
    """Hata yönetimi örneği"""
    print("=== HATA YÖNETİMİ ÖRNEĞİ ===")
    
    # Geçersiz uygulama kimliği
    try:
        scraper = GooglePlayReviewScraper(
            app_id="invalid.app.id",
            language="tr"
        )
        reviews = scraper.scrape_reviews()
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Scraping error: {e}")
    
    # Geçersiz dil kodu
    try:
        scraper = GooglePlayReviewScraper(
            app_id="com.sozlerkosku.beste5v2",
            language="invalid"
        )
    except ValueError as e:
        print(f"Language validation error: {e}")
    
    print("\n" + "="*60 + "\n")


def main():
    """Ana fonksiyon - tüm örnekleri çalıştır"""
    print("Google Play Review Scraper - Kullanım Örnekleri")
    print("="*60)
    
    # Hangi örneği çalıştırmak istediğinizi seçin
    examples = {
        "1": ("Temel Kullanım", example_basic_usage),
        "2": ("Özel Parametreler", example_custom_parameters),
        "3": ("Çoklu Uygulama", example_multiple_apps),
        "4": ("Sadece İstatistik", example_statistics_only),
        "5": ("Hata Yönetimi", example_error_handling),
        "6": ("Tüm Örnekler", lambda: [func() for _, func in examples.values() if func != examples["6"][1]])
    }
    
    print("\nMevcut örnekler:")
    for key, (name, _) in examples.items():
        print(f"{key}. {name}")
    
    choice = input("\nÇalıştırmak istediğiniz örnek numarasını girin (1-6): ").strip()
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\n{name} çalıştırılıyor...\n")
        func()
    else:
        print("Geçersiz seçim!")


if __name__ == "__main__":
    main() 