"""Tests for structured LLM/command extraction."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.extractor import StructuredExtractor


class FakeRunner:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def __call__(self, command, prompt):
        self.calls.append((command, prompt))
        return json.dumps(self.payload)


def test_structured_extractor_maps_json_pain_points_and_scores_them():
    payload = {
        "pain_points": [
            {
                "quote": "Every week I copy invoices from email into a spreadsheet by hand.",
                "pain": "manual invoice entry",
                "audience": "freelancers",
                "workaround": "spreadsheet",
                "existing_tools": ["Excel"],
                "confidence": "high",
            }
        ]
    }
    runner = FakeRunner(payload)

    extractor = StructuredExtractor(command="fake-llm", runner=runner)
    pains = extractor.extract(
        "HN post about painful invoice workflows",
        source_url="https://news.ycombinator.com/item?id=123",
        source_type="hn",
    )

    assert len(pains) == 1
    pain = pains[0]
    assert pain.source_url == "https://news.ycombinator.com/item?id=123"
    assert pain.source_type == "hn"
    assert pain.quote == "Every week I copy invoices from email into a spreadsheet by hand."
    assert pain.pain == "manual invoice entry"
    assert pain.audience == "freelancers"
    assert pain.workaround == "spreadsheet"
    assert pain.existing_tools == ["Excel"]
    assert pain.confidence == "high"
    assert pain.processed_by == "structured-extractor-v1"
    assert pain.total_score > 0
    assert runner.calls
    assert "Return strict JSON" in runner.calls[0][1]


def test_structured_extractor_rejects_empty_or_invalid_items():
    payload = {
        "pain_points": [
            {"quote": "too short", "pain": "x", "audience": ""},
            {"quote": "This quote is long enough but has no useful pain", "pain": "", "audience": "users"},
        ]
    }

    extractor = StructuredExtractor(command="fake-llm", runner=FakeRunner(payload))
    assert extractor.extract("source text", "https://news.ycombinator.com/item?id=1", "hn") == []


if __name__ == "__main__":
    print("Running tests...")
    test_structured_extractor_maps_json_pain_points_and_scores_them()
    print("✓ test_structured_extractor_maps_json_pain_points_and_scores_them")
    test_structured_extractor_rejects_empty_or_invalid_items()
    print("✓ test_structured_extractor_rejects_empty_or_invalid_items")
    print("\nAll tests passed! ✓")
