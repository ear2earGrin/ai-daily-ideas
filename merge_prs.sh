#!/bin/bash
# AI Daily Ideas - PR Merge Workflow
# Run this script to merge all approved PRs in the correct order

set -e

REPO_DIR="/Users/buddyguy/projects/ai-daily-ideas"
cd "$REPO_DIR"

echo "=== AI Daily Ideas PR Merge Script ==="
echo "This will merge 3 approved PRs in sequence:"
echo "  1. PR #1: feat/repo-foundation"
echo "  2. PR #2: feat/execution-ready-briefs"
echo "  3. PR #3: feat/daily-idea-automation"
echo ""

# Ensure we're on main and up to date
echo "Step 1: Updating main branch..."
git checkout main
git pull origin main

# Try to use gh CLI if available, otherwise provide manual instructions
if command -v gh &>/dev/null && gh auth status &>/dev/null 2>&1; then
  echo "Using GitHub CLI..."
  
  echo ""
  echo "Step 2: Merging PR #1 (repo-foundation)..."
  gh pr merge 1 --squash --delete-branch || echo "PR #1 may need manual merge"
  
  echo ""
  echo "Step 3: Merging PR #2 (execution-ready-briefs)..."
  gh pr merge 2 --squash --delete-branch || echo "PR #2 may need manual merge"
  
  echo ""
  echo "Step 4: Merging PR #3 (daily-idea-automation)..."
  gh pr merge 3 --squash --delete-branch || echo "PR #3 may need manual merge"
  
else
  echo "GitHub CLI not available. Manual merge instructions:"
  echo ""
  echo "Step 2: Merge PR #1 (repo-foundation)"
  echo "  git merge --squash origin/feat/repo-foundation"
  echo "  git commit -m 'feat: add repository foundation (templates, docs, catalog)'"
  echo "  git push origin main"
  echo "  git push origin --delete feat/repo-foundation"
  echo ""
  echo "Step 3: Merge PR #2 (execution-ready-briefs)"
  echo "  git merge --squash origin/feat/execution-ready-briefs"
  echo "  git commit -m 'docs: expand ideas into execution-ready briefs'"
  echo "  git push origin main"
  echo "  git push origin --delete feat/execution-ready-briefs"
  echo ""
  echo "Step 4: Merge PR #3 (daily-idea-automation)"
  echo "  git merge --squash origin/feat/daily-idea-automation"
  echo "  git commit -m 'feat: add daily idea automation scaffold'"
  echo "  git push origin main"
  echo "  git push origin --delete feat/daily-idea-automation"
  exit 1
fi

echo ""
echo "Step 5: Pulling merged changes..."
git pull origin main

echo ""
echo "Step 6: Verifying automation works..."
if [ -f scripts/generate_index.py ]; then
  python3 scripts/generate_index.py && echo "✓ Index generation works"
else
  echo "✗ scripts/generate_index.py not found"
fi

if [ -f scripts/add_daily_idea.py ]; then
  python3 scripts/add_daily_idea.py --help > /dev/null && echo "✓ Daily idea script works"
else
  echo "✗ scripts/add_daily_idea.py not found"
fi

echo ""
echo "Step 7: Cleaning up worktrees..."
for worktree in .worktrees/t_*; do
  if [ -d "$worktree" ]; then
    echo "Removing worktree: $worktree"
    git worktree remove "$worktree" 2>/dev/null || echo "  (already removed or in use)"
  fi
done

echo ""
echo "=== Merge Complete ==="
echo "Main branch now includes:"
echo "  - Repository structure and templates"
echo "  - Execution-ready idea briefs"
echo "  - Daily idea automation tools"
echo ""
echo "Next steps:"
echo "  1. Review AUTONOMOUS_EXECUTION_PLAN.md"
echo "  2. Choose which idea to validate first"
echo "  3. Create GitHub issues for validation tasks"
echo "  4. Execute first validation task within 7 days"
