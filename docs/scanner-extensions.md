# Market Problem Scanner — Extension Points

This document describes how to extend the prototype with LLM-based extraction and real data sources.

## Current Implementation (v0.1.0)

The prototype uses:
- **Heuristic extraction** (`src/scanner/extractor.py`): Regex-based pattern matching for pain indicators
- **Fixture data** (`fixtures/sample_pain_points.json`): Synthetic test data
- **Deterministic scoring**: Rule-based scoring without LLM judgment

## Extension Point 1: LLM-Based Extraction

To integrate local Qwen or another LLM for pain point extraction:

### Option A: Hermes Agent Integration

```python
# src/scanner/extractors/llm_extractor.py

from pathlib import Path
import subprocess
import json

class QwenExtractor:
    """Extract pain points using local Qwen via Hermes."""
    
    def __init__(self, profile: str = "local-qwen"):
        self.profile = profile
        self.prompt_template = Path("src/scanner/prompts/extract_pain.txt").read_text()
    
    def extract(self, text: str, source_url: str, source_type: str):
        """Extract pain points using Qwen."""
        prompt = self.prompt_template.format(raw_text=text)
        
        # Call Hermes with local-qwen profile
        result = subprocess.run([
            "hermes", "chat", 
            "--profile", self.profile,
            "--prompt", prompt
        ], capture_output=True, text=True)
        
        # Parse JSON response
        extracted = json.loads(result.stdout)
        
        # Convert to PainPoint objects
        pain_points = []
        for item in extracted:
            pain = PainPoint(
                source_url=source_url,
                source_type=source_type,
                quote=item['quote'],
                audience=item['audience'],
                pain=item['pain'],
                workaround=item.get('workaround', ''),
                existing_tools=item.get('existing_tools', []),
                intensity=item.get('intensity', 0),
                frequency=item.get('frequency', 0),
                buyer_quality=item.get('buyer_quality', 0),
                processed_by="local-qwen",
            )
            pain_points.append(pain)
        
        return pain_points
```

### Option B: Direct LLM API

```python
# For providers that don't use Hermes profiles

import openai  # or other provider SDK

class LLMExtractor:
    def __init__(self, model: str = "qwen-2.5"):
        self.model = model
        self.prompt_template = Path("src/scanner/prompts/extract_pain.txt").read_text()
    
    def extract(self, text: str, source_url: str, source_type: str):
        prompt = self.prompt_template.format(raw_text=text)
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        
        # Parse and convert to PainPoint objects
        # ... (similar to above)
```

### Switching Extractors in CLI

```python
# scripts/run_scanner.py

parser.add_argument(
    "--extractor",
    choices=["heuristic", "qwen", "llm"],
    default="heuristic",
    help="Extraction method"
)

# In scan_from_fixture():
if args.extractor == "qwen":
    extractor = QwenExtractor()
elif args.extractor == "llm":
    extractor = LLMExtractor()
else:
    extractor = HeuristicExtractor()
```

## Extension Point 2: Real Data Sources

### Reddit API Collector

Already stubbed in `src/scanner/collectors/__init__.py`. To enable:

1. Install dependencies:
   ```bash
   pip install praw
   ```

2. Set environment variables:
   ```bash
   export REDDIT_CLIENT_ID="your_id"
   export REDDIT_CLIENT_SECRET="your_secret"
   export REDDIT_USER_AGENT="market-problem-scanner/0.1"
   ```

3. Use in CLI:
   ```python
   from scanner.collectors import RedditCollector
   
   collector = RedditCollector(subreddit="Entrepreneur", limit=50)
   sources = collector.collect()
   ```

### HackerNews Scraper

```python
# src/scanner/collectors/hn.py

import requests
from typing import List, Dict

class HNCollector:
    """Collect pain points from HackerNews."""
    
    def __init__(self, story_type: str = "ask", limit: int = 30):
        self.story_type = story_type  # "ask", "show", "top"
        self.limit = limit
        self.base_url = "https://hacker-news.firebaseio.com/v0"
    
    def collect(self) -> List[Dict[str, str]]:
        """Collect recent HN stories."""
        # Get story IDs
        stories_url = f"{self.base_url}/{self.story_type}stories.json"
        response = requests.get(stories_url)
        story_ids = response.json()[:self.limit]
        
        sources = []
        for story_id in story_ids:
            # Fetch story details
            story_url = f"{self.base_url}/item/{story_id}.json"
            story = requests.get(story_url).json()
            
            if story.get('text'):
                sources.append({
                    "url": f"https://news.ycombinator.com/item?id={story_id}",
                    "type": "hn",
                    "text": f"{story.get('title', '')}\n\n{story.get('text', '')}",
                    "metadata": {
                        "score": story.get('score', 0),
                        "by": story.get('by', ''),
                    }
                })
        
        return sources
```

