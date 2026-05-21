"""Storage utilities for pain points and clusters."""

import json
from pathlib import Path
from typing import List, Optional
from .models import PainPoint, OpportunityCluster


class PainPointStorage:
    """Store and retrieve pain points as JSON."""
    
    def __init__(self, storage_dir: str = "data/pain_points"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, pain: PainPoint) -> Path:
        """Save a pain point to a JSON file."""
        filepath = self.storage_dir / f"{pain.id}.json"
        with open(filepath, 'w') as f:
            json.dump(pain.to_dict(), f, indent=2)
        return filepath
    
    def load(self, pain_id: str) -> Optional[PainPoint]:
        """Load a pain point by ID."""
        filepath = self.storage_dir / f"{pain_id}.json"
        if not filepath.exists():
            return None
        with open(filepath, 'r') as f:
            data = json.load(f)
        return PainPoint.from_dict(data)
    
    def load_all(self) -> List[PainPoint]:
        """Load all pain points from storage."""
        pain_points = []
        for filepath in self.storage_dir.glob("pain_*.json"):
            with open(filepath, 'r') as f:
                data = json.load(f)
            pain_points.append(PainPoint.from_dict(data))
        return pain_points


class ClusterStorage:
    """Store and retrieve opportunity clusters as JSON."""
    
    def __init__(self, storage_dir: str = "data/clusters"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, cluster: OpportunityCluster) -> Path:
        """Save a cluster to a JSON file."""
        filepath = self.storage_dir / f"{cluster.id}.json"
        with open(filepath, 'w') as f:
            json.dump(cluster.to_dict(), f, indent=2)
        return filepath
    
    def load(self, cluster_id: str) -> Optional[OpportunityCluster]:
        """Load a cluster by ID."""
        filepath = self.storage_dir / f"{cluster_id}.json"
        if not filepath.exists():
            return None
        with open(filepath, 'r') as f:
            data = json.load(f)
        return OpportunityCluster.from_dict(data)
    
    def load_all(self) -> List[OpportunityCluster]:
        """Load all clusters from storage."""
        clusters = []
        for filepath in self.storage_dir.glob("opp_*.json"):
            with open(filepath, 'r') as f:
                data = json.load(f)
            clusters.append(OpportunityCluster.from_dict(data))
        return clusters
