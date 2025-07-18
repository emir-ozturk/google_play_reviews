"""
Google Play Review Scraper Module
"""

import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from google_play_scraper import app, reviews, Sort
from google_play_scraper.exceptions import GooglePlayScraperException

from config import Config
from utils import DateUtils, ValidationUtils, FileHandler


class GooglePlayReviewScraper:
    """Main class for scraping Google Play reviews"""
    
    def __init__(self, app_id: str, language: str = Config.DEFAULT_LANGUAGE, 
                 country: str = Config.DEFAULT_COUNTRY):
        """
        Initialize the scraper
        
        Args:
            app_id: Google Play app ID (e.g., 'com.sozlerkosku.beste5v2')
            language: Language code (e.g., 'tr')
            country: Country code (e.g., 'tr')
        """
        self.app_id = app_id
        self.language = language
        self.country = country
        self.app_info = None
        
        # Validate inputs
        if not ValidationUtils.validate_app_id(app_id):
            raise ValueError(f"Invalid app ID format: {app_id}")
        
        if not ValidationUtils.validate_language_code(language):
            raise ValueError(f"Invalid language code: {language}")
        
        print(f"Scraper initialized for app: {app_id}")
        print(f"Language: {language}, Country: {country}")
    
    def get_app_info(self) -> Dict[str, Any]:
        """Get basic app information"""
        if self.app_info is None:
            try:
                print("Fetching app information...")
                self.app_info = app(
                    self.app_id,
                    lang=self.language,
                    country=self.country
                )
                print(f"App found: {self.app_info.get('title', 'Unknown')}")
                print(f"Developer: {self.app_info.get('developer', 'Unknown')}")
                print(f"Rating: {self.app_info.get('score', 'N/A')}/5")
                print(f"Reviews count: {self.app_info.get('reviews', 'N/A')}")
                
            except GooglePlayScraperException as e:
                print(f"Error fetching app info: {e}")
                raise
        
        return self.app_info
    
    def scrape_reviews(self, months_back: int = Config.DEFAULT_MONTHS_BACK,
                      count: int = Config.DEFAULT_COUNT) -> List[Dict[str, Any]]:
        """
        Scrape reviews from Google Play Store
        
        Args:
            months_back: Number of months to go back (default: 12)
            count: Maximum number of reviews to fetch (default: 1000)
            
        Returns:
            List of review dictionaries
        """
        print(f"\nStarting review scraping...")
        print(f"Time range: Last {months_back} months")
        print(f"Maximum reviews: {count}")
        
        # Get date threshold
        date_threshold = Config.get_date_threshold(months_back)
        print(f"Date threshold: {DateUtils.format_date(date_threshold)}")
        
        try:
            # Get app info first
            self.get_app_info()
            
            # Scrape reviews
            print("Fetching reviews...")
            result, continuation_token = reviews(
                self.app_id,
                lang=self.language,
                country=self.country,
                sort=Sort.NEWEST,
                count=count
            )
            
            print(f"Initial batch: {len(result)} reviews fetched")
            
            # Filter reviews by date
            filtered_reviews = self._filter_reviews_by_date(result, date_threshold)
            print(f"Reviews within date range: {len(filtered_reviews)}")
            
            # Try to get more reviews if needed and continuation token exists
            all_reviews = filtered_reviews.copy()
            total_fetched = len(result)
            
            while continuation_token and len(all_reviews) < count and total_fetched < count * 2:
                print(f"Fetching more reviews... (Current: {len(all_reviews)})")
                time.sleep(1)  # Rate limiting
                
                try:
                    result, continuation_token = reviews(
                        self.app_id,
                        lang=self.language,
                        country=self.country,
                        sort=Sort.NEWEST,
                        count=min(200, count - len(all_reviews)),
                        continuation_token=continuation_token
                    )
                    
                    total_fetched += len(result)
                    batch_filtered = self._filter_reviews_by_date(result, date_threshold)
                    
                    if not batch_filtered:
                        print("No more reviews in date range found. Stopping.")
                        break
                    
                    all_reviews.extend(batch_filtered)
                    print(f"Added {len(batch_filtered)} more reviews")
                    
                except Exception as e:
                    print(f"Error fetching additional reviews: {e}")
                    break
            
            print(f"\nScraping completed!")
            print(f"Total reviews found: {len(all_reviews)}")
            
            return all_reviews
            
        except GooglePlayScraperException as e:
            print(f"Error during review scraping: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    def _filter_reviews_by_date(self, reviews_list: List[Dict[str, Any]], 
                               date_threshold: datetime) -> List[Dict[str, Any]]:
        """Filter reviews by date threshold"""
        filtered_reviews = []
        
        for review in reviews_list:
            review_date = review.get('at')
            if review_date and DateUtils.is_within_date_range(review_date, date_threshold):
                filtered_reviews.append(review)
        
        return filtered_reviews
    
    def export_reviews(self, reviews_list: List[Dict[str, Any]], 
                      save_json: bool = True) -> Tuple[str, str]:
        """
        Export reviews to files
        
        Args:
            reviews_list: List of review dictionaries
            save_json: Whether to save JSON backup
            
        Returns:
            Tuple of (txt_filename, json_filename)
        """
        if not reviews_list:
            print("No reviews to export")
            return "", ""
        
        # Generate filename
        filename = Config.get_output_filename(self.app_id, self.language)
        
        # Save to text file
        FileHandler.save_reviews_to_file(reviews_list, filename)
        
        # Save JSON backup if requested
        json_filename = ""
        if save_json:
            json_filename = filename.replace('.txt', '.json')
            FileHandler.save_reviews_to_json(reviews_list, filename)
        
        return filename, json_filename
    
    def get_review_stats(self, reviews_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about the scraped reviews"""
        if not reviews_list:
            return {}
        
        # Rating distribution
        rating_counts = {}
        for review in reviews_list:
            rating = review.get('score', 0)
            rating_counts[rating] = rating_counts.get(rating, 0) + 1
        
        # Date range
        dates = [review.get('at') for review in reviews_list if review.get('at')]
        oldest_date = min(dates) if dates else None
        newest_date = max(dates) if dates else None
        
        # Average rating
        ratings = [review.get('score', 0) for review in reviews_list if review.get('score')]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # Reviews with developer replies
        replied_reviews = [r for r in reviews_list if r.get('replyContent')]
        
        stats = {
            'total_reviews': len(reviews_list),
            'rating_distribution': rating_counts,
            'average_rating': round(avg_rating, 2),
            'oldest_review': DateUtils.format_date(oldest_date) if oldest_date else None,
            'newest_review': DateUtils.format_date(newest_date) if newest_date else None,
            'reviews_with_replies': len(replied_reviews),
            'reply_rate': round(len(replied_reviews) / len(reviews_list) * 100, 1) if reviews_list else 0
        }
        
        return stats
    
    def print_stats(self, stats: Dict[str, Any]) -> None:
        """Print review statistics"""
        print("\n" + "="*50)
        print("REVIEW STATISTICS")
        print("="*50)
        print(f"Total Reviews: {stats.get('total_reviews', 0)}")
        print(f"Average Rating: {stats.get('average_rating', 0)}/5")
        print(f"Date Range: {stats.get('oldest_review', 'N/A')} to {stats.get('newest_review', 'N/A')}")
        print(f"Reviews with Developer Replies: {stats.get('reviews_with_replies', 0)} ({stats.get('reply_rate', 0)}%)")
        
        print("\nRating Distribution:")
        rating_dist = stats.get('rating_distribution', {})
        for rating in sorted(rating_dist.keys(), reverse=True):
            count = rating_dist[rating]
            percentage = round(count / stats.get('total_reviews', 1) * 100, 1)
            stars = "⭐" * rating
            print(f"  {stars} ({rating}): {count} reviews ({percentage}%)")
        
        print("="*50) 