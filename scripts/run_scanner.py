#!/usr/bin/env python3
"""
Market Problem Scanner CLI

Prototype entry point for discovering monetizable pain points.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scanner.collectors import FixtureCollector, HackerNewsCollector
from scanner.extractor import HeuristicExtractor, StructuredExtractor
from scanner.opportunity_builder import build_opportunity_clusters
from scanner.query_packs import collect_hn_pack
from scanner.scoring import score_pain_point, rank_clusters
from scanner.reporter import generate_report
from scanner.storage import PainPointStorage, ClusterStorage
from scanner.sqlite_storage import ScannerDatabase


def make_extractor(mode: str, llm_command: Optional[str] = None):
    if mode == "structured":
        if not llm_command:
            raise ValueError("--extractor structured requires --llm-command")
        return StructuredExtractor(llm_command)
    if mode == "heuristic":
        return HeuristicExtractor()
    raise ValueError("extractor must be heuristic or structured")


def scan_sources(
    sources,
    source_label: str,
    output_dir: str = "reports",
    db_path: Optional[str] = None,
    extractor_mode: str = "heuristic",
    llm_command: Optional[str] = None,
) -> str:
    """Run extraction/scoring/reporting for collected source dictionaries."""
    print(f"📊 Market Problem Scanner v0.5.0")
    print(f"📁 Source: {source_label}")
    print(f"✅ Loaded {len(sources)} source(s)")
    
    # Extract pain points
    extractor = make_extractor(extractor_mode, llm_command)
    print(f"🧠 Extractor: {extractor_mode}")
    all_pain_points = []
    
    for source in sources:
        text = source.get('text', '')
        url = source.get('url', '')
        source_type = source.get('type', 'text')
        
        pain_points = extractor.extract(text, url, source_type)
        all_pain_points.extend(pain_points)
    
    print(f"✅ Extracted {len(all_pain_points)} pain point(s)")
    
    # Score pain points
    for pain in all_pain_points:
        score_pain_point(pain)
    
    # Build named opportunity clusters from related pain points.
    clusters = build_opportunity_clusters(all_pain_points, source_label)
    
    print(f"✅ Created {len(clusters)} opportunity cluster(s)")
    
    # Generate report
    report = generate_report(clusters)
    
    # Save report
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    report_file = output_path / "weekly_report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Report saved to: {report_file}")

    if db_path:
        db = ScannerDatabase(db_path)
        scan_run_id = db.persist_scan(
            fixture_path=source_label,
            report_path=str(report_file),
            source_count=len(sources),
            pain_points=all_pain_points,
            clusters=clusters,
        )
        print(f"✅ Saved findings to SQLite: {db_path} (scan run #{scan_run_id})")
    print("")
    print("Preview:")
    print("=" * 60)
    print(report[:1000])
    if len(report) > 1000:
        print("\n... (truncated, see full report in file)")
    print("=" * 60)
    
    return str(report_file)


def scan_from_fixture(
    fixture_path: str,
    output_dir: str = "reports",
    db_path: Optional[str] = None,
    extractor_mode: str = "heuristic",
    llm_command: Optional[str] = None,
) -> str:
    """Run the scanner on a local fixture file and generate a report."""
    collector = FixtureCollector(fixture_path)
    return scan_sources(collector.collect(), fixture_path, output_dir, db_path, extractor_mode, llm_command)


def scan_from_hn(
    query: str,
    output_dir: str = "reports",
    db_path: Optional[str] = None,
    limit: int = 20,
    extractor_mode: str = "heuristic",
    llm_command: Optional[str] = None,
) -> str:
    """Run the scanner against real Hacker News search results."""
    collector = HackerNewsCollector(query=query, limit=limit)
    return scan_sources(collector.collect(), f"hn:{query}", output_dir, db_path, extractor_mode, llm_command)


def scan_from_hn_pack(
    pack: str,
    output_dir: str = "reports",
    db_path: Optional[str] = None,
    limit: int = 20,
    extractor_mode: str = "heuristic",
    llm_command: Optional[str] = None,
) -> str:
    """Run the scanner against every HN query in a named query pack."""
    sources = collect_hn_pack(pack, limit_per_query=limit)
    return scan_sources(sources, f"hn-pack:{pack}", output_dir, db_path, extractor_mode, llm_command)


def main():
    parser = argparse.ArgumentParser(
        description="Market Problem Scanner - Discover monetizable pain points"
    )
    parser.add_argument(
        "--fixture",
        default="fixtures/sample_pain_points.json",
        help="Path to fixture JSON file"
    )
    parser.add_argument(
        "--source",
        choices=["fixture", "hn", "hn-pack"],
        default="fixture",
        help="Collector source: fixture for local demo data, hn for one Hacker News query, hn-pack for a named HN query pack"
    )
    parser.add_argument(
        "--query",
        default="manual spreadsheet",
        help="Search query for live collectors such as --source hn"
    )
    parser.add_argument(
        "--pack",
        default="ops-manual-work",
        help="Named query pack for --source hn-pack"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum live-source results to collect per query"
    )
    parser.add_argument(
        "--output",
        default="reports",
        help="Output directory for reports"
    )
    parser.add_argument(
        "--extractor",
        choices=["heuristic", "structured"],
        default="heuristic",
        help="Extraction mode. structured calls --llm-command and expects strict JSON."
    )
    parser.add_argument(
        "--llm-command",
        default=None,
        help="Shell command for --extractor structured. Prompt is passed on stdin; stdout must be JSON."
    )
    parser.add_argument(
        "--db",
        default=None,
        help="Optional SQLite database path for persisted dashboard findings"
    )
    
    args = parser.parse_args()
    
    try:
        if args.source == "hn":
            report_path = scan_from_hn(args.query, args.output, args.db, args.limit, args.extractor, args.llm_command)
        elif args.source == "hn-pack":
            report_path = scan_from_hn_pack(args.pack, args.output, args.db, args.limit, args.extractor, args.llm_command)
        else:
            report_path = scan_from_fixture(args.fixture, args.output, args.db, args.extractor, args.llm_command)
        print(f"\n✅ Success! Report: {report_path}")
        return 0
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print(f"\nCreate a fixture file at: {args.fixture}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
