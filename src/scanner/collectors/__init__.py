"""Collectors for ingesting data from various sources."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen


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


class HackerNewsCollector:
    """Collect real Hacker News posts/comments via the public Algolia API."""

    api_url = "https://hn.algolia.com/api/v1/search_by_date"

    def __init__(self, query: str, limit: int = 20, tags: Optional[str] = None):
        self.query = query.strip()
        self.limit = max(1, min(int(limit), 100))
        self.tags = tags

    def collect(self) -> List[Dict[str, Any]]:
        if not self.query:
            raise ValueError("HackerNewsCollector requires a non-empty query")

        params = {
            "query": self.query,
            "hitsPerPage": self.limit,
        }
        if self.tags:
            params["tags"] = self.tags
        url = f"{self.api_url}?{urlencode(params)}"
        request = Request(url, headers={"User-Agent": "market-problem-scanner/0.2"})
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))

        sources: List[Dict[str, Any]] = []
        for hit in payload.get("hits", []):
            source = self._hit_to_source(hit)
            if source is not None:
                sources.append(source)
        return sources

    def _hit_to_source(self, hit: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        object_id = str(hit.get("objectID") or hit.get("story_id") or "").strip()
        if not object_id:
            return None

        title = (
            hit.get("title")
            or hit.get("story_title")
            or hit.get("comment_title")
            or "HN discussion"
        )
        text_parts = [
            title,
            hit.get("story_text") or "",
            hit.get("comment_text") or "",
        ]
        text = "\n\n".join(part.strip() for part in text_parts if isinstance(part, str) and part.strip())
        if not text:
            return None

        item_id = str(hit.get("story_id") or object_id)
        return {
            "url": f"https://news.ycombinator.com/item?id={item_id}",
            "type": "hn",
            "text": text,
            "metadata": {
                "synthetic": False,
                "query": self.query,
                "hn_object_id": object_id,
                "hn_story_id": item_id,
                "external_url": hit.get("url") or hit.get("story_url"),
                "points": hit.get("points"),
                "num_comments": hit.get("num_comments"),
                "created_at": hit.get("created_at"),
            },
        }


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
