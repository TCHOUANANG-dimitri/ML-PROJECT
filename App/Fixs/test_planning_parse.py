#!/usr/bin/env python
import json
import sys
sys.path.insert(0, 'App')

from ml_utils.data_prep import parse_planning_file

matieres_by_filiere_level, matieres_map = parse_planning_file()

print("=== FILIÈRES ===")
for f in sorted(matieres_by_filiere_level.keys()):
    print(f"  {f}")

print("\n=== NIVEAUX par FILIÈRE ===")
for f in sorted(matieres_by_filiere_level.keys()):
    levels = sorted(matieres_by_filiere_level[f].keys())
    print(f"{f}: {levels}")

print("\n=== TRONC_COMMUN Niveaux 1 & 2 ===")
if "TRONC_COMMUN" in matieres_by_filiere_level:
    for level in [1, 2]:
        subjects = matieres_by_filiere_level["TRONC_COMMUN"].get(level, [])
        print(f"Niveau {level}: {len(subjects)} matières")
        for s in subjects[:3]:
            print(f"  - {s}")
        if len(subjects) > 3:
            print(f"  ... et {len(subjects)-3} autres")

print("\n=== STRUCTURE pour JS ===")
print(f"Total filières: {len(matieres_by_filiere_level)}")
print(f"Total matières (matieres_map): {sum(len(v) for v in matieres_map.values())}")

# Test JSON serialization
try:
    json_str = json.dumps(matieres_by_filiere_level, ensure_ascii=False)
    print(f"JSON size: {len(json_str)} bytes - OK")
except Exception as e:
    print(f"JSON error: {e}")
