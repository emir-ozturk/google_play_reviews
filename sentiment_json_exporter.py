#!/usr/bin/env python3
"""
Export Google Play reviews as compact JSON filtered by sentiment.

Usage:
  python sentiment_json_exporter.py <app_id> <language> <sentiment> <count>

Example:
  python sentiment_json_exporter.py com.sozlerkosku.beste5v2 tr olumlu 200
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from google_play_scraper import Sort, reviews


SENTIMENT_RANGES = {
    "olumlu": {4, 5},
    "olumsuz": {1, 2},
    "notr": {3},
}


def parse_arguments() -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Export Google Play reviews to JSON by sentiment."
    )
    parser.add_argument("app_id", help="Google Play app id (e.g. com.example.app)")
    parser.add_argument("language", help="Language code (e.g. tr, en)")
    parser.add_argument(
        "sentiment",
        choices=tuple(SENTIMENT_RANGES.keys()),
        help="Sentiment filter: olumlu (4-5), olumsuz (1-2), notr (3)",
    )
    parser.add_argument(
        "count",
        type=int,
        help="How many filtered reviews should be exported",
    )
    parser.add_argument(
        "--country",
        default="tr",
        help="Country code for Google Play query (default: tr)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON file path (default: reviews/<app_id>_<language>_<sentiment>.json)",
    )
    args = parser.parse_args()

    if args.count <= 0:
        parser.error("count must be a positive integer")

    return args


def build_default_output_path(app_id: str, language: str, sentiment: str) -> Path:
    """Create default output path for the JSON file."""
    safe_app_id = app_id.replace(".", "_")
    file_name = f"{safe_app_id}_{language}_{sentiment}.json"
    return Path("reviews") / file_name


def filter_review_fields(review: Dict[str, Any]) -> Dict[str, Any]:
    """Keep only the requested fields in output."""
    return {
        "content": review.get("content", ""),
        "score": review.get("score", 0),
        "thumbsUpCount": review.get("thumbsUpCount", 0),
    }


def fetch_filtered_reviews(
    app_id: str,
    language: str,
    country: str,
    sentiment: str,
    target_count: int,
) -> List[Dict[str, Any]]:
    """Fetch reviews incrementally until filtered target_count is reached."""
    allowed_scores = SENTIMENT_RANGES[sentiment]
    filtered: List[Dict[str, Any]] = []
    continuation_token: Optional[str] = None
    page_size = min(max(target_count * 2, 100), 200)
    max_rounds = 50
    rounds = 0

    while len(filtered) < target_count and rounds < max_rounds:
        rounds += 1
        batch_reviews, continuation_token = reviews(
            app_id,
            lang=language,
            country=country,
            sort=Sort.NEWEST,
            count=page_size,
            continuation_token=continuation_token,
        )

        if not batch_reviews:
            break

        for review in batch_reviews:
            if review.get("score") in allowed_scores:
                filtered.append(filter_review_fields(review))
                if len(filtered) >= target_count:
                    break

        if continuation_token is None:
            break

    return filtered[:target_count]


def write_json_file(path: Path, payload: List[Dict[str, Any]]) -> None:
    """Write payload to UTF-8 JSON file with pretty format."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def main() -> int:
    """Run CLI workflow."""
    args = parse_arguments()
    output_path = Path(args.output) if args.output else build_default_output_path(
        args.app_id, args.language, args.sentiment
    )

    try:
        filtered_reviews = fetch_filtered_reviews(
            app_id=args.app_id,
            language=args.language,
            country=args.country,
            sentiment=args.sentiment,
            target_count=args.count,
        )
    except Exception as exc:  # pragma: no cover
        print(f"Error while fetching reviews: {exc}", file=sys.stderr)
        return 1

    if not filtered_reviews:
        print("No reviews found for the given filter.")
        return 0

    try:
        write_json_file(output_path, filtered_reviews)
    except OSError as exc:
        print(f"Failed to write JSON file: {exc}", file=sys.stderr)
        return 1

    print(f"Saved {len(filtered_reviews)} reviews to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
