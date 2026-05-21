"""Scoring logic for pain points and opportunity clusters."""

from typing import List
from .models import PainPoint, OpportunityCluster


def _clamp_score(value: int) -> int:
    return max(0, min(5, int(value)))


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
        score_opportunity_ranking(cluster)
        return cluster
    
    # Score each pain point if not already scored
    for pain in cluster.pain_points:
        if pain.total_score == 0:
            score_pain_point(pain)
    
    # Calculate cluster metrics
    cluster.total_mentions = len(cluster.pain_points)
    cluster.avg_score = sum(p.total_score for p in cluster.pain_points) / len(cluster.pain_points)
    score_opportunity_ranking(cluster)
    
    return cluster


def score_opportunity_ranking(cluster: OpportunityCluster) -> OpportunityCluster:
    """Score an opportunity on money potential and probability to ship.

    The final priority score intentionally multiplies the two axes. That punishes
    sexy-but-hard ideas and easy-but-worthless ideas, which is the point for a
    solo-builder queue.
    """
    if not cluster.pain_points:
        cluster.profitability_score = 0
        cluster.build_probability_score = 0
        cluster.priority_score = 0
        cluster.priority_band = "ignore"
        cluster.buyer_type = cluster.audience or "unknown"
        cluster.monetization_guess = "missing pain evidence"
        cluster.mvp_shape = "collect evidence before building"
        cluster.risk_notes = "no source-backed pain points"
        cluster.missing_data = "pain evidence, buyer budget, current workaround, distribution channel"
        cluster.next_validation_step = "Collect at least 5 source-backed pain points before scoring."
        return cluster

    for pain in cluster.pain_points:
        if pain.total_score == 0:
            score_pain_point(pain)

    count = len(cluster.pain_points)
    avg = lambda attr: round(sum(_clamp_score(getattr(p, attr)) for p in cluster.pain_points) / count)

    intensity = avg("intensity")
    frequency = avg("frequency")
    buyer_quality = avg("buyer_quality")
    workaround_cost = avg("workaround_cost")
    existing_spend = avg("existing_spend")
    reachability = avg("reachability")
    mvp_simplicity = avg("mvp_simplicity")
    competition_gap = avg("competition_gap")

    revenue_model_clarity = max(existing_spend, buyer_quality)
    automation_fit = max(intensity, workaround_cost)
    low_compliance_risk = _infer_low_compliance_risk(cluster)
    low_maintenance_burden = mvp_simplicity
    founder_fit = 3  # neutral default until the user manually marks strategic fit

    cluster.profitability_score = (
        intensity
        + buyer_quality
        + existing_spend
        + frequency
        + reachability
        + revenue_model_clarity
        + workaround_cost
    )
    cluster.build_probability_score = (
        mvp_simplicity
        + reachability
        + competition_gap
        + low_compliance_risk
        + low_maintenance_burden
        + automation_fit
        + founder_fit
    )
    cluster.priority_score = cluster.profitability_score * cluster.build_probability_score
    cluster.priority_band = _priority_band(cluster.priority_score)
    cluster.buyer_type = cluster.audience or _most_common_nonempty([p.audience for p in cluster.pain_points]) or "unknown"
    cluster.monetization_guess = _monetization_guess(cluster, buyer_quality, existing_spend)
    cluster.mvp_shape = _mvp_shape(cluster, mvp_simplicity)
    cluster.risk_notes = _risk_notes(cluster, low_compliance_risk, competition_gap)
    cluster.missing_data = _missing_data(cluster, existing_spend, reachability, competition_gap)
    cluster.next_validation_step = _next_validation_step(cluster)
    return cluster


def rank_clusters(clusters: List[OpportunityCluster]) -> List[OpportunityCluster]:
    """Sort clusters by priority score, then average evidence score.

    Empty clusters keep any precomputed avg_score for backwards-compatible tests
    and imported historical data.
    """
    for cluster in clusters:
        if cluster.pain_points:
            score_cluster(cluster)
        elif cluster.priority_score == 0 and cluster.avg_score == 0:
            score_opportunity_ranking(cluster)
    return sorted(
        clusters,
        key=lambda c: (c.priority_score, c.profitability_score, c.avg_score, c.total_mentions),
        reverse=True,
    )


def _priority_band(priority_score: int) -> str:
    if priority_score >= 900:
        return "validate immediately"
    if priority_score >= 650:
        return "promising"
    if priority_score >= 400:
        return "keep watching"
    return "ignore"


def _infer_low_compliance_risk(cluster: OpportunityCluster) -> int:
    text = " ".join(
        [cluster.title, cluster.domain, cluster.audience]
        + [p.pain for p in cluster.pain_points]
        + [p.quote for p in cluster.pain_points]
    ).lower()
    high_risk = ["legal", "law", "tax", "medical", "health", "therapy", "bank", "insurance"]
    medium_risk = ["payment", "payroll", "contract"]
    if any(term in text for term in high_risk):
        return 2
    if any(term in text for term in medium_risk):
        return 4
    return 5


def _most_common_nonempty(values: List[str]) -> str:
    counts = {}
    for value in values:
        value = (value or "").strip()
        if value:
            counts[value] = counts.get(value, 0) + 1
    if not counts:
        return ""
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)[0][0]


def _monetization_guess(cluster: OpportunityCluster, buyer_quality: int, existing_spend: int) -> str:
    if buyer_quality >= 4 or existing_spend >= 4:
        return "$49-199/mo or $500-2k setup for a focused workflow MVP"
    if buyer_quality >= 3 or existing_spend >= 2:
        return "$19-79/mo subscription or $200-500 setup after manual validation"
    return "low-ticket or lead magnet unless stronger buyer-budget evidence appears"


def _mvp_shape(cluster: OpportunityCluster, mvp_simplicity: int) -> str:
    if mvp_simplicity >= 4:
        return "48-hour concierge MVP: spreadsheet/SQLite intake, one automation, simple dashboard, manual QA"
    if mvp_simplicity >= 3:
        return "1-week prototype: narrow workflow, manual back office, simple UI around the painful step"
    return "research spike first: validate APIs/data access before building product UI"


def _risk_notes(cluster: OpportunityCluster, low_compliance_risk: int, competition_gap: int) -> str:
    risks = []
    if low_compliance_risk <= 2:
        risks.append("regulated/legal/finance/health-adjacent claims need conservative scope")
    if competition_gap <= 2:
        risks.append("crowded market means positioning or niche wedge must be sharper")
    if cluster.total_mentions < 3:
        risks.append("thin evidence set; do not build before finding more examples")
    return "; ".join(risks) or "low obvious risk from current evidence; still validate willingness to pay"


def _missing_data(cluster: OpportunityCluster, existing_spend: int, reachability: int, competition_gap: int) -> str:
    missing = []
    if existing_spend < 3:
        missing.append("buyer budget/current spend")
    if reachability < 3:
        missing.append("cheap distribution channel")
    if competition_gap < 3:
        missing.append("clear wedge against existing tools")
    if cluster.total_mentions < 5:
        missing.append("more repeated public evidence")
    return ", ".join(missing) or "none obvious from current scoring"


def _next_validation_step(cluster: OpportunityCluster) -> str:
    return (
        "Find 10 more public posts from the same buyer type, identify 3 paid alternatives, "
        "then draft a 48-hour concierge MVP offer before writing more product code."
    )
