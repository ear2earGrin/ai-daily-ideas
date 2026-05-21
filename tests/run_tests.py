#!/usr/bin/env python3
"""Run all tests."""

import sys
from pathlib import Path

# Run each test file
test_dir = Path(__file__).parent
test_files = [
    "test_models.py",
    "test_scoring.py",
    "test_extractor.py",
    "test_sqlite_storage.py",
    "test_dashboard.py",
]

print("=" * 60)
print("Running Market Problem Scanner Tests")
print("=" * 60)
print()

failed = []

for test_file in test_files:
    print(f"Running {test_file}...")
    print("-" * 60)
    
    try:
        # Execute test file
        exec(open(test_dir / test_file).read())
        print()
    except Exception as e:
        print(f"\n❌ FAILED: {test_file}")
        print(f"Error: {e}")
        print()
        failed.append(test_file)

print("=" * 60)
if failed:
    print(f"❌ {len(failed)} test file(s) failed:")
    for f in failed:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("✅ All tests passed!")
    sys.exit(0)
