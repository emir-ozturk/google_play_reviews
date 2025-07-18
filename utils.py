"""
Utility functions for Google Play Review Scraper
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from config import Config


class FileHandler:
    """Handle file operations for review data"""
    
    @staticmethod
    def ensure_output_directory() -> None:
        """Create output directory if it doesn't exist"""
        if not os.path.exists(Config.OUTPUT_DIR):
            os.makedirs(Config.OUTPUT_DIR)
            print(f"Created output directory: {Config.OUTPUT_DIR}")
    
    @staticmethod
    def save_reviews_to_file(reviews: List[Dict[str, Any]], filename: str) -> None:
        """Save reviews to a text file"""
        FileHandler.ensure_output_directory()
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        
        try:
            with open(filepath, 'w', encoding=Config.FILE_ENCODING) as f:
                f.write(f"Google Play Reviews Export\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total reviews: {len(reviews)}\n")
                f.write("="*80 + "\n\n")
                
                for i, review in enumerate(reviews, 1):
                    f.write(f"Review #{i}\n")
                    f.write(f"Review ID: {review.get('reviewId', 'N/A')}\n")
                    f.write(f"User: {review.get('userName', 'Anonymous')}\n")
                    f.write(f"Rating: {review.get('score', 'N/A')}/5\n")
                    f.write(f"Date: {review.get('at', 'N/A')}\n")
                    f.write(f"Thumbs Up: {review.get('thumbsUpCount', 0)}\n")
                    f.write(f"Content:\n{review.get('content', 'No content')}\n")
                    
                    # Add reply if exists
                    if review.get('replyContent'):
                        f.write(f"Developer Reply: {review.get('replyContent')}\n")
                        f.write(f"Reply Date: {review.get('repliedAt', 'N/A')}\n")
                    
                    f.write("-"*80 + "\n\n")
            
            print(f"Reviews saved to: {filepath}")
            print(f"Total reviews saved: {len(reviews)}")
            
        except Exception as e:
            print(f"Error saving reviews to file: {e}")
            raise
    
    @staticmethod
    def save_reviews_to_json(reviews: List[Dict[str, Any]], filename: str) -> None:
        """Save reviews to JSON file for backup"""
        FileHandler.ensure_output_directory()
        json_filename = filename.replace('.txt', '.json')
        filepath = os.path.join(Config.OUTPUT_DIR, json_filename)
        
        try:
            # Convert datetime objects to ISO format strings for JSON serialization
            json_reviews = []
            for review in reviews:
                json_review = review.copy()
                for key, value in json_review.items():
                    if isinstance(value, datetime):
                        json_review[key] = value.isoformat()
                json_reviews.append(json_review)
            
            with open(filepath, 'w', encoding=Config.FILE_ENCODING) as f:
                json.dump({
                    'export_date': datetime.now().isoformat(),
                    'total_reviews': len(reviews),
                    'reviews': json_reviews
                }, f, indent=2, ensure_ascii=False)
            
            print(f"JSON backup saved to: {filepath}")
            
        except Exception as e:
            print(f"Error saving JSON backup: {e}")


class DateUtils:
    """Utility functions for date operations"""
    
    @staticmethod
    def is_within_date_range(review_date: datetime, threshold_date: datetime) -> bool:
        """Check if review date is within the specified range"""
        return review_date >= threshold_date
    
    @staticmethod
    def format_date(date_obj: datetime) -> str:
        """Format datetime object to readable string"""
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def parse_review_date(date_str: str) -> datetime:
        """Parse review date string to datetime object"""
        try:
            # Handle different date formats if needed
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.now()


class ValidationUtils:
    """Utility functions for input validation"""
    
    @staticmethod
    def validate_app_id(app_id: str) -> bool:
        """Validate Google Play app ID format"""
        if not app_id:
            return False
        
        # Basic validation for app ID format
        if not app_id.count('.') >= 2:
            return False
        
        # Should not contain spaces or special characters
        if ' ' in app_id or any(char in app_id for char in ['/', '\\', '?', '&']):
            return False
        
        return True
    
    @staticmethod
    def validate_language_code(lang_code: str) -> bool:
        """Validate language code format"""
        if not lang_code:
            return False
        
        # Should be 2 characters
        if len(lang_code) != 2:
            return False
        
        # Should be alphabetic
        if not lang_code.isalpha():
            return False
        
        return True 