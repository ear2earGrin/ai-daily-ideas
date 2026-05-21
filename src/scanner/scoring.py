"""Scoring logic for pain points and opportunity clusters."""

from typing import List
from .models import PainPoint, OpportunityCluster


def score_pain_point(pain: PainPoint) -> PainPoint:
    """
    Calculate total score for a pain point.
    
    Scoring rubric (0-5 per factor):
    - Pain Intensity: 0=minor annoyance, 3=significant friction, 5=mission-critical
    - Frequency: 0=once a year, 3=monthly, 5=daily/hourly
    - Buyer Quality: 0=hobbyists, 3=freelancers, 5=SMBs/enterprises
    - Workaround Cost: 0=none, 3=manual but tolerable, 5=painful manual work
    - Existing Spend: 0=$0, 3=$10-50/mo, 5=$100+/mo
    - Reachability: 0=hard to find, 3=niche communities, 5=active communities
    - MVP Simplicity: 0=complex AI/ML, 3=standard CRUD, 5=no-code viable
    - Competition Gap: 0=saturated, 3=2-3 players, 5=no good solution
    
    Total range: 0-40
    Threshold for promotion: ≥25
    """
    pain.total_score = (
        pain.intensity +
        pain.frequency +
        pain.buyer_quality +
        pain.workaround_cost +
        pain.existing_spend +
        pain.reachability +
        pain.mvp_simplicity +
        pain.competition_gap
    )
    return pain


def score_cluster(cluster: OpportunityCluster) -> OpportunityCluster:
    """Calculate aggregate metrics for an opportunity cluster."""
    if not cluster.pain_points:
        cluster.avg_score = 0.0
        cluster.total_mentions = 0
        return cluster
    
    # Score each pain point if not already scored
    for pain in cluster.pain_points:
        if pain.total_score == 0:
            score_pain_point(pain)
    
    # Calculate cluster metrics
    cluster.total_mentions = len(cluster.pain_points)
    cluster.avg_score = sum(p.total_score for p in cluster.pain_points) / len(cluster.pain_points)
    
    return cluster


def rank_clusters(clusters: List[OpportunityCluster]) -> List[OpportunityCluster]:
    """Sort clusters by average score (descending)."""
    return sorted(clusters, key=lambda c: c.avg_score, reverse=True)
