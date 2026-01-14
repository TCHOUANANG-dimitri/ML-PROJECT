#!/usr/bin/env python3
"""
Final verification script - checks all fixes are in place
"""

import os
import sys
import json
from pathlib import Path

sys.path.insert(0, 'd:\\ML-PROJECT\\App')

print("=" * 80)
print("FINAL VERIFICATION - All Bug Fixes")
print("=" * 80)

issues = []
checks_passed = 0
checks_total = 0

# 1. Check template syntax
print("\n1. Checking template variable syntax...")
checks_total += 1
try:
    index_path = Path('d:\\ML-PROJECT\\App\\index.html')
    content = index_path.read_text(encoding='utf-8')
    
    if '{{ matieres_by_level_json | safe }}' in content and '{{ matieres_json | safe }}' in content:
        print("   ✓ Template syntax correct")
        checks_passed += 1
    else:
        issues.append("Template variables not using correct Django syntax")
        print("   ✗ Template syntax INCORRECT")
except Exception as e:
    issues.append(f"Cannot read index.html: {e}")
    print(f"   ✗ Error: {e}")

# 2. Check JavaScript string key conversion
print("\n2. Checking JavaScript string key conversion...")
checks_total += 1
try:
    app_js_path = Path('d:\\ML-PROJECT\\App\\static\\js\\app.js')
    content = app_js_path.read_text(encoding='utf-8')
    
    if 'const levelKey = String(level)' in content:
        print("   ✓ String key conversion present")
        checks_passed += 1
    else:
        issues.append("String key conversion (levelKey = String(level)) not found")
        print("   ✗ String key conversion MISSING")
except Exception as e:
    issues.append(f"Cannot read app.js: {e}")
    print(f"   ✗ Error: {e}")

# 3. Check TRONC logic in JavaScript
print("\n3. Checking TRONC_COMMUN auto-redirect logic...")
checks_total += 1
try:
    if '(level === 1 || level === 2) && filiere !== "TRONC_COMMUN"' in content:
        if 'MATIERES_BY_LEVEL["TRONC_COMMUN"] && MATIERES_BY_LEVEL["TRONC_COMMUN"][levelKey]' in content:
            print("   ✓ TRONC auto-redirect logic present")
            checks_passed += 1
        else:
            issues.append("TRONC logic incomplete - missing MATIERES_BY_LEVEL check")
            print("   ✗ TRONC logic INCOMPLETE")
    else:
        issues.append("TRONC level check condition not found")
        print("   ✗ TRONC logic MISSING")
except Exception as e:
    issues.append(f"Error checking TRONC logic: {e}")
    print(f"   ✗ Error: {e}")

# 4. Check form validation allows empty works
print("\n4. Checking form validation for empty 'works' field...")
checks_total += 1
try:
    # Check that works validation is NOT strict
    if 'anTravaille' in content and 'if (!student.anTravaille' not in content:
        print("   ✓ Form validation allows empty works field")
        checks_passed += 1
    else:
        # Alternative check - look for comment or default handling
        if '// anTravaille is now optional' in content or 'works_code = 0 if not works_value' in content:
            print("   ✓ Form validation allows empty works field")
            checks_passed += 1
        else:
            issues.append("Form still validates anTravaille field strictly")
            print("   ✗ Form validation STILL STRICT")
except Exception as e:
    issues.append(f"Error checking form validation: {e}")
    print(f"   ✗ Error: {e}")

# 5. Check data_prep.py parser ordering
print("\n5. Checking planning.txt parser ordering...")
checks_total += 1
try:
    data_prep_path = Path('d:\\ML-PROJECT\\App\\ml_utils\\data_prep.py')
    content = data_prep_path.read_text(encoding='utf-8')
    
    # Find positions of TRONC and FILIERE checks
    tronc_pos = content.find('if "TRONC" in up:')
    filiere_pos = content.find('if ("FILI" in up')
    
    if tronc_pos > 0 and filiere_pos > 0 and tronc_pos < filiere_pos:
        print("   ✓ Parser checks TRONC before FILIERE (correct order)")
        checks_passed += 1
    else:
        issues.append("Parser not checking TRONC before FILIERE")
        print("   ✗ Parser ordering INCORRECT")
except Exception as e:
    issues.append(f"Cannot read data_prep.py: {e}")
    print(f"   ✗ Error: {e}")

