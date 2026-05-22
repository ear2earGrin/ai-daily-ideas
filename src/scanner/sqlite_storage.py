"""SQLite persistence for scanner findings and dashboard review state."""

from __future__ import annotations

import hashlib
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .models import OpportunityCluster, PainPoint
from .scoring import score_opportunity_ranking


STATUS_VALUES = {"new", "interesting", "ignore", "build", "validate"}

TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {"ref", "ref_src", "source", "fbclid", "gclid"}


def normalize_source_url(url: str) -> str:
    """Normalize source URLs enough for local dedupe without losing provenance."""
    parts = urlsplit((url or "").strip())
    query_pairs = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered in TRACKING_QUERY_KEYS or any(lowered.startswith(prefix) for prefix in TRACKING_QUERY_PREFIXES):
            continue
        query_pairs.append((key, value))
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), urlencode(query_pairs), ""))


def normalize_quote(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def pain_point_fingerprint(pain: PainPoint) -> str:
    payload = f"{normalize_source_url(pain.source_url)}\n{normalize_quote(pain.quote)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class ScannerDatabase:
    """Small sqlite3 wrapper for local scanner findings."""

    def __init__(self, db_path: str = "data/scanner.sqlite"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS scan_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    fixture_path TEXT,
                    report_path TEXT,
                    source_count INTEGER NOT NULL DEFAULT 0,
                    pain_point_count INTEGER NOT NULL DEFAULT 0,
                    cluster_count INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS pain_points (
                    id TEXT PRIMARY KEY,
                    scan_run_id INTEGER,
                    quote TEXT NOT NULL,
                    pain TEXT,
                    source_url TEXT NOT NULL,
                    source_type TEXT,
                    audience TEXT,
                    domain TEXT,
                    fingerprint TEXT,
                    total_score INTEGER NOT NULL DEFAULT 0,
                    intensity INTEGER NOT NULL DEFAULT 0,
                    frequency INTEGER NOT NULL DEFAULT 0,
                    buyer_quality INTEGER NOT NULL DEFAULT 0,
                    workaround_cost INTEGER NOT NULL DEFAULT 0,
                    existing_spend INTEGER NOT NULL DEFAULT 0,
                    reachability INTEGER NOT NULL DEFAULT 0,
                    mvp_simplicity INTEGER NOT NULL DEFAULT 0,
                    competition_gap INTEGER NOT NULL DEFAULT 0,
                    collected_at TEXT,
                    status TEXT NOT NULL DEFAULT 'new',
                    notes TEXT NOT NULL DEFAULT '',
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(scan_run_id) REFERENCES scan_runs(id) ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS clusters (
                    id TEXT PRIMARY KEY,
                    scan_run_id INTEGER,
                    title TEXT NOT NULL,
                    domain TEXT,
                    audience TEXT,
                    total_mentions INTEGER NOT NULL DEFAULT 0,
                    avg_score REAL NOT NULL DEFAULT 0,
                    executive_summary TEXT,
                    recommendation TEXT,
                    profitability_score INTEGER NOT NULL DEFAULT 0,
                    build_probability_score INTEGER NOT NULL DEFAULT 0,
                    priority_score INTEGER NOT NULL DEFAULT 0,
                    priority_band TEXT NOT NULL DEFAULT 'unranked',
                    buyer_type TEXT,
                    monetization_guess TEXT,
                    mvp_shape TEXT,
                    risk_notes TEXT,
                    missing_data TEXT,
                    next_validation_step TEXT,
                    status TEXT NOT NULL DEFAULT 'new',
                    notes TEXT NOT NULL DEFAULT '',
                    created_at TEXT,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(scan_run_id) REFERENCES scan_runs(id) ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS cluster_pain_points (
                    cluster_id TEXT NOT NULL,
                    pain_point_id TEXT NOT NULL,
                    PRIMARY KEY(cluster_id, pain_point_id),
                    FOREIGN KEY(cluster_id) REFERENCES clusters(id) ON DELETE CASCADE,
                    FOREIGN KEY(pain_point_id) REFERENCES pain_points(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_pain_points_score ON pain_points(total_score DESC);
                CREATE INDEX IF NOT EXISTS idx_clusters_score ON clusters(avg_score DESC);
                CREATE INDEX IF NOT EXISTS idx_scan_runs_created ON scan_runs(created_at DESC);
                """
            )
            self._migrate_schema(conn)
            conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_pain_points_fingerprint ON pain_points(fingerprint) WHERE fingerprint IS NOT NULL")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_clusters_priority ON clusters(priority_score DESC)")

    def _migrate_schema(self, conn: sqlite3.Connection) -> None:
        """Add ranking columns to existing local databases without data loss."""
        cluster_columns = {row[1] for row in conn.execute("PRAGMA table_info(clusters)")}
        additions = {
            "profitability_score": "INTEGER NOT NULL DEFAULT 0",
            "build_probability_score": "INTEGER NOT NULL DEFAULT 0",
            "priority_score": "INTEGER NOT NULL DEFAULT 0",
            "priority_band": "TEXT NOT NULL DEFAULT 'unranked'",
            "buyer_type": "TEXT",
            "monetization_guess": "TEXT",
            "mvp_shape": "TEXT",
            "risk_notes": "TEXT",
            "missing_data": "TEXT",
            "next_validation_step": "TEXT",
        }
        for column, definition in additions.items():
            if column not in cluster_columns:
                conn.execute(f"ALTER TABLE clusters ADD COLUMN {column} {definition}")

        pain_columns = {row[1] for row in conn.execute("PRAGMA table_info(pain_points)")}
        if "fingerprint" not in pain_columns:
            conn.execute("ALTER TABLE pain_points ADD COLUMN fingerprint TEXT")
        for row in conn.execute("SELECT id, source_url, quote FROM pain_points WHERE fingerprint IS NULL OR fingerprint = ''"):
            payload = f"{normalize_source_url(row['source_url'])}\n{normalize_quote(row['quote'])}"
            conn.execute(
                "UPDATE pain_points SET fingerprint = ? WHERE id = ?",
                (hashlib.sha256(payload.encode("utf-8")).hexdigest(), row["id"]),
            )
        for row in conn.execute(
            """
            SELECT id, fingerprint, ROW_NUMBER() OVER (PARTITION BY fingerprint ORDER BY id) AS duplicate_index
            FROM pain_points
            WHERE fingerprint IS NOT NULL AND fingerprint != ''
            """
        ):
            if row["duplicate_index"] > 1:
                conn.execute(
                    "UPDATE pain_points SET fingerprint = ? WHERE id = ?",
                    (f"{row['fingerprint']}:{row['id']}", row["id"]),
                )

    def create_scan_run(
        self,
        fixture_path: str,
        report_path: str,
        source_count: int,
        pain_point_count: int,
        cluster_count: int,
    ) -> int:
        now = datetime.now().isoformat(timespec="seconds")
        with self.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO scan_runs
                (created_at, fixture_path, report_path, source_count, pain_point_count, cluster_count)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (now, fixture_path, report_path, source_count, pain_point_count, cluster_count),
            )
            if cur.lastrowid is None:
                raise RuntimeError("failed to create scan run")
            return int(cur.lastrowid)

    def save_pain_points(self, pain_points: Iterable[PainPoint], scan_run_id: Optional[int] = None) -> None:
        now = datetime.now().isoformat(timespec="seconds")
        with self.connect() as conn:
            for pain in pain_points:
                fingerprint = pain_point_fingerprint(pain)
                conn.execute(
                    """
                    INSERT INTO pain_points (
                        id, scan_run_id, quote, pain, source_url, source_type, audience, domain, fingerprint,
                        total_score, intensity, frequency, buyer_quality, workaround_cost,
                        existing_spend, reachability, mvp_simplicity, competition_gap,
                        collected_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT DO NOTHING
                    """,
                    (
                        pain.id,
                        scan_run_id,
                        pain.quote,
                        pain.pain,
                        pain.source_url,
                        pain.source_type,
                        pain.audience,
                        self._infer_domain(pain.source_url),
                        fingerprint,
                        pain.total_score,
                        pain.intensity,
                        pain.frequency,
                        pain.buyer_quality,
                        pain.workaround_cost,
                        pain.existing_spend,
                        pain.reachability,
                        pain.mvp_simplicity,
                        pain.competition_gap,
                        pain.collected_at,
                        now,
                    ),
                )

    def save_clusters(self, clusters: Iterable[OpportunityCluster], scan_run_id: Optional[int] = None) -> None:
        now = datetime.now().isoformat(timespec="seconds")
        with self.connect() as conn:
            for cluster in clusters:
                score_opportunity_ranking(cluster)
                conn.execute(
                    """
                    INSERT INTO clusters (
                        id, scan_run_id, title, domain, audience, total_mentions, avg_score,
                        executive_summary, recommendation, profitability_score, build_probability_score,
                        priority_score, priority_band, buyer_type, monetization_guess, mvp_shape,
                        risk_notes, missing_data, next_validation_step, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        scan_run_id=excluded.scan_run_id,
                        title=excluded.title,
                        domain=excluded.domain,
                        audience=excluded.audience,
                        total_mentions=excluded.total_mentions,
                        avg_score=excluded.avg_score,
                        executive_summary=excluded.executive_summary,
                        recommendation=excluded.recommendation,
                        profitability_score=excluded.profitability_score,
                        build_probability_score=excluded.build_probability_score,
                        priority_score=excluded.priority_score,
                        priority_band=excluded.priority_band,
                        buyer_type=excluded.buyer_type,
                        monetization_guess=excluded.monetization_guess,
                        mvp_shape=excluded.mvp_shape,
                        risk_notes=excluded.risk_notes,
                        missing_data=excluded.missing_data,
                        next_validation_step=excluded.next_validation_step,
                        created_at=excluded.created_at,
                        updated_at=excluded.updated_at
                    """,
                    (
                        cluster.id,
                        scan_run_id,
                        cluster.title,
                        cluster.domain,
                        cluster.audience,
                        cluster.total_mentions,
                        cluster.avg_score,
                        cluster.executive_summary,
                        cluster.recommendation,
                        cluster.profitability_score,
                        cluster.build_probability_score,
                        cluster.priority_score,
                        cluster.priority_band,
                        cluster.buyer_type,
                        cluster.monetization_guess,
                        cluster.mvp_shape,
                        cluster.risk_notes,
                        cluster.missing_data,
                        cluster.next_validation_step,
                        cluster.created_at,
                        now,
                    ),
                )
                for pain in cluster.pain_points:
                    pain_id = self._stored_pain_id(conn, pain)
                    if pain_id is None:
                        continue
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO cluster_pain_points (cluster_id, pain_point_id)
                        VALUES (?, ?)
                        """,
                        (cluster.id, pain_id),
                    )

    def _stored_pain_id(self, conn: sqlite3.Connection, pain: PainPoint) -> Optional[str]:
        row = conn.execute(
            "SELECT id FROM pain_points WHERE fingerprint = ? OR id = ? ORDER BY updated_at DESC LIMIT 1",
            (pain_point_fingerprint(pain), pain.id),
        ).fetchone()
        return row["id"] if row else None

    def persist_scan(
        self,
        fixture_path: str,
        report_path: str,
        source_count: int,
        pain_points: List[PainPoint],
        clusters: List[OpportunityCluster],
    ) -> int:
        scan_run_id = self.create_scan_run(
            fixture_path=fixture_path,
            report_path=report_path,
            source_count=source_count,
            pain_point_count=len(pain_points),
            cluster_count=len(clusters),
        )
        self.save_pain_points(pain_points, scan_run_id)
        self.save_clusters(clusters, scan_run_id)
        return scan_run_id

    def summary(self) -> Dict[str, Any]:
        with self.connect() as conn:
            return {
                "scan_runs": conn.execute("SELECT COUNT(*) FROM scan_runs").fetchone()[0],
                "pain_points": conn.execute("SELECT COUNT(*) FROM pain_points").fetchone()[0],
                "clusters": conn.execute("SELECT COUNT(*) FROM clusters").fetchone()[0],
                "top_priority_score": conn.execute(
                    "SELECT COALESCE(MAX(priority_score), 0) FROM clusters"
                ).fetchone()[0],
                "validate_now": conn.execute(
                    "SELECT COUNT(*) FROM clusters WHERE priority_band = 'validate immediately'"
                ).fetchone()[0],
                "high_score_pain_points": conn.execute(
                    "SELECT COUNT(*) FROM pain_points WHERE total_score >= 25"
                ).fetchone()[0],
                "interesting_items": conn.execute(
                    "SELECT COUNT(*) FROM pain_points WHERE status IN ('interesting','build','validate')"
                ).fetchone()[0],
            }

    def recent_scan_runs(self, limit: int = 20) -> List[sqlite3.Row]:
        with self.connect() as conn:
            return list(
                conn.execute(
                    "SELECT * FROM scan_runs ORDER BY datetime(created_at) DESC, id DESC LIMIT ?",
                    (limit,),
                )
            )

    def top_clusters(self, limit: int = 50) -> List[sqlite3.Row]:
        with self.connect() as conn:
            return list(
                conn.execute(
                    """
                    WITH cluster_rollups AS (
                        SELECT
                            MIN(c.id) AS id,
                            c.title AS title,
                            MAX(c.scan_run_id) AS scan_run_id,
                            c.domain AS domain,
                            c.audience AS audience,
                            SUM(CASE WHEN c.total_mentions > 0 THEN c.total_mentions ELSE 1 END) AS total_mentions,
                            AVG(c.avg_score) AS avg_score,
                            CASE
                                WHEN COUNT(*) > 1 THEN COUNT(*) || ' scan runs rolled up for this opportunity. Open detail for evidence.'
                                ELSE MAX(c.executive_summary)
                            END AS executive_summary,
                            MAX(c.recommendation) AS recommendation,
                            MAX(c.profitability_score) AS profitability_score,
                            MAX(c.build_probability_score) AS build_probability_score,
                            MAX(c.priority_score) AS priority_score,
                            MAX(c.priority_band) AS priority_band,
                            MAX(c.buyer_type) AS buyer_type,
                            MAX(c.monetization_guess) AS monetization_guess,
                            MAX(c.mvp_shape) AS mvp_shape,
                            MAX(c.risk_notes) AS risk_notes,
                            MAX(c.missing_data) AS missing_data,
                            MAX(c.next_validation_step) AS next_validation_step,
                            MAX(c.status) AS status,
                            MAX(c.notes) AS notes,
                            MAX(c.created_at) AS created_at,
                            MAX(c.updated_at) AS updated_at,
                            COUNT(DISTINCT cpp.pain_point_id) AS evidence_count
                        FROM clusters c
                        LEFT JOIN cluster_pain_points cpp ON cpp.cluster_id = c.id
                        GROUP BY c.title, c.domain, c.audience
                    )
                    SELECT * FROM cluster_rollups
                    ORDER BY priority_score DESC, profitability_score DESC, avg_score DESC, total_mentions DESC
                    LIMIT ?
                    """,
                    (limit,),
                )
            )

    def top_pain_points(self, limit: int = 100) -> List[sqlite3.Row]:
        with self.connect() as conn:
            return list(
                conn.execute(
                    "SELECT * FROM pain_points ORDER BY total_score DESC, collected_at DESC LIMIT ?",
                    (limit,),
                )
            )

    def get_cluster(self, cluster_id: str) -> Optional[sqlite3.Row]:
        with self.connect() as conn:
            return conn.execute("SELECT * FROM clusters WHERE id = ?", (cluster_id,)).fetchone()

    def pain_points_for_cluster(self, cluster_id: str) -> List[sqlite3.Row]:
        with self.connect() as conn:
            cluster = conn.execute("SELECT title, domain, audience FROM clusters WHERE id = ?", (cluster_id,)).fetchone()
            if cluster is None:
                return []
            return list(
                conn.execute(
                    """
                    SELECT DISTINCT p.*
                    FROM pain_points p
                    JOIN cluster_pain_points cpp ON cpp.pain_point_id = p.id
                    JOIN clusters c ON c.id = cpp.cluster_id
                    WHERE c.title = ?
                      AND COALESCE(c.domain, '') = COALESCE(?, '')
                      AND COALESCE(c.audience, '') = COALESCE(?, '')
                    ORDER BY p.total_score DESC, p.collected_at DESC
                    """,
                    (cluster["title"], cluster["domain"], cluster["audience"]),
                )
            )

    def update_status_notes(self, table: str, item_id: str, status: str, notes: str) -> None:
        if table not in {"pain_points", "clusters"}:
            raise ValueError("table must be pain_points or clusters")
        if status not in STATUS_VALUES:
            raise ValueError(f"status must be one of {sorted(STATUS_VALUES)}")
        now = datetime.now().isoformat(timespec="seconds")
        with self.connect() as conn:
            conn.execute(
                f"UPDATE {table} SET status = ?, notes = ?, updated_at = ? WHERE id = ?",
                (status, notes, now, item_id),
            )

    @staticmethod
    def _infer_domain(source_url: str) -> str:
        if "reddit.com" in source_url:
            return "reddit"
        if "ycombinator.com" in source_url or "news.ycombinator.com" in source_url:
            return "hacker-news"
        return "web"
