"""Tests for scoring logic."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.models import PainPoint, OpportunityCluster
from scanner.scoring import score_pain_point, score_cluster, rank_clusters


def test_score_pain_point():
    """Test scoring a pain point."""
    pain = PainPoint(
        source_url="https://example.com",
        quote="I spend 2 hours every week manually syncing data",
        audience="small business owners",
        pain="manual data sync",
        intensity=4,
        frequency=5,
        buyer_quality=4,
        workaround_cost=4,
        existing_spend=3,
        reachability=4,
        mvp_simplicity=3,
        competition_gap=3,
    )
    
    scored = score_pain_point(pain)
    assert scored.total_score == 30  # Sum of all factors
    assert scored.total_score > 0
    assert scored.total_score <= 40


def test_score_cluster():
    """Test scoring an opportunity cluster."""
    pain1 = PainPoint(
        source_url="https://example.com/1",
        quote="Pain 1",
        audience="users",
        intensity=4,
        frequency=5,
        buyer_quality=4,
        workaround_cost=3,
        existing_spend=3,
        reachability=4,
        mvp_simplicity=3,
        competition_gap=2,
    )
    pain2 = PainPoint(
        source_url="https://example.com/2",
        quote="Pain 2",
        audience="users",
        intensity=3,
        frequency=4,
        buyer_quality=3,
        workaround_cost=3,
        existing_spend=2,
        reachability=3,
        mvp_simplicity=3,
        competition_gap=3,
    )
    
    cluster = OpportunityCluster(
        title="Test Cluster",
        pain_points=[pain1, pain2],
    )
    
    scored = score_cluster(cluster)
    
    assert scored.total_mentions == 2
    assert scored.avg_score > 0
    assert scored.avg_score <= 40
    # pain1 = 28, pain2 = 24, avg = 26
    assert scored.avg_score == 26.0


def test_rank_clusters():
    """Test ranking clusters by score."""
    cluster1 = OpportunityCluster(
        title="Low Score",
        pain_points=[],
        avg_score=15.0,
    )
    cluster2 = OpportunityCluster(
        title="High Score",
        pain_points=[],
        avg_score=30.0,
    )
    cluster3 = OpportunityCluster(
        title="Medium Score",
        pain_points=[],
        avg_score=22.0,
    )
    
    ranked = rank_clusters([cluster1, cluster2, cluster3])
    
    assert len(ranked) == 3
    assert ranked[0].title == "High Score"
    assert ranked[1].title == "Medium Score"
    assert ranked[2].title == "Low Score"


if __name__ == "__main__":
    print("Running tests...")
    test_score_pain_point()
    print("✓ test_score_pain_point")
    
    test_score_cluster()
    print("✓ test_score_cluster")
    
    test_rank_clusters()
    print("✓ test_rank_clusters")
    
    print("\nAll tests passed! ✓")
