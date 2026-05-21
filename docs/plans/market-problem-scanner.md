# Market Problem Scanner Pipeline — Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build an automated pipeline that discovers repeated monetizable pain points from public sources and converts them into evidence-backed AI Daily Ideas.

**Architecture:** Two-tier agentic workflow. Local Qwen handles high-volume extraction, classification, deduplication, and rough scoring (cheap scout). Claude planner/reviewer synthesizes clusters, applies business judgment, ranks opportunities, and produces final reports (strategic decision-maker).

**Tech Stack:** Python 3.10+, local-qwen profile (Hermes), ai-daily-planner profile (Hermes), Hermes Kanban for orchestration, Reddit API (PRAW), web scraping (BeautifulSoup/Playwright), optional X/Twitter API.

---

## Purpose

Find repeated, monetizable pain points from public conversations and convert them into evidence-backed AI Daily Ideas that are:
- Validated by real user complaints (not guesswork)
- Scored on intensity, frequency, buyer quality, and MVP simplicity
- Ready for execution by solo devs or small teams

## Data Sources (v1)

**Primary sources (v1 launch):**
- Reddit: r/Entrepreneur, r/smallbusiness, r/SaaS, r/freelance, r/digitalnomad, niche-specific subreddits
- Public web searches: "I wish there was a tool for...", "frustrated with...", "tired of manually..."
- HackerNews: Show HN, Ask HN threads about pain points
- Indie Hackers forums

**Optional future sources (v2+):**
- X/Twitter: if API access or auth becomes available; search for complaints, feature requests
- Product Hunt comments: extract "I need this for..." patterns
- GitHub Issues: common feature requests across popular repos

## Role Split: Qwen vs Claude

### Local Qwen (Cheap Scout)
**Use for high-volume, repetitive, mechanical tasks:**
- Extract pain points from raw text (comments, posts, threads)
- Classify pain points by domain (dev tools, marketing, ops, finance, etc.)
- Deduplicate similar complaints using fuzzy matching
- Apply initial scoring rubric (0-5 scale per factor)
- Summarize individual pain points into structured records
- Flag spam, off-topic, or low-signal content

**Do NOT use for:**
- Final business judgment
- Strategic ranking across opportunity clusters
- Synthesis of evidence into executive summaries
- Deciding which ideas to promote to Daily Ideas
- Writing polished reports for human review

### Claude Planner/Reviewer (Strategic Decision-Maker)
**Use for high-value, judgment-heavy tasks:**
- Synthesize Qwen's extractions into coherent opportunity clusters
- Apply business judgment: is this really monetizable? Is the pain deep enough?
- Rank opportunities by total score and strategic fit
- Write executive summaries and recommendations
- Generate AI Daily Idea drafts from top clusters
- Review Qwen's work for quality and catch hallucinations
- Final approval before PRs or reports go out

**Principle:** Qwen does the $0.01/1K tokens grunt work; Claude does the $3/1M tokens thinking.

## Evidence Schema

Each detected pain point is stored as a structured record:

```json
{
  "id": "pain_<uuid>",
  "source_url": "https://reddit.com/r/Entrepreneur/comments/abc123",
  "source_type": "reddit_comment",
  "collected_at": "2026-05-21T12:00:00Z",
  "quote": "I'm tired of manually copy-pasting data between Stripe and QuickBooks every week. Takes me 2 hours and I always make mistakes.",
  "audience": "small business owners, e-commerce operators",
  "pain": "manual data entry between Stripe and QuickBooks",
  "workaround": "weekly manual CSV export/import, error-prone",
  "existing_tools": ["Zapier (complex setup)", "A2X ($20/mo, overkill for small shops)"],
  "intensity": 4,
  "frequency": 5,
  "buyer_quality": 4,
  "workaround_cost": 4,
  "existing_spend": 3,
  "reachability": 4,
  "mvp_simplicity": 3,
  "competition_gap": 3,
  "total_score": 30,
  "monetization_hypothesis": "$15/mo subscription, target 100 users = $18K ARR",
  "mvp_angle": "OAuth + read-only Stripe sync, auto-generate QuickBooks-ready CSV",
  "confidence": "high",
  "processed_by": "local-qwen",
  "reviewed_by": null
}
```

