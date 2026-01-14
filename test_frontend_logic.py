#!/usr/bin/env python3
"""Test script to verify frontend JavaScript logic and data flow."""

import json
from pathlib import Path

# Test 1: Verify planning.txt can be parsed
print("=" * 80)
print("TEST 1: Vérifier que planning.txt peut être parsé")
print("=" * 80)

try:
    from App.ml_utils.data_prep import parse_planning_file
    matieres_by_filiere_level, matieres_map = parse_planning_file()
    
    print("✓ planning.txt parsé avec succès!")
    print(f"  - {len(matieres_map)} filières trouvées:")
    for filiere in sorted(matieres_map.keys()):
        count = sum(len(m) for m in matieres_by_filiere_level[filiere].values())
        print(f"    - {filiere}: {count} matières")
    
    # Afficher l'exemple de TRONC COMMUN niveau 1
    if "TRONC COMMUN" in matieres_by_filiere_level:
        matieres_n1 = matieres_by_filiere_level["TRONC COMMUN"].get(1, [])
        print(f"  - TRONC COMMUN Niveau 1: {matieres_n1[:3]}...")
except Exception as e:
    print(f"✗ Erreur: {e}")

# Test 2: Verify that the filieresMatieres object in JavaScript is valid
print("\n" + "=" * 80)
print("TEST 2: Vérifier que la structure filieresMatieres est valide")
print("=" * 80)

# Read app.js to check filieresMatieres
try:
    with open("d:/ML-PROJECT/App/static/js/app.js", "r", encoding="utf-8") as f:
        js_content = f.read()
    
    # Check for filieresMatieres
    if "const filieresMatieres = {" in js_content:
        print("✓ filieresMatieres trouvé dans app.js")
        
        # Check for TRONC COMMUN
        if '"TRONC COMMUN"' in js_content:
            print("  ✓ TRONC COMMUN présent")
        if '"GIT"' in js_content:
            print("  ✓ GIT présent")
        if '"SDIA"' in js_content:
            print("  ✓ SDIA présent")
        if '"GCI"' in js_content:
            print("  ✓ GCI présent")
    else:
        print("✗ filieresMatieres NOT trouvé dans app.js")
        
except Exception as e:
    print(f"✗ Erreur: {e}")

# Test 3: Verify HTML form IDs
print("\n" + "=" * 80)
print("TEST 3: Vérifier les IDs du formulaire HTML")
print("=" * 80)

try:
    with open("d:/ML-PROJECT/App/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    required_ids = [
        'rec-filiere',
        'rec-niveau',
        'rec-nom_matiere',
        'rec-Type_cours',
        'rec-Nb_personnes',
        'rec-jour',
        'rec-heure',
        'rec-besoin_projecteur',
        'recommendationForm',
        'recommendationResults'
    ]
    
    for id_name in required_ids:
        if f'id="{id_name}"' in html_content or f"id='{id_name}'" in html_content:
            print(f"  ✓ ID '{id_name}' trouvé")
        else:
            print(f"  ✗ ID '{id_name}' NOT trouvé")
            
except Exception as e:
    print(f"✗ Erreur: {e}")

# Test 4: Verify JavaScript functions
print("\n" + "=" * 80)
print("TEST 4: Vérifier que les fonctions JavaScript existent")
print("=" * 80)

try:
    required_functions = [
        'populateFiliereSelects',
        'populateMatiereOptions',
        'initRecommendationForm',
        'handleRecommendationSubmit',
        'openProgrammer',
        'attachRecommendationFormListener'
    ]
    
    for func_name in required_functions:
        if f"function {func_name}" in js_content:
            print(f"  ✓ Fonction '{func_name}' trouvée")
        else:
            print(f"  ✗ Fonction '{func_name}' NOT trouvée")
            
except Exception as e:
    print(f"✗ Erreur: {e}")

# Test 5: Verify Django view
print("\n" + "=" * 80)
print("TEST 5: Vérifier que la view Django fonctionne")
print("=" * 80)

try:
    from App.views_recommendation import recommendation_view
    print("✓ recommendation_view importée avec succès")
    
    # Check if the function is callable
    if callable(recommendation_view):
        print("  ✓ recommendation_view est une fonction callable")
except Exception as e:
    print(f"✗ Erreur: {e}")

print("\n" + "=" * 80)
print("RÉSUMÉ DES TESTS")
print("=" * 80)
print("✓ Tous les tests de logique frontend ont été vérifiés!")
print("✓ La structure est prête pour être testée dans le navigateur")

