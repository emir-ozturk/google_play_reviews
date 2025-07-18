#!/usr/bin/env python3
"""
Google Play Review Scraper - Main Script
Usage: python main.py <app_id> <language> [months_back] [max_reviews]
Example: python main.py com.sozlerkosku.beste5v2 tr 12 1000
"""

import sys
import argparse
from datetime import datetime
from scraper import GooglePlayReviewScraper
from config import Config


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Google Play Review Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py com.sozlerkosku.beste5v2 tr
  python main.py com.sozlerkosku.beste5v2 tr --months 6
  python main.py com.sozlerkosku.beste5v2 tr --months 12 --count 2000
  python main.py com.sozlerkosku.beste5v2 tr --months 24 --count 500 --no-json
        """
    )
    
    parser.add_argument(
        'app_id',
        help='Google Play app ID (e.g., com.sozlerkosku.beste5v2)'
    )
    
    parser.add_argument(
        'language',
        help='Language code (e.g., tr, en, de)'
    )
    
    parser.add_argument(
        '--months',
        type=int,
        default=Config.DEFAULT_MONTHS_BACK,
        help=f'Number of months to go back (default: {Config.DEFAULT_MONTHS_BACK})'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=Config.DEFAULT_COUNT,
        help=f'Maximum number of reviews to fetch (default: {Config.DEFAULT_COUNT})'
    )
    
    parser.add_argument(
        '--country',
        default=Config.DEFAULT_COUNTRY,
        help=f'Country code (default: {Config.DEFAULT_COUNTRY})'
    )
    
    parser.add_argument(
        '--no-json',
        action='store_true',
        help='Skip saving JSON backup file'
    )
    
    parser.add_argument(
        '--stats-only',
        action='store_true',
        help='Only show statistics without saving files'
    )
    
    return parser.parse_args()


def main():
    """Main function"""
    print("Google Play Review Scraper")
    print("=" * 40)
    
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Validate inputs
        if args.months <= 0:
            print("Error: months must be positive")
            sys.exit(1)
        
        if args.count <= 0:
            print("Error: count must be positive")
            sys.exit(1)
        
        # Initialize scraper
        scraper = GooglePlayReviewScraper(
            app_id=args.app_id,
            language=args.language,
            country=args.country
        )
        
        # Scrape reviews
        reviews = scraper.scrape_reviews(
            months_back=args.months,
            count=args.count
        )
        
        if not reviews:
            print("No reviews found matching the criteria.")
            return
        
        # Get and display statistics
        stats = scraper.get_review_stats(reviews)
        scraper.print_stats(stats)
        
        # Save files unless stats-only mode
        if not args.stats_only:
            txt_file, json_file = scraper.export_reviews(
                reviews, 
                save_json=not args.no_json
            )
            
            print(f"\nFiles saved:")
            print(f"  Text file: reviews/{txt_file}")
            if json_file:
                print(f"  JSON file: reviews/{json_file}")
        
        print("\nScraping completed successfully!")
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
        sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def interactive_mode():
    """Interactive mode for easier usage"""
    print("Google Play Review Scraper - Interactive Mode")
    print("=" * 50)
    
    try:
        # Get app ID
        app_id = input("Enter Google Play app ID (e.g., com.sozlerkosku.beste5v2): ").strip()
        if not app_id:
            print("App ID is required!")
            return
        
        # Get language
        language = input(f"Enter language code (default: {Config.DEFAULT_LANGUAGE}): ").strip()
        if not language:
            language = Config.DEFAULT_LANGUAGE
        
        # Get country
        country = input(f"Enter country code (default: {Config.DEFAULT_COUNTRY}): ").strip()
        if not country:
            country = Config.DEFAULT_COUNTRY
        
        # Get months back
        months_input = input(f"Enter months to go back (default: {Config.DEFAULT_MONTHS_BACK}): ").strip()
        months_back = int(months_input) if months_input.isdigit() else Config.DEFAULT_MONTHS_BACK
        
        # Get max reviews
        count_input = input(f"Enter maximum reviews to fetch (default: {Config.DEFAULT_COUNT}): ").strip()
        count = int(count_input) if count_input.isdigit() else Config.DEFAULT_COUNT
        
        # Save JSON?
        save_json_input = input("Save JSON backup? (y/n, default: y): ").strip().lower()
        save_json = save_json_input != 'n'
        
        print(f"\nStarting scraper with:")
        print(f"  App ID: {app_id}")
        print(f"  Language: {language}")
        print(f"  Country: {country}")
        print(f"  Months back: {months_back}")
        print(f"  Max reviews: {count}")
        print(f"  Save JSON: {save_json}")
        print()
        
        # Initialize and run scraper
        scraper = GooglePlayReviewScraper(
            app_id=app_id,
            language=language,
            country=country
        )
        
        reviews = scraper.scrape_reviews(
            months_back=months_back,
            count=count
        )
        
        if not reviews:
            print("No reviews found matching the criteria.")
            return
        
        # Show stats
        stats = scraper.get_review_stats(reviews)
        scraper.print_stats(stats)
        
        # Save files
        txt_file, json_file = scraper.export_reviews(reviews, save_json=save_json)
        
        print(f"\nFiles saved:")
        print(f"  Text file: reviews/{txt_file}")
        if json_file:
            print(f"  JSON file: reviews/{json_file}")
        
        print("\nScraping completed successfully!")
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, run interactive mode
        interactive_mode()
    else:
        # Arguments provided, run with command line arguments
        main() 