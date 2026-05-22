"""Tests for loading and collecting query packs."""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.query_packs import collect_hn_pack, load_query_pack


def test_load_query_pack_reads_named_pack_and_query_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        pack_dir = Path(tmp)
        (pack_dir / "finance-admin.json").write_text(json.dumps({
            "name": "finance-admin",
            "description": "Finance admin pains",
            "queries": ["manual invoice", "spreadsheet bookkeeping"],
        }))

        pack = load_query_pack("finance-admin", pack_dir=pack_dir)

        assert pack.name == "finance-admin"
        assert pack.description == "Finance admin pains"
        assert pack.queries == ["manual invoice", "spreadsheet bookkeeping"]


def test_collect_hn_pack_dedupes_urls_and_keeps_query_provenance():
    calls = []

    class FakeCollector:
        def __init__(self, query, limit):
            self.query = query
            self.limit = limit

        def collect(self):
            calls.append((self.query, self.limit))
            return [
                {"url": "https://news.ycombinator.com/item?id=1", "type": "hn", "text": f"same post for {self.query}"},
                {"url": f"https://news.ycombinator.com/item?id={len(calls) + 1}", "type": "hn", "text": f"unique post for {self.query}"},
            ]

    with tempfile.TemporaryDirectory() as tmp:
        pack_dir = Path(tmp)
        (pack_dir / "ops.json").write_text(json.dumps({"queries": ["manual invoice", "manual spreadsheet"]}))

        with patch("scanner.query_packs.HackerNewsCollector", FakeCollector):
            sources = collect_hn_pack("ops", limit_per_query=3, pack_dir=pack_dir)

    assert calls == [("manual invoice", 3), ("manual spreadsheet", 3)]
    assert [source["url"] for source in sources] == [
        "https://news.ycombinator.com/item?id=1",
        "https://news.ycombinator.com/item?id=2",
        "https://news.ycombinator.com/item?id=3",
    ]
    assert sources[0]["metadata"]["query_pack"] == "ops"
    assert sources[0]["metadata"]["query"] == "manual invoice"


if __name__ == "__main__":
    print("Running tests...")
    test_load_query_pack_reads_named_pack_and_query_metadata()
    print("✓ test_load_query_pack_reads_named_pack_and_query_metadata")
    test_collect_hn_pack_dedupes_urls_and_keeps_query_provenance()
    print("✓ test_collect_hn_pack_dedupes_urls_and_keeps_query_provenance")
    print("\nAll tests passed! ✓")