## Scoring Rubric (0-5 scale per factor)

Each pain point is scored on 8 factors. Qwen applies the rubric mechanically; Claude reviews and adjusts.

| Factor | 0 (Low) | 3 (Medium) | 5 (High) |
|--------|---------|------------|----------|
| **Pain Intensity** | Minor annoyance | Significant friction | Mission-critical blocker |
| **Frequency** | Once a year | Monthly | Daily/hourly |
| **Buyer Quality** | Hobbyists, no budget | Freelancers, small budget | SMBs/enterprises, proven spend |
| **Workaround/Manual Labor** | None, easy fix | Manual but tolerable | Painful manual work, high error rate |
| **Existing Spend** | $0 | $10-50/mo | $100+/mo |
| **Reachability** | Hard to find audience | Niche communities exist | Active online communities, SEO-able |
| **MVP Simplicity** | Requires AI/ML, complex | Standard CRUD + API | No-code/low-code viable |
| **Competition Gap** | Saturated market | 2-3 established players | No good solution or major gaps |

**Total Score Range:** 0-40  
**Threshold for promotion:** ≥25 (Qwen flags, Claude reviews)

## Daily/Weekly Workflow

### Daily Collection (Automated)
1. **Collect** (1 hour, Qwen): Scrape Reddit, HN, search results; save raw HTML/JSON
2. **Extract** (30 min, Qwen): Parse raw data → structured pain point records
3. **Classify** (15 min, Qwen): Tag by domain, audience, urgency
4. **Deduplicate** (15 min, Qwen): Merge similar complaints

### Weekly Synthesis (Semi-Automated)
5. **Cluster** (30 min, Qwen): Group related pain points → opportunity clusters
6. **Score** (1 hour, Qwen): Apply scoring rubric to each cluster
7. **Synthesize** (1 hour, Claude): Review Qwen's clusters, apply business judgment, rank by total score + strategic fit
8. **Create Opportunity Cards** (30 min, Claude): Top 3-5 clusters → draft AI Daily Idea files (using existing format)
9. **Review** (30 min, ai-daily-reviewer): Check for hallucinated evidence, confirm source URLs, validate scoring logic
10. **PR/Report** (15 min, Claude): Commit new ideas to repo, open PR, generate weekly summary report

**Total weekly cost estimate:**
- Qwen: ~500K tokens input, ~100K tokens output = ~$0.60
- Claude: ~50K tokens input, ~20K tokens output = ~$1.50
- **Total: ~$2.10/week**

## Safety & Quality Rules

### Safety
- **No autonomous outreach:** Do not contact users, post to forums, or scrape private/gated communities
- **No spam:** Do not auto-generate spammy content or mass-post ideas
- **Respect robots.txt:** Follow crawl delays, rate limits, and exclusions
- **No personal data:** Strip usernames, emails, and PII from evidence records

### Quality
- **Preserve source URLs:** Every pain point must link back to the original source
- **Avoid hallucinated evidence:** Qwen's extractions must be reviewable by Claude; flag uncertain claims
- **Mark uncertain claims:** Use `"confidence": "low"` when evidence is thin or ambiguous
- **Human review required:** All ideas must pass ai-daily-reviewer before merging to main
- **Version control:** All evidence, scores, and reports tracked in git

## Initial Implementation Tasks (Next PR)

### Task 1: Create Core Data Structures
**Objective:** Define pain point schema and storage format

**Files:**
- Create: `src/scanner/models.py`
- Create: `src/scanner/storage.py`
- Create: `tests/test_models.py`

**Step 1: Write failing test**
```python
# tests/test_models.py
def test_pain_point_creation():
    from scanner.models import PainPoint
    pain = PainPoint(
        source_url="https://example.com",
        quote="I hate doing X manually",
        audience="developers"
    )
    assert pain.id.startswith("pain_")
    assert pain.total_score == 0  # Not scored yet
```

