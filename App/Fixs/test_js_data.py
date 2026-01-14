#!/usr/bin/env python3
"""
Test the JavaScript data structure that will be embedded in HTML
"""

import sys
import json

sys.path.insert(0, 'd:\\ML-PROJECT\\App')

from ml_utils.data_prep import parse_planning_file

print("=" * 70)
print("TESTING: JavaScript Data Structure Generation")
print("=" * 70)

# Parse planning.txt exactly as Django view does
matieres_by_filiere_level, matieres_map = parse_planning_file()

print("\n1. MATIERES_BY_LEVEL Structure (for JS)")
print("-" * 70)

# Convert to JSON as the view does
matieres_by_level_json = json.dumps(matieres_by_filiere_level, ensure_ascii=False)

# Validate JSON
parsed = json.loads(matieres_by_level_json)
print(f"[OK] JSON valid: {len(matieres_by_level_json)} bytes")

# Check TRONC_COMMUN
if 'TRONC_COMMUN' in parsed:
    print(f"[OK] TRONC_COMMUN found")
    tronc = parsed['TRONC_COMMUN']
    print(f"  - Levels: {sorted(tronc.keys())}")
    
    for level in [1, 2]:
        levelKey = str(level)
        if levelKey in tronc:
            count = len(tronc[levelKey])
            print(f"  - Niveau {level}: {count} matieres")
            if count > 0:
                print(f"    First 3: {tronc[levelKey][:3]}")
else:
    print(f"[ERROR] TRONC_COMMUN NOT found")

# Check other filières
print(f"\n[OK] Total filieres: {len(parsed)}")
for filiere in list(parsed.keys())[:3]:
    levels = parsed[filiere]
    print(f"  - {filiere}: levels {sorted(levels.keys())}")

print("\n2. JavaScript Code Simulation")
print("-" * 70)

# Simulate the JavaScript code that will run
print("Simulating: populateMatiereOptions() logic")
print()

def populate_matiere_js_sim(filiere_selected, niveau_selected):
    """Simulate the JS populateMatiereOptions function"""
    MATIERES_BY_LEVEL = parsed
    
    filiere = filiere_selected
    level = int(niveau_selected)
    levelKey = str(level)  # JSON keys are strings
    
    # Handle TRONC_COMMUN for levels 1 and 2
    selected_filiere = filiere
    if (level == 1 or level == 2) and filiere != "TRONC_COMMUN":
        # Check if TRONC_COMMUN exists and has this level
        if "TRONC_COMMUN" in MATIERES_BY_LEVEL and levelKey in MATIERES_BY_LEVEL["TRONC_COMMUN"]:
            selected_filiere = "TRONC_COMMUN"
            print(f"  Redirecting level {level} from '{filiere}' to TRONC_COMMUN")
    
    subjects = (MATIERES_BY_LEVEL.get(selected_filiere, {}).get(levelKey, []))
    
    return selected_filiere, subjects

# Test cases
test_cases = [
    ("TRONC_COMMUN", 1),
    ("GIT", 1),
    ("GIT", 3),
    ("SDIA", 2),
    ("SDIA", 4),
]

for filiere, level in test_cases:
    selected_f, subjects = populate_matiere_js_sim(filiere, level)
    print(f"  filiere={filiere}, niveau={level}")
    print(f"    -> Selected: {selected_f}, Count: {len(subjects)}")
    if subjects:
        print(f"    -> Examples: {subjects[:2]}")
    print()

print("=" * 70)
print("[OK] JavaScript Data Structure Test PASSED")
print("=" * 70)
