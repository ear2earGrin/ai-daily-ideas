"""Build named opportunity clusters from extracted pain points."""

import re
from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

from .models import OpportunityCluster, PainPoint
from .scoring import score_cluster

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "get", "getting",
    "i", "in", "into", "it", "keep", "manually", "manual", "me", "my", "of", "on", "or",
    "our", "the", "their", "there", "this", "to", "too", "up", "using", "with", "without", "work", "workflow", "every",
    "week", "weekly", "pain", "problem", "process", "task", "tasks", "wish", "simple", "tool",
    "could", "would", "lack", "solution", "paying", "paid", "dealing", "hours", "hour", "month",
    "months", "places", "stuff", "thing", "things", "good", "all",
}

DOMAIN_KEYWORDS = [
    ("finance-ops", {"invoice", "invoices", "billing", "bookkeeping", "payment", "payments", "receipt", "receipts", "accounting", "tax", "expense", "expenses"}),
    ("sales-ops", {"crm", "lead", "leads", "sales", "pipeline", "prospect", "outreach"}),
    ("support-ops", {"support", "ticket", "tickets", "customer", "customers", "helpdesk"}),
    ("devtools", {"screenshot", "screenshots", "release", "deploy", "deployment", "docs", "documentation", "api", "code"}),
    ("legal-ops", {"contract", "contracts", "compliance", "legal", "policy", "policies"}),
    ("marketing-ops", {"content", "seo", "ads", "campaign", "campaigns", "social"}),
]

CANONICAL_TERMS = {
    "invoices": "invoice",
    "payments": "payment",
    "receipts": "receipt",
    "spreadsheets": "spreadsheet",
    "screenshots": "screenshot",
    "syncing": "sync",
    "tracking": "track",
    "expenses": "expense",
    "logs": "log",
    "auto-generate": "generate",
    "developers": "developer",
    "freelancers": "freelancer",
    "agencies": "agency",
    "founders": "founder",
    "customers": "customer",
    "tickets": "ticket",
    "docs": "doc",
}

AUDIENCE_LABELS = {
    "freelancers": "Freelancer",
    "freelancer": "Freelancer",
    "developers": "Developer",
    "developer": "Developer",
    "agencies": "Agency",
    "agency": "Agency",
    "founders": "Founder",
    "founder": "Founder",
    "small businesses": "Small business",
    "small business": "Small business",
    "builders": "Builder",
}


def normalize_word(word: str) -> str:
    word = re.sub(r"[^a-z0-9-]", "", word.lower())
    return CANONICAL_TERMS.get(word, word)


def pain_tokens(pain: PainPoint) -> List[str]:
    text = f"{pain.pain} {pain.quote}".lower()
    words = [normalize_word(w) for w in re.findall(r"[a-z0-9-]+", text)]
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


def infer_domain(pains: Iterable[PainPoint]) -> str:
    counts: Dict[str, int] = defaultdict(int)
    for pain in pains:
        tokens = set(pain_tokens(pain))
        for domain, keywords in DOMAIN_KEYWORDS:
            counts[domain] += len(tokens & keywords)
    if counts:
        domain, count = max(counts.items(), key=lambda item: item[1])
        if count > 0:
            return domain
    return "workflow-automation"


def infer_audience(pains: Iterable[PainPoint]) -> str:
    counts: Dict[str, int] = defaultdict(int)
    for pain in pains:
        audience = (pain.audience or "").strip().lower()
        if audience:
            counts[audience] += 1
    if counts:
        return max(counts.items(), key=lambda item: item[1])[0]
    return "general users"


def audience_label(audience: str) -> str:
    normalized = (audience or "").strip().lower()
    return AUDIENCE_LABELS.get(normalized, normalized[:1].upper() + normalized[1:] if normalized else "User")