**Step 2: Run test to verify failure**
Run: `pytest tests/test_models.py::test_pain_point_creation -v`
Expected: FAIL — "ModuleNotFoundError: No module named 'scanner'"

**Step 3: Write minimal implementation**
```python
# src/scanner/models.py
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

@dataclass
class PainPoint:
    source_url: str
    quote: str
    audience: str
    id: str = field(default_factory=lambda: f"pain_{uuid4().hex[:8]}")
    source_type: str = ""
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())
    pain: str = ""
    workaround: str = ""
    existing_tools: list = field(default_factory=list)
    intensity: int = 0
    frequency: int = 0
    buyer_quality: int = 0
    workaround_cost: int = 0
    existing_spend: int = 0
    reachability: int = 0
    mvp_simplicity: int = 0
    competition_gap: int = 0
    total_score: int = 0
    monetization_hypothesis: str = ""
    mvp_angle: str = ""
    confidence: str = "unknown"
    processed_by: str = ""
    reviewed_by: str = None
```

**Step 4: Run test to verify pass**
Run: `pytest tests/test_models.py::test_pain_point_creation -v`
Expected: PASS

**Step 5: Commit**
```bash
git add src/scanner/models.py tests/test_models.py
git commit -m "feat: add PainPoint data model"
```

---

### Task 2: Create Reddit Collector Script
**Objective:** Scrape Reddit threads and save raw data

**Files:**
- Create: `src/scanner/collectors/reddit.py`
- Create: `tests/test_reddit_collector.py`

**Step 1: Write failing test**
```python
# tests/test_reddit_collector.py
def test_reddit_collector_fetch():
    from scanner.collectors.reddit import RedditCollector
    collector = RedditCollector(subreddit="test", limit=5)
    posts = collector.fetch()
    assert len(posts) <= 5
    assert all("url" in p and "text" in p for p in posts)
```

**Step 2: Run test to verify failure**
Run: `pytest tests/test_reddit_collector.py -v`
Expected: FAIL — "ModuleNotFoundError: No module named 'scanner.collectors'"

**Step 3: Write minimal implementation**
```python
# src/scanner/collectors/reddit.py
import praw
from typing import List, Dict

class RedditCollector:
    def __init__(self, subreddit: str, limit: int = 10):
        self.subreddit = subreddit
        self.limit = limit
        self.reddit = praw.Reddit(
            client_id="your_client_id",
            client_secret="your_client_secret",
            user_agent="market-problem-scanner/0.1"
        )
    
    def fetch(self) -> List[Dict[str, str]]:
        posts = []
        subreddit = self.reddit.subreddit(self.subreddit)
        for submission in subreddit.hot(limit=self.limit):
            posts.append({
                "url": submission.url,
                "text": submission.title + "\n" + submission.selftext,
                "score": submission.score,
                "comments": submission.num_comments
            })
        return posts
```

**Step 4: Run test to verify pass**
Run: `pytest tests/test_reddit_collector.py -v`
Expected: PASS (or SKIP if no Reddit credentials configured)

**Step 5: Commit**
```bash
git add src/scanner/collectors/reddit.py tests/test_reddit_collector.py
git commit -m "feat: add Reddit collector"
```

---

### Task 3: Create Qwen Extraction Prompt Template
**Objective:** Define the prompt template for Qwen to extract pain points from raw text

**Files:**
- Create: `src/scanner/prompts/extract_pain.txt`
- Create: `tests/test_prompts.py`

**Step 1: Write failing test**
```python
# tests/test_prompts.py
def test_extract_pain_prompt_exists():
    from pathlib import Path
    prompt_path = Path("src/scanner/prompts/extract_pain.txt")
    assert prompt_path.exists()
    assert len(prompt_path.read_text()) > 100
```

**Step 2: Run test to verify failure**
Run: `pytest tests/test_prompts.py::test_extract_pain_prompt_exists -v`
Expected: FAIL — "AssertionError: assert False"

