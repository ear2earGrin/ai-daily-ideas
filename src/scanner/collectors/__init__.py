"""Collectors for ingesting data from various sources."""

import json
from pathlib import Path
from typing import List, Dict


class FixtureCollector:
    """
    Collect pain points from local JSON fixtures.
    
    This is a safe, no-credentials-required collector for the prototype.
    Real collectors (Reddit API, HN scraper) can be added later.
    """
    
    def __init__(self, fixture_path: str):
        self.fixture_path = Path(fixture_path)
    
    def collect(self) -> List[Dict[str, str]]:
        """
        Load fixture data.
        
        Expected format:
        {
            "sources": [
                {
                    "url": "https://example.com",
                    "type": "reddit",
                    "text": "I hate manually doing X...",
                    "metadata": {...}
                }
            ]
        }
        """
        if not self.fixture_path.exists():
            return []
        
        with open(self.fixture_path, 'r') as f:
            data = json.load(f)
        
        return data.get('sources', [])


class RedditCollector:
    """
    Reddit collector stub (requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET).
    
    To enable:
    1. Set environment variables:
       - REDDIT_CLIENT_ID
       - REDDIT_CLIENT_SECRET
       - REDDIT_USER_AGENT (optional)
    
    2. Install praw: pip install praw
    
    3. Use RedditCollector instead of FixtureCollector
    """
    
    def __init__(self, subreddit: str, limit: int = 10):
        import os
        
        self.subreddit = subreddit
        self.limit = limit
        
        # Check for credentials
        client_id = os.environ.get("REDDIT_CLIENT_ID")
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise RuntimeError(
                "Reddit API credentials not configured. "
                "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables, "
                "or use FixtureCollector instead."
            )
        
        try:
            import praw
        except ImportError:
            raise RuntimeError(
                "praw library not installed. Run: pip install praw"
            )
        
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=os.environ.get("REDDIT_USER_AGENT", "market-problem-scanner/0.1")
        )
    
    def collect(self) -> List[Dict[str, str]]:
        """Collect recent posts from a subreddit."""
        import time
        
        posts = []
        subreddit = self.reddit.subreddit(self.subreddit)
        
        for submission in subreddit.hot(limit=self.limit):
            time.sleep(1.0)  # Rate limiting
            
            posts.append({
                "url": f"https://reddit.com{submission.permalink}",
                "type": "reddit",
                "text": f"{submission.title}\n\n{submission.selftext}",
                "metadata": {
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "subreddit": self.subreddit,
                }
            })
        
        return posts
