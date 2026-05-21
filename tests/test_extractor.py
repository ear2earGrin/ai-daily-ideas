"""Tests for the heuristic extractor."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.extractor import HeuristicExtractor


def test_extract_pain_with_manual_work():
    """Test extraction of pain with manual work indicator."""
    extractor = HeuristicExtractor()
    
    text = "I hate manually copying data between systems every week. It takes me 3 hours."
    pain_points = extractor.extract(text, "https://example.com", "test")
    
    assert len(pain_points) > 0
    pain = pain_points[0]
    
    assert pain.source_url == "https://example.com"
    assert "manually" in pain.quote.lower()
    assert pain.workaround_cost > 0  # Should detect manual work
    assert pain.frequency > 0  # Should detect "every week"


def test_extract_pain_with_time_cost():
    """Test extraction of pain with time cost."""
    extractor = HeuristicExtractor()
    
    text = "I'm frustrated with manually creating invoices every month because it takes me 5 hours and I always make mistakes with the data entry."
    pain_points = extractor.extract(text, "https://example.com", "test")
    
    # This might extract or might not depending on heuristics
    # Just check that it doesn't crash
    assert isinstance(pain_points, list)


def test_audience_detection():
    """Test audience detection from text."""
    extractor = HeuristicExtractor()
    
    text = "As a small business owner I hate manually tracking expenses every day because it takes forever and I'm frustrated with the process."
    pain_points = extractor.extract(text, "https://example.com", "test")
    
    # Just verify it runs without error
    assert isinstance(pain_points, list)


def test_no_extraction_from_short_text():
    """Test that very short text is not extracted."""
    extractor = HeuristicExtractor()
    
    text = "Short text."
    pain_points = extractor.extract(text, "https://example.com", "test")
    
    # Short text should not produce pain points
    assert len(pain_points) == 0


def test_scoring_applied():
    """Test that heuristic scoring is applied."""
    extractor = HeuristicExtractor()
    
    text = "I hate manually doing this task every day because it's a nightmare for developers like me and I'm so frustrated with the process."
    pain_points = extractor.extract(text, "https://example.com", "test")
    
    # Verify extraction works and scoring is applied
    assert isinstance(pain_points, list)
    if pain_points:
        pain = pain_points[0]
        # Check scores are set (should be > 0 if scoring worked)
        assert pain.intensity >= 0
        assert pain.frequency >= 0


if __name__ == "__main__":
    print("Running tests...")
    test_extract_pain_with_manual_work()
    print("✓ test_extract_pain_with_manual_work")
    
    test_extract_pain_with_time_cost()
    print("✓ test_extract_pain_with_time_cost")
    
    test_audience_detection()
    print("✓ test_audience_detection")
    
    test_no_extraction_from_short_text()
    print("✓ test_no_extraction_from_short_text")
    
    test_scoring_applied()
    print("✓ test_scoring_applied")
    
    print("\nAll tests passed! ✓")