**Step 3: Write minimal implementation**
```txt
# src/scanner/prompts/extract_pain.txt
You are a market research analyst. Extract pain points from the following text.

For each pain point you find, output a JSON object with these fields:
- quote: the exact quote expressing the pain
- audience: who experiences this pain (be specific)
- pain: short description of the problem
- workaround: current manual/painful workaround they use
- existing_tools: list of existing tools mentioned (if any)

Only extract pain points that are:
- Specific and actionable
- Expressed by someone who actually experiences the problem
- Related to a workflow, process, or recurring task

Do NOT extract:
- Vague complaints without details
- Hypothetical scenarios
- Spam or off-topic content

Text to analyze:
{raw_text}

Output format: JSON array of pain point objects.
```

**Step 4: Run test to verify pass**
Run: `pytest tests/test_prompts.py::test_extract_pain_prompt_exists -v`
Expected: PASS

**Step 5: Commit**
```bash
mkdir -p src/scanner/prompts
git add src/scanner/prompts/extract_pain.txt tests/test_prompts.py
git commit -m "feat: add Qwen extraction prompt template"
```

---

### Task 4: Create Scoring Module
**Objective:** Apply the 0-5 rubric to each pain point

**Files:**
- Create: `src/scanner/scoring.py`
- Create: `tests/test_scoring.py`

**Step 1: Write failing test**
```python
# tests/test_scoring.py
def test_score_pain_point():
    from scanner.models import PainPoint
    from scanner.scoring import score_pain_point
    
    pain = PainPoint(
        source_url="https://example.com",
        quote="I spend 2 hours every week manually syncing data",
        audience="small business owners",
        pain="manual data sync",
        frequency=5,  # Weekly
        intensity=4   # Significant
    )
    
    scored = score_pain_point(pain)
    assert scored.total_score > 0
    assert scored.total_score <= 40
```

**Step 2: Run test to verify failure**
Run: `pytest tests/test_scoring.py -v`
Expected: FAIL — "ImportError: cannot import name 'score_pain_point'"

**Step 3: Write minimal implementation**
```python
# src/scanner/scoring.py
from scanner.models import PainPoint

def score_pain_point(pain: PainPoint) -> PainPoint:
    """Apply scoring rubric to a pain point."""
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
```

**Step 4: Run test to verify pass**
Run: `pytest tests/test_scoring.py -v`
Expected: PASS

**Step 5: Commit**
```bash
git add src/scanner/scoring.py tests/test_scoring.py
git commit -m "feat: add scoring rubric implementation"
```

---

### Task 5: Create Sample Report Template
**Objective:** Define the output format for weekly opportunity reports

**Files:**
- Create: `templates/weekly_report.md`

**Step 1: Create template file**
```markdown
# templates/weekly_report.md
# Market Problem Scanner — Weekly Report
**Week of:** {week_start} to {week_end}  
**Generated:** {timestamp}

## Summary
- **Pain points collected:** {total_collected}
- **Clusters identified:** {total_clusters}
- **Opportunities scored ≥25:** {high_score_count}
- **Top recommendations:** {top_count}

---

## Top Opportunities

{opportunity_list}

---

## Detailed Analysis

{detailed_analysis}

---

## Next Steps
- Review top 3 opportunities with human judgment
- Create AI Daily Idea drafts for approved opportunities
- Open PR with new ideas

**Report generated by:** {generated_by}
```

**Step 2: Commit**
```bash
mkdir -p templates
git add templates/weekly_report.md
git commit -m "feat: add weekly report template"
```

---

### Task 6: Create Hermes Kanban Task Graph
**Objective:** Define the multi-agent workflow using Kanban tasks

**Files:**
- Create: `docs/kanban-workflow.md`

