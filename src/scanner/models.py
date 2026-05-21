"""Data models for pain points and opportunity clusters."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Optional
from uuid import uuid4
import json


@dataclass
class PainPoint:
    """A single pain point extracted from a source."""
    
    source_url: str
    quote: str
    audience: str
    
    # Auto-generated fields
    id: str = field(default_factory=lambda: f"pain_{uuid4().hex[:8]}")
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Extracted fields
    source_type: str = ""
    pain: str = ""
    workaround: str = ""
    existing_tools: List[str] = field(default_factory=list)
    
    # Scoring fields (0-5 scale each)
    intensity: int = 0
    frequency: int = 0
    buyer_quality: int = 0
    workaround_cost: int = 0
    existing_spend: int = 0
    reachability: int = 0
    mvp_simplicity: int = 0
    competition_gap: int = 0
    total_score: int = 0
    
    # Analysis fields
    monetization_hypothesis: str = ""
    mvp_angle: str = ""
    confidence: str = "unknown"
    processed_by: str = ""
    reviewed_by: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "PainPoint":
        """Create PainPoint from dictionary."""
        return cls(**data)


@dataclass
class OpportunityCluster:
    """A cluster of related pain points forming a single opportunity."""
    
    title: str
    pain_points: List[PainPoint]
    
    # Auto-generated fields
    id: str = field(default_factory=lambda: f"opp_{uuid4().hex[:8]}")
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Cluster analysis
    domain: str = ""
    audience: str = ""
    total_mentions: int = 0
    avg_score: float = 0.0
    
    # Strategic analysis
    executive_summary: str = ""
    monetization_strategy: str = ""
    mvp_approach: str = ""
    competitive_landscape: str = ""
    recommendation: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert nested PainPoint objects
        data['pain_points'] = [pp.to_dict() if hasattr(pp, 'to_dict') else pp 
                               for pp in self.pain_points]
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "OpportunityCluster":
        """Create OpportunityCluster from dictionary."""
        pain_points = [PainPoint.from_dict(pp) if isinstance(pp, dict) else pp 
                      for pp in data.pop('pain_points', [])]
        return cls(pain_points=pain_points, **data)
