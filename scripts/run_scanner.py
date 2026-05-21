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

from scanner.collectors import FixtureCollector
from scanner.extractor import HeuristicExtractor
from scanner.models import OpportunityCluster
from scanner.scoring import score_pain_point, score_cluster, rank_clusters
from scanner.reporter import generate_report
from scanner.storage import PainPointStorage, ClusterStorage
from scanner.sqlite_storage import ScannerDatabase


def scan_from_fixture(fixture_path: str, output_dir: str = "reports", db_path: Optional[str] = None) -> str:
    """
    Run the scanner on a fixture file and generate a report.
    
    Args:
        fixture_path: Path to JSON fixture file
        output_dir: Directory for output reports
    
    Returns:
        Path to generated report
    """
    print(f"📊 Market Problem Scanner v0.2.0")
    print(f"📁 Loading fixture: {fixture_path}")
    
    # Collect data
    collector = FixtureCollector(fixture_path)
    sources = collector.collect()
    print(f"✅ Loaded {len(sources)} source(s)")
    
    # Extract pain points
    extractor = HeuristicExtractor()
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
    
    # Simple clustering: group all pain points into one cluster for prototype
    # (Real clustering would use similarity/domain grouping)
    if all_pain_points:
        cluster = OpportunityCluster(
            title="Automated Pain Point Opportunities",
            pain_points=all_pain_points,
            domain="multi-domain",
            audience="various",
            executive_summary="Collection of pain points extracted from fixtures",
        )
        score_cluster(cluster)
        clusters = [cluster]
    else:
        clusters = []
    
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
            fixture_path=fixture_path,
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
        "--output",
        default="reports",
        help="Output directory for reports"
    )
    parser.add_argument(
        "--db",
        default=None,
        help="Optional SQLite database path for persisted dashboard findings"
    )
    
    args = parser.parse_args()
    
    try:
        report_path = scan_from_fixture(args.fixture, args.output, args.db)
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
