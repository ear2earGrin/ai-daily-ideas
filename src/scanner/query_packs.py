"""Named search query packs for collecting real market-pain evidence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .collectors import HackerNewsCollector

DEFAULT_PACK_DIR = Path(__file__).resolve().parents[2] / "config" / "query_packs"


@dataclass
class QueryPack:
    name: str
    description: str
    queries: List[str]


def load_query_pack(name: str, pack_dir: Optional[Path] = None) -> QueryPack:
    """Load a named query pack from config/query_packs/<name>.json."""
    directory = Path(pack_dir) if pack_dir is not None else DEFAULT_PACK_DIR
    path = directory / f"{name}.json"
    if not path.exists():
        available = sorted(p.stem for p in directory.glob("*.json")) if directory.exists() else []
        suffix = f" Available packs: {', '.join(available)}" if available else " No query packs found."
        raise FileNotFoundError(f"Query pack not found: {path}.{suffix}")

    data = json.loads(path.read_text())
    queries = data.get("queries", [])
    if not isinstance(queries, list) or not all(isinstance(query, str) and query.strip() for query in queries):
        raise ValueError(f"Query pack {name} must contain a non-empty list of query strings")

    return QueryPack(
        name=data.get("name") or name,
        description=data.get("description") or "",
        queries=[query.strip() for query in queries],
    )


def collect_hn_pack(name: str, limit_per_query: int = 20, pack_dir: Optional[Path] = None) -> List[Dict]:
    """Collect HN results for every query in a pack, deduping by source URL."""
    pack = load_query_pack(name, pack_dir)
    sources: List[Dict] = []
    seen_urls = set()

    for query in pack.queries:
        for source in HackerNewsCollector(query=query, limit=limit_per_query).collect():
            url = source.get("url", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            metadata = dict(source.get("metadata") or {})
            metadata.update({"query_pack": pack.name, "query": query})
            source = dict(source)
            source["metadata"] = metadata
            sources.append(source)

    return sources
