#!/usr/bin/env python3
"""
Debug parsing logic - full trace
"""

import sys
import json

sys.path.insert(0, 'd:\\ML-PROJECT\\App')

from ml_utils.data_prep import parse_planning_file

# Parse planning.txt 
matieres_by_filiere_level, matieres_map = parse_planning_file()

# Debug test
print("=" * 70)
print("Testing the exact filiere names from MATIERES_BY_LEVEL")
print("=" * 70)

print("\nAll filiere keys:")
for f in sorted(matieres_by_filiere_level.keys()):
    print(f"  '{f}'")

# Find the GIT filiere
git_filiere = None
for f in matieres_by_filiere_level.keys():
    if 'GIT' in f:
        git_filiere = f
        break

if git_filiere:
    print(f"\n[OK] Found GIT: '{git_filiere}'")
    print(f"\nGIT levels and subjects:")
    for level in sorted(matieres_by_filiere_level[git_filiere].keys()):
        subjects = matieres_by_filiere_level[git_filiere][level]
        print(f"  Level {level}: {len(subjects)} subjects")
        for subj in subjects[:2]:
            print(f"    - {subj}")
else:
    print("[ERROR] GIT not found!")

# Now test what happens when we access with the raw string level vs string level
print("\n" + "=" * 70)
print("Testing JSON access with string vs int keys")
print("=" * 70)

# Convert to JSON like Django does
json_str = json.dumps(matieres_by_filiere_level, ensure_ascii=False)
parsed = json.loads(json_str)

# Test access
if git_filiere:
    print(f"\nAccessing with level as string:")
    for levelstr in ['3', '4', '5']:
        if levelstr in parsed[git_filiere]:
            count = len(parsed[git_filiere][levelstr])
            print(f"  Level {levelstr}: {count} subjects")
        else:
            print(f"  Level {levelstr}: NOT FOUND (keys available: {list(parsed[git_filiere].keys())})")
    
    print(f"\nAccessing with level as int:")
    for levelint in [3, 4, 5]:
        if levelint in parsed[git_filiere]:
            count = len(parsed[git_filiere][levelint])
            print(f"  Level {levelint}: {count} subjects")
        else:
            print(f"  Level {levelint}: NOT FOUND")