**Step 1: Document the workflow**
```markdown
# docs/kanban-workflow.md
# Market Problem Scanner — Kanban Workflow

## Weekly Execution Graph

### Task 1: Collect Raw Data (Assignee: local-qwen)
**Title:** Collect raw data from Reddit, HN, web searches  
**Skills:** None (uses Hermes terminal + web tools)  
**Workspace:** `scratch`  
**Output:** `raw_data/*.json` (Reddit posts, HN threads, search results)

---

### Task 2: Extract Pain Points (Assignee: local-qwen)
**Title:** Extract pain points from raw data using extraction prompt  
**Skills:** None  
**Parents:** Task 1  
**Workspace:** `dir:/path/to/persistent/scanner/workspace`  
**Output:** `pain_points/*.json` (structured pain point records)

---

### Task 3: Deduplicate & Score (Assignee: local-qwen)
**Title:** Deduplicate similar pain points and apply scoring rubric  
**Skills:** None  
**Parents:** Task 2  
**Workspace:** Same as Task 2  
**Output:** `scored_pain_points.json`

---

### Task 4: Synthesize & Rank (Assignee: ai-daily-planner)
**Title:** Review Qwen's extractions, apply business judgment, rank opportunities  
**Skills:** None  
**Parents:** Task 3  
**Workspace:** Same as Task 2  
**Output:** `opportunity_clusters.json`, `weekly_report.md`

---

### Task 5: Generate Idea Drafts (Assignee: ai-daily-planner)
**Title:** Create AI Daily Idea drafts for top 3 opportunities  
**Skills:** None  
**Parents:** Task 4  
**Workspace:** Same as Task 2  
**Output:** `ideas/2026-XX-XX-*.md` (draft idea files)

---

### Task 6: Review & Approve (Assignee: ai-daily-reviewer)
**Title:** Review idea drafts for quality, evidence, and feasibility  
**Skills:** None  
**Parents:** Task 5  
**Workspace:** Same as Task 2  
**Output:** Approval/rejection comments, revised drafts if needed

---

### Task 7: Merge to Main (Assignee: ai-daily-planner)
**Title:** Open PR with approved ideas and weekly report  
**Skills:** `github-pr-workflow`  
**Parents:** Task 6  
**Workspace:** `worktree` (branch: `feat/weekly-scanner-YYYY-MM-DD`)  
**Output:** GitHub PR URL

---

## Task Creation Script

```python
# Create the weekly workflow tasks
import os
from datetime import datetime

week_id = datetime.now().strftime("%Y-%m-%d")
workspace_path = f"/Users/buddyguy/scanner-workspace/{week_id}"

task1 = kanban_create(
    title=f"Collect raw data (week {week_id})",
    assignee="local-qwen",
    workspace_kind="scratch"
)

task2 = kanban_create(
    title=f"Extract pain points (week {week_id})",
    assignee="local-qwen",
    parents=[task1["task_id"]],
    workspace_kind="dir",
    workspace_path=workspace_path
)

task3 = kanban_create(
    title=f"Deduplicate & score (week {week_id})",
    assignee="local-qwen",
    parents=[task2["task_id"]],
    workspace_kind="dir",
    workspace_path=workspace_path
)

task4 = kanban_create(
    title=f"Synthesize & rank (week {week_id})",
    assignee="ai-daily-planner",
    parents=[task3["task_id"]],
    workspace_kind="dir",
    workspace_path=workspace_path
)

task5 = kanban_create(
    title=f"Generate idea drafts (week {week_id})",
    assignee="ai-daily-planner",
    parents=[task4["task_id"]],
    workspace_kind="dir",
    workspace_path=workspace_path
)

task6 = kanban_create(
    title=f"Review & approve ideas (week {week_id})",
    assignee="ai-daily-reviewer",
    parents=[task5["task_id"]],
    workspace_kind="dir",
    workspace_path=workspace_path
)

task7 = kanban_create(
    title=f"Merge to main (week {week_id})",
    assignee="ai-daily-planner",
    parents=[task6["task_id"]],
    workspace_kind="worktree",
    workspace_path=f"/Users/buddyguy/projects/ai-daily-ideas/.worktrees/scanner-{week_id}",
    skills=["github-pr-workflow"]
)
```
```

**Step 2: Commit**
```bash
git add docs/kanban-workflow.md
git commit -m "docs: add Kanban workflow definition"
```

---

### Task 7: Create Environment Setup Script
**Objective:** Document dependencies and setup steps

**Files:**
- Create: `docs/setup.md`

**Step 1: Write setup documentation**
```markdown
# docs/setup.md
# Market Problem Scanner — Setup Guide

## Prerequisites
- Python 3.10+
- Hermes Agent with profiles: ai-daily-planner, ai-daily-coder, ai-daily-reviewer, local-qwen
- Git
- Reddit API credentials (optional, for Reddit collector)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ear2earGrin/ai-daily-ideas.git
cd ai-daily-ideas
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install praw beautifulsoup4 playwright pytest
```

4. Configure Reddit API (optional):
```bash
# Create .env file
cat > .env << EOF
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=market-problem-scanner/0.1
EOF
```

5. Run tests:
```bash
pytest tests/ -v
```

## Usage

### Manual Collection
```bash
python -m scanner.collectors.reddit --subreddit Entrepreneur --limit 50
```

### Weekly Workflow (Automated)
```bash
# Create the weekly Kanban tasks
hermes kanban create "Weekly scanner: 2026-05-21" --assignee ai-daily-planner
```

The ai-daily-planner will orchestrate the full pipeline using the task graph defined in `docs/kanban-workflow.md`.
```

**Step 2: Commit**
```bash
git add docs/setup.md
git commit -m "docs: add setup guide"
```

---

## Summary of Implementation Tasks

1. **Task 1:** Create core data structures (PainPoint model, storage) — ai-daily-coder
2. **Task 2:** Create Reddit collector script — ai-daily-coder
3. **Task 3:** Create Qwen extraction prompt template — ai-daily-planner
4. **Task 4:** Create scoring module — ai-daily-coder
5. **Task 5:** Create sample report template — ai-daily-planner
6. **Task 6:** Create Hermes Kanban task graph — ai-daily-planner
7. **Task 7:** Create environment setup script — ai-daily-coder

**Estimated total effort:** 8-12 hours (split across 4 profiles)

**Next PR deliverables:**
- Working code for Tasks 1-4
- Templates and documentation for Tasks 5-7
- Full test coverage (pytest)
- CI/CD checks (if applicable)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       Weekly Trigger (Cron/Manual)              │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │   Task 1: Collect (local-qwen) │
                │   Reddit/HN/Web → raw_data/*.json│
                └────────────────┬────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │   Task 2: Extract (local-qwen) │
                │   Raw text → pain_points.json    │
                └────────────────┬────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │   Task 3: Dedupe/Score (Qwen)  │
                │   Merge + Rubric → scored.json   │
                └────────────────┬────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │   Task 4: Synthesize (Claude)  │
                │   Business judgment → ranked.json│
                └────────────────┬────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │   Task 5: Ideas (Claude)       │
                │   Top 3 → idea drafts           │
                └────────────────┬────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │   Task 6: Review (Reviewer)    │
                │   Check evidence → approval     │
                └────────────────┬────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │   Task 7: Merge (Claude)       │
                │   Open PR → repo updated        │
                └─────────────────────────────────┘
```

---

## Success Criteria

- [ ] All 7 implementation tasks have passing tests
- [ ] Qwen profile successfully extracts pain points from sample Reddit data
- [ ] Scoring rubric produces total scores in 0-40 range
- [ ] Claude profile synthesizes Qwen output into ranked opportunities
- [ ] Weekly report template generates readable markdown
- [ ] Kanban workflow executes end-to-end without manual intervention
- [ ] No hallucinated evidence (all pain points traceable to source URLs)
- [ ] Cost stays under $5/week for full pipeline

---

**Role clarity:** Qwen is the cheap scout for repetitive extraction/classification/summarization. Claude planner/reviewer applies final business judgment, synthesis, and strategic ranking.
