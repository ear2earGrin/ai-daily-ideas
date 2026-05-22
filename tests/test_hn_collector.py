"""Tests for Hacker News live collector mapping."""

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.collectors import HackerNewsCollector


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self.payload


def test_hn_collector_maps_algolia_hits_to_real_item_urls():
    payload = b'''
    {
      "hits": [
        {
          "objectID": "12345",
          "title": "Ask HN: Manual invoice pain",
          "story_text": "I spend hours manually creating invoices from time logs.",
          "url": null,
          "points": 42,
          "num_comments": 17,
          "created_at": "2026-05-20T10:00:00Z"
        },
        {
          "objectID": "67890",
          "story_title": "Show HN: Spreadsheet sync",
          "comment_text": "Manual spreadsheet syncing is painful and error-prone.",
          "story_id": 67890,
          "story_url": "https://example.com/spreadsheet-sync",
          "points": null,
          "num_comments": null,
          "created_at": "2026-05-21T10:00:00Z"
        }
      ]
    }
    '''

    requested = {}

    def fake_urlopen(request, timeout=0):
        requested["url"] = request.full_url
        return FakeResponse(payload)

    with patch("scanner.collectors.urlopen", fake_urlopen):
        sources = HackerNewsCollector(query="manual invoice", limit=2).collect()

    assert "hn.algolia.com/api/v1/search_by_date" in requested["url"]
    assert "manual+invoice" in requested["url"]
    assert len(sources) == 2
    assert sources[0]["url"] == "https://news.ycombinator.com/item?id=12345"
    assert sources[0]["type"] == "hn"
    assert sources[0]["metadata"]["synthetic"] is False
    assert sources[0]["metadata"]["hn_object_id"] == "12345"
    assert "Manual invoice pain" in sources[0]["text"]
    assert "manually creating invoices" in sources[0]["text"]
    assert sources[1]["url"] == "https://news.ycombinator.com/item?id=67890"
    assert sources[1]["metadata"]["external_url"] == "https://example.com/spreadsheet-sync"


if __name__ == "__main__":
    print("Running tests...")
    test_hn_collector_maps_algolia_hits_to_real_item_urls()
    print("✓ test_hn_collector_maps_algolia_hits_to_real_item_urls")
    print("\nAll tests passed! ✓")
