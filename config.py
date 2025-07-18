"""
Configuration module for Google Play Review Scraper
"""

from datetime import datetime, timedelta
from typing import Optional


class Config:
    """Configuration class for Google Play review scraper"""
    
    # Default settings
    DEFAULT_MONTHS_BACK = 12  # Son 1 yıl
    DEFAULT_COUNTRY = "tr"
    DEFAULT_LANGUAGE = "tr"
    DEFAULT_SORT = "newest"  # newest, rating, helpfulness
    DEFAULT_COUNT = 1000  # Maximum reviews to fetch per request
    
    # File settings
    OUTPUT_DIR = "reviews"
    FILE_ENCODING = "utf-8"
    
    # Review fields to extract
    REVIEW_FIELDS = [
        "reviewId",
        "userName", 
        "userImage",
        "content",
        "score",
        "thumbsUpCount",
        "reviewCreatedVersion",
        "at",
        "replyContent",
        "repliedAt"
    ]
    
    @staticmethod
    def get_date_threshold(months_back: int = DEFAULT_MONTHS_BACK) -> datetime:
        """Get the date threshold for filtering reviews"""
        return datetime.now() - timedelta(days=months_back * 30)
    
    @staticmethod
    def get_output_filename(app_id: str, language: str) -> str:
        """Generate output filename based on app ID and language"""
        # com.sozlerkosku.beste5v2 -> com.sozlerkosku.beste5v2_tr.txt
        return f"{app_id}_{language}.txt" 