## Extension Point 3: Clustering & Domain Detection

Current prototype groups all pain points into one cluster. For real use:

```python
# src/scanner/clustering.py

from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from .models import PainPoint, OpportunityCluster

def cluster_pain_points(pain_points: List[PainPoint], eps: float = 0.3) -> List[OpportunityCluster]:
    """Cluster similar pain points using text similarity."""
    
    if not pain_points:
        return []
    
    # Extract text features
    texts = [f"{p.pain} {p.quote}" for p in pain_points]
    vectorizer = TfidfVectorizer(max_features=100)
    features = vectorizer.fit_transform(texts)
    
    # Cluster
    clustering = DBSCAN(eps=eps, min_samples=2, metric='cosine')
    labels = clustering.fit_predict(features)
    
    # Group by cluster
    clusters = []
    for cluster_id in set(labels):
        if cluster_id == -1:  # Noise points
            continue
        
        cluster_points = [p for i, p in enumerate(pain_points) if labels[i] == cluster_id]
        
        cluster = OpportunityCluster(
            title=f"Cluster {cluster_id}",  # Better naming with LLM
            pain_points=cluster_points,
            domain=_detect_domain(cluster_points),
        )
        clusters.append(cluster)
    
    return clusters
```

## Extension Point 4: Strategic Review (Claude)

For final opportunity synthesis:

```python
# src/scanner/reviewer.py

def claude_review_cluster(cluster: OpportunityCluster) -> OpportunityCluster:
    """Use Claude to apply business judgment and write executive summary."""
    
    # Build context from evidence
    evidence_summary = "\n\n".join([
        f"- {p.quote} (Score: {p.total_score}/40, Source: {p.source_url})"
        for p in cluster.pain_points
    ])
    
    prompt = f"""
    Review this opportunity cluster and provide strategic analysis:
    
    {evidence_summary}
    
    Provide:
    1. Executive summary (2-3 sentences)
    2. Monetization strategy
    3. MVP approach
    4. Competitive landscape
    5. Recommendation (pursue/pass/investigate)
    """
    
    # Call Claude via Hermes
    result = subprocess.run([
        "hermes", "chat",
        "--profile", "ai-daily-planner",
        "--prompt", prompt
    ], capture_output=True, text=True)
    
    # Parse and update cluster
    cluster.executive_summary = "..."  # Extract from response
    cluster.monetization_strategy = "..."
    cluster.mvp_approach = "..."
    
    return cluster
```

## Running with Extensions

```bash
# With LLM extraction and real Reddit data
python3 scripts/run_scanner.py \
  --extractor qwen \
  --source reddit \
  --subreddit Entrepreneur \
  --limit 100

# Full pipeline with Claude review
python3 scripts/run_scanner.py \
  --extractor qwen \
  --source reddit \
  --reviewer claude \
  --output reports/weekly
```

## Testing Extensions

Add tests for new extractors:

```python
# tests/test_llm_extractor.py

def test_qwen_extraction():
    extractor = QwenExtractor()
    text = "I hate manually doing X..."
    pain_points = extractor.extract(text, "https://example.com", "test")
    
    assert len(pain_points) > 0
    assert pain_points[0].processed_by == "local-qwen"
```

## Cost Estimation

With LLM extractors enabled:

- **Qwen (local):** ~$0.01/1K tokens → ~$0.60/week for 500K tokens
- **Claude (strategic review):** ~$3/1M tokens → ~$1.50/week for 50K tokens
- **Total:** ~$2.10/week (as planned)

## Safety Checklist

Before enabling real collectors:

- [ ] Set rate limits on all API calls
- [ ] Respect robots.txt
- [ ] Strip PII from collected data
- [ ] Add error handling and retry logic
- [ ] Log all API calls for audit trail
- [ ] Test with small batches first
- [ ] Review collected data before processing