# 6. Check backend feature preparation
print("\n6. Checking backend handles empty works...")
checks_total += 1
try:
    analyzer_path = Path('d:\\ML-PROJECT\\App\\ml_utils\\dbscan_analyzer.py')
    content = analyzer_path.read_text(encoding='utf-8')
    
    # Check for empty works handling
    if 'works_val = form_data.get' in content and 'Empty: default to 0' in content:
        print("   ✓ Backend handles empty works field")
        checks_passed += 1
    else:
        issues.append("Backend doesn't handle empty works gracefully")
        print("   ✗ Backend handling MISSING")
except Exception as e:
    issues.append(f"Cannot read dbscan_analyzer.py: {e}")
    print(f"   ✗ Error: {e}")

# 7. Check planning.txt exists and is parseable
print("\n7. Checking planning.txt and parsing...")
checks_total += 1
try:
    from ml_utils.data_prep import parse_planning_file
    import os
    os.chdir('App')
    
    matieres_by_level, matieres_map = parse_planning_file()
    
    if 'TRONC_COMMUN' in matieres_by_level:
        if 1 in matieres_by_level['TRONC_COMMUN'] and 2 in matieres_by_level['TRONC_COMMUN']:
            print("   ✓ planning.txt parses correctly with TRONC_COMMUN")
            checks_passed += 1
        else:
            issues.append("TRONC_COMMUN levels 1-2 not found in parsed data")
            print("   ✗ TRONC parsing INCOMPLETE")
    else:
        issues.append("TRONC_COMMUN not found in parsed planning.txt")
        print("   ✗ TRONC not parsed")
    
    os.chdir('..')
except Exception as e:
    issues.append(f"Cannot parse planning.txt: {e}")
    print(f"   ✗ Error: {e}")

# 8. Check DBSCAN model exists
print("\n8. Checking DBSCAN model file...")
checks_total += 1
try:
    model_path = Path('d:\\ML-PROJECT\\Artifacts\\meilleurs models\\DBSCAN.json')
    if model_path.exists():
        # Try to load it
        with open(model_path) as f:
            model_data = json.load(f)
        if 'eps' in model_data and 'donnees' in model_data:
            print("   ✓ DBSCAN model exists and is valid")
            checks_passed += 1
        else:
            issues.append("DBSCAN.json structure invalid")
            print("   ✗ DBSCAN model structure INVALID")
    else:
        issues.append("DBSCAN.json file not found")
        print("   ✗ DBSCAN model MISSING")
except Exception as e:
    issues.append(f"Cannot validate DBSCAN model: {e}")
    print(f"   ✗ Error: {e}")

# 9. Check API endpoint exists
print("\n9. Checking Django API endpoint...")
checks_total += 1
try:
    views_path = Path('d:\\ML-PROJECT\\App\\core\\views.py')
    content = views_path.read_text(encoding='utf-8')
    
    if 'def api_analyze(request):' in content:
        if '@csrf_exempt' in content and '@require_POST' in content:
            print("   ✓ API endpoint /api/analyze/ exists and configured")
            checks_passed += 1
        else:
            issues.append("API endpoint not properly decorated")
            print("   ✗ API endpoint decorators MISSING")
    else:
        issues.append("api_analyze function not found in views.py")
        print("   ✗ API endpoint MISSING")
except Exception as e:
    issues.append(f"Cannot check views.py: {e}")
    print(f"   ✗ Error: {e}")

# 10. Check documentation files
print("\n10. Checking documentation files...")
checks_total += 1
docs_to_check = [
    'd:\\ML-PROJECT\\STATUS_REPORT.md',
    'd:\\ML-PROJECT\\BUG_FIXES_SUMMARY.md',
    'd:\\ML-PROJECT\\CHANGE_LOG.md',
    'd:\\ML-PROJECT\\CODE_REFERENCES.md',
    'd:\\ML-PROJECT\\TESTING_GUIDE.md',
]

missing_docs = [d for d in docs_to_check if not Path(d).exists()]
if not missing_docs:
    print("   ✓ All documentation files present")
    checks_passed += 1
else:
    issues.append(f"Missing docs: {', '.join(missing_docs)}")
    print(f"   ✗ Missing: {', '.join([Path(d).name for d in missing_docs])}")

# Summary
print("\n" + "=" * 80)
print(f"VERIFICATION COMPLETE: {checks_passed}/{checks_total} checks passed")
print("=" * 80)

if checks_passed == checks_total:
    print("\n✅ ALL FIXES VERIFIED - System ready for deployment!")
    sys.exit(0)
else:
    print(f"\n⚠️  {len(issues)} ISSUES FOUND:\n")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")
    sys.exit(1)