def title_terms_for_pains(pains: List[PainPoint]) -> List[str]:
    text = " ".join(f"{pain.pain} {pain.quote}" for pain in pains).lower()
    tokens = set()
    for pain in pains:
        tokens.update(pain_tokens(pain))

    if {"inventory", "shopify"} & tokens:
        return ["inventory", "sync"]
    if "invoice" in tokens and ({"time", "log"} & tokens):
        return ["invoice", "time-log"]
    if "invoice" in tokens and "spreadsheet" in tokens:
        return ["invoice", "spreadsheet"]
    if "crm" in tokens or "salesforce" in tokens or "follow-up" in text or "follow" in tokens:
        return ["CRM", "follow-up"]
    if "travel" in tokens and "expense" in tokens:
        return ["travel", "expense"]
    if "expense" in tokens:
        return ["expense", "tracking"]
    if "screenshot" in tokens:
        return ["screenshot", "update"]
    return []


def synthesize_opportunity_title(pains: List[PainPoint]) -> str:
    """Create a specific, human-readable opportunity title from evidence."""
    if not pains:
        return "Workflow automation opportunity"

    audience = audience_label(infer_audience(pains))
    known_terms = title_terms_for_pains(pains)
    if known_terms:
        return f"{audience} {' '.join(known_terms)} automation"

    tokens = []
    for pain in pains:
        tokens.extend(pain_tokens(pain))

    token_counts: Dict[str, int] = defaultdict(int)
    for token in tokens:
        token_counts[token] += 1

    ranked = [token for token, _ in sorted(token_counts.items(), key=lambda item: (-item[1], item[0]))]

    # Prefer noun-ish workflow objects over generic action words.
    preferred = [
        token for token in ranked
        if token not in {"copy", "copying", "update", "updating", "entry", "automation", "automate", "hour", "hours", "dealing"}
    ]
    action_terms = [token for token in ranked if token in {"copy", "copying", "update", "updating", "entry"}]

    core_terms = preferred[:2]
    if "invoice" in ranked and "spreadsheet" in ranked:
        core_terms = ["invoice", "spreadsheet"]
    elif "screenshot" in ranked:
        core_terms = ["screenshot", "update"]
    elif len(core_terms) == 1 and action_terms:
        core_terms.append(action_terms[0])

    if not core_terms:
        core_terms = ["workflow"]

    return f"{audience} {' '.join(core_terms)} automation"


def cluster_key(pain: PainPoint) -> Tuple[str, str, str]:
    domain = infer_domain([pain])
    tokens = set(pain_tokens(pain))
    if "invoice" in tokens or "billing" in tokens:
        theme = "invoice"
    elif "inventory" in tokens or "shopify" in tokens:
        theme = "inventory"
    elif "crm" in tokens or "salesforce" in tokens or "follow" in tokens:
        theme = "crm-follow-up"
    elif "travel" in tokens and "expense" in tokens:
        theme = "travel-expense"
    elif "expense" in tokens:
        theme = "expense"
    elif "screenshot" in tokens:
        theme = "screenshot"
    elif "spreadsheet" in tokens:
        theme = "spreadsheet"
    elif tokens:
        theme = sorted(tokens)[0]
    else:
        theme = "workflow"
    return (domain, infer_audience([pain]), theme)


def build_opportunity_clusters(pain_points: List[PainPoint], source_label: str = "sources") -> List[OpportunityCluster]:
    """Group pain points into named opportunity clusters."""
    grouped: Dict[Tuple[str, str, str], List[PainPoint]] = defaultdict(list)
    for pain in pain_points:
        grouped[cluster_key(pain)].append(pain)

    clusters = []
    for (_domain, _audience, _theme), pains in grouped.items():
        title = synthesize_opportunity_title(pains)
        domain = infer_domain(pains)
        audience = infer_audience(pains)
        total_mentions = len(pains)
        cluster = OpportunityCluster(
            title=title,
            pain_points=pains,
            domain=domain,
            audience=audience,
            total_mentions=total_mentions,
            executive_summary=(
                f"{total_mentions} public evidence post{'s' if total_mentions != 1 else ''} point to "
                f"{title.lower()} from {source_label}."
            ),
        )
        score_cluster(cluster)
        clusters.append(cluster)

    return sorted(clusters, key=lambda cluster: (cluster.avg_score, cluster.total_mentions), reverse=True)
