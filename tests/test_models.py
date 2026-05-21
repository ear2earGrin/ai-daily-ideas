"""Tests for data models."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.models import PainPoint, OpportunityCluster


def test_pain_point_creation():
    """Test creating a basic pain point."""
    pain = PainPoint(
        source_url="https://example.com",
        quote="I hate doing X manually",
        audience="developers",
    )
    
    assert pain.id.startswith("pain_")
    assert pain.source_url == "https://example.com"
    assert pain.quote == "I hate doing X manually"
    assert pain.audience == "developers"
    assert pain.total_score == 0  # Not scored yet


def test_pain_point_serialization():
    """Test JSON serialization."""
    pain = PainPoint(
        source_url="https://example.com",
        quote="Test quote",
        audience="test audience",
        pain="test pain",
        intensity=4,
        frequency=5,
    )
    
    # To dict
    data = pain.to_dict()
    assert isinstance(data, dict)
    assert data['quote'] == "Test quote"
    assert data['intensity'] == 4
    
    # To JSON
    json_str = pain.to_json()
    assert isinstance(json_str, str)
    assert '"quote"' in json_str
    
    # From dict
    pain2 = PainPoint.from_dict(data)
    assert pain2.quote == pain.quote
    assert pain2.intensity == pain.intensity


def test_opportunity_cluster_creation():
    """Test creating an opportunity cluster."""
    pain1 = PainPoint(
        source_url="https://example.com/1",
        quote="Pain 1",
        audience="users",
    )
    pain2 = PainPoint(
        source_url="https://example.com/2",
        quote="Pain 2",
        audience="users",
    )
    
    cluster = OpportunityCluster(
        title="Test Cluster",
        pain_points=[pain1, pain2],
        domain="test",
    )
    
    assert cluster.id.startswith("opp_")
    assert cluster.title == "Test Cluster"
    assert len(cluster.pain_points) == 2
    assert cluster.domain == "test"


def test_opportunity_cluster_serialization():
    """Test cluster JSON serialization."""
    pain = PainPoint(
        source_url="https://example.com",
        quote="Test",
        audience="users",
    )
    
    cluster = OpportunityCluster(
        title="Test",
        pain_points=[pain],
    )
    
    # To dict
    data = cluster.to_dict()
    assert isinstance(data, dict)
    assert len(data['pain_points']) == 1
    
    # From dict
    cluster2 = OpportunityCluster.from_dict(data)
    assert cluster2.title == cluster.title
    assert len(cluster2.pain_points) == 1


if __name__ == "__main__":
    print("Running tests...")
    test_pain_point_creation()
    print("✓ test_pain_point_creation")
    
    test_pain_point_serialization()
    print("✓ test_pain_point_serialization")
    
    test_opportunity_cluster_creation()
    print("✓ test_opportunity_cluster_creation")
    
    test_opportunity_cluster_serialization()
    print("✓ test_opportunity_cluster_serialization")
    
    print("\nAll tests passed! ✓")
