# Validation Task Reference

This document lists all 12 validation tasks extracted from the three AI Daily Ideas.
Use these as templates for creating GitHub issues or Kanban cards.

---

## Real Estate Digital Plumber (4 tasks)

### RE-DP-001: Customer Discovery Interviews
**Goal:** Interview 10 solo agents about missed leads and response time  
**Acceptance Criteria:**
- Contact 25+ solo real estate agents
- Complete 10 phone/video interviews (30 min each)
- Document pain points around lead follow-up, scheduling, and admin
- Identify at least 3 agents who lose deals due to slow response

**Time Estimate:** 1 week  
**Priority:** HIGH (foundational validation)

### RE-DP-002: Free Workflow Audit Offer
**Goal:** Offer free workflow audit to identify 3-hour time-saving automation  
**Acceptance Criteria:**
- Create workflow audit checklist (lead intake, follow-up, scheduling, quoting)
- Map current process for 3-5 agents
- Identify one specific automation that saves ≥3 hours/week
- Get written confirmation of time-saving potential

**Time Estimate:** 5 days  
**Priority:** HIGH (value validation)

### RE-DP-003: Build Concierge MVP Pilot
**Goal:** Build concierge pilot with Zapier/Make + LLM email drafting  
**Acceptance Criteria:**
- Connect form → CRM → approval queue
- LLM drafts follow-up email for new leads
- Human approval before send
- Daily summary report of actions
- Deploy for 1 agent for 2 weeks

**Time Estimate:** 1 week  
**Priority:** MEDIUM (after RE-DP-001/002)

### RE-DP-004: Collect Setup Deposit or Fee
**Goal:** Collect setup deposit or fee before implementation  
**Acceptance Criteria:**
- Create service pricing sheet (setup + monthly)
- Get at least 1 agent to commit $500-2000 setup fee
- Sign service agreement or SOW
- Schedule implementation kickoff

**Time Estimate:** 2 weeks  
**Priority:** MEDIUM (monetization proof)

---

## Niche Legacy Story Weaver (4 tasks)

### LSW-001: Build Demo Vault
**Goal:** Build demo vault: scan 5 photos + 2 voice memos → narrative draft  
**Acceptance Criteria:**
- OCR/transcribe 5 family photos + 2 voice notes
- Use LLM to generate 1000-word narrative connecting artifacts
- Create sample PDF/video showing the output
- Demonstrate in ≤10 minutes end-to-end

**Time Estimate:** 1 week  
**Priority:** HIGH (proof of concept)

### LSW-002: Family Discovery Interviews
**Goal:** Interview 5 families about legacy documentation challenges  
**Acceptance Criteria:**
- Identify 10-15 potential families (50+ years old, parents/grandparents)
- Complete 5 interviews about photo/memory preservation
- Document current solutions (boxes, Google Photos, nothing)
- Confirm willingness to pay $2k-5k for legacy book

**Time Estimate:** 1 week  
**Priority:** HIGH (demand validation)

### LSW-003: Create Productized Package
**Goal:** Create productized package: discovery, media intake, draft review  
**Acceptance Criteria:**
- Define 3-5 package tiers (basic book, premium video, full vault)
- Write discovery questionnaire for families
- Create media intake checklist and secure upload process
- Draft review/revision workflow (2-3 rounds max)

**Time Estimate:** 5 days  
**Priority:** MEDIUM (offering structure)

### LSW-004: Sell First Pilot Project
**Goal:** Sell 1 pilot project with deposit + milestone payments  
**Acceptance Criteria:**
- Get 1 family to commit $1000+ deposit
- Define scope (X photos, Y recordings, format)
- Sign contract with milestone payments
- Complete pilot within 4 weeks

**Time Estimate:** 2-3 weeks  
**Priority:** MEDIUM (revenue proof)

---

## Niche Trend Report Agent (4 tasks)

### NTR-001: Build MVP Report Generator
**Goal:** Build MVP: topic form → web scrape → structured report in 5 min  
**Acceptance Criteria:**
- Simple form accepts topic + niche keywords
- Web scraper hits 5-10 sources (news, Reddit, Twitter)
- LLM structures findings into 3-5 page PDF report
- Generate complete report in ≤5 minutes

**Time Estimate:** 1 week  
**Priority:** HIGH (technical feasibility)

### NTR-002: Content Creator Interviews
**Goal:** Interview 10 content creators about trend research workflows  
**Acceptance Criteria:**
- Identify 20+ newsletter/blog writers, YouTubers, consultants
- Complete 10 interviews about current trend research process
- Document time spent, tools used, pain points
- Confirm willingness to pay $29-99/month for automation

**Time Estimate:** 1 week  
**Priority:** HIGH (market validation)

### NTR-003: Free Report Offer
**Goal:** Offer free report to 10 target users in exchange for feedback  
**Acceptance Criteria:**
- Generate 10 custom reports for different niches
- Collect detailed feedback on quality, formatting, sources
- Measure time saved vs manual research
- Ask if they would pay and how much

**Time Estimate:** 1 week  
**Priority:** MEDIUM (quality validation)

### NTR-004: Convert to Paid Tier
**Goal:** Convert 2 users to paid tier ($29-99/month)  
**Acceptance Criteria:**
- Create pricing page with tiers (free, basic, pro)
- Offer free trial users discount to upgrade
- Get 2 paid subscriptions (any tier)
- Collect first month revenue

**Time Estimate:** 2 weeks  
**Priority:** MEDIUM (monetization proof)

---

## Recommended Execution Order

### Option A: Service-First (Real Estate Digital Plumber)
1. RE-DP-001 (interviews)
2. RE-DP-002 (audits)
3. RE-DP-003 (MVP pilot)
4. RE-DP-004 (collect payment)

**Pros:** Fastest path to revenue, recurring income, proven demand  
**Cons:** Service business (less scalable), customer support overhead

### Option B: Product-First (Niche Trend Report Agent)
1. NTR-001 (build MVP)
2. NTR-002 (interviews)
3. NTR-003 (free reports)
4. NTR-004 (convert to paid)

**Pros:** More scalable, SaaS model, product can run automated  
**Cons:** Longer to revenue, requires more technical polish

### Option C: Creative/High-Touch (Legacy Story Weaver)
1. LSW-001 (demo vault)
2. LSW-002 (interviews)
3. LSW-003 (productized package)
4. LSW-004 (first pilot)

**Pros:** High per-project revenue, meaningful product, defensible with quality  
**Cons:** Longer sales cycle, emotionally intensive, slower iteration

---

## Next Actions

1. **Choose one idea** based on personal strengths and goals
2. **Create 4 GitHub issues** for that idea's validation tasks
3. **Execute first task within 7 days** (interviews or MVP)
4. **Log results** using templates/execution-log.md
5. **Decide after Task 2:** proceed, pivot, or abandon

Use this command to create issues:
```bash
gh issue create --title "RE-DP-001: Customer Discovery Interviews" --body "$(cat task_body.md)"
```

Or use Kanban:
```bash
hermes kanban create "RE-DP-001: Customer Discovery Interviews" \
  --assignee ai-daily-planner \
  --body "$(cat task_body.md)"
```
