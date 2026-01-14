#!/usr/bin/env python3
"""
Debug the planning.txt parsing to see what's actually being extracted
"""

import sys
import json

sys.path.insert(0, 'd:\\ML-PROJECT\\App')

from ml_utils.data_prep import parse_planning_file

# Parse planning.txt 
matieres_by_filiere_level, matieres_map = parse_planning_file()

# Show GIT details
print("=" * 70)
print("GIT (Genie Informatique et Telecoms) Details")
print("=" * 70)

for filiere in matieres_by_filiere_level.keys():
    if 'GIT' in filiere or 'Informatique' in filiere:
        print(f"\nFiliere: {filiere}")
        levels = matieres_by_filiere_level[filiere]
        for level in sorted(levels.keys()):
            count = len(levels[level])
            print(f"  Level {level}: {count} subjects")
            if count > 0:
                for subj in levels[level][:3]:
                    print(f"    - {subj}")
                if count > 3:
                    print(f"    ... and {count - 3} more")
