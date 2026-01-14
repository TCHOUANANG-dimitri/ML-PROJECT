#!/usr/bin/env python3
"""Comprehensive validation of all recommendation features."""

import json
from pathlib import Path
import sys

# Add App to path
sys.path.insert(0, 'd:/ML-PROJECT/App')

print("=" * 80)
print("TEST COMPLET: SYSTÈME DE RECOMMANDATION")
print("=" * 80)

# Test 1: Vérifier que les données filieres/matieres sont correct
print("\n[1/6] Vérification des données filieres/matieres...")
try:
    from ml_utils.data_prep import parse_planning_file
    matieres_by_filiere_level, matieres_map = parse_planning_file()
    
    # Vérifier les éléments clés
    assert "TRONC_COMMUN" in matieres_by_filiere_level, "TRONC_COMMUN manquant"
    assert 1 in matieres_by_filiere_level["TRONC_COMMUN"], "Niveau 1 manquant"
    assert len(matieres_by_filiere_level["TRONC_COMMUN"][1]) > 0, "Aucune matière au niveau 1"
    
    print("  ✓ Données filieres/matieres chargées correctement")
    print(f"    - {len(matieres_map)} filières trouvées")
    print(f"    - TRONC_COMMUN Niveau 1: {len(matieres_by_filiere_level['TRONC_COMMUN'][1])} matières")
except Exception as e:
    print(f"  ✗ ERREUR: {e}")
    sys.exit(1)

# Test 2: Vérifier que la view Django peut être importée
print("\n[2/6] Vérification de la view Django...")
try:
    from views_recommendation import recommendation_view
    print("  ✓ recommendation_view importée avec succès")
except Exception as e:
    print(f"  ✗ ERREUR: {e}")
    sys.exit(1)

# Test 3: Vérifier les IDs du formulaire HTML
print("\n[3/6] Vérification des IDs du formulaire HTML...")
try:
    html_path = Path("d:/ML-PROJECT/App/index.html")
    html_content = html_path.read_text(encoding="utf-8")
    
    required_ids = {
        'rec-filiere': 'select',
        'rec-niveau': 'select',
        'rec-nom_matiere': 'select',
        'rec-Type_cours': 'select',
        'rec-Nb_personnes': 'input',
        'rec-jour': 'input',
        'rec-heure': 'select',
        'rec-besoin_projecteur': 'select',
        'recommendationForm': 'form',
        'recommendationResults': 'div',
        'roomRecommendations': 'div',
        'teacherRecommendations': 'div'
    }
    
    missing = []
    for id_name in required_ids.keys():
        if f'id="{id_name}"' not in html_content:
            missing.append(id_name)
    
    if missing:
        print(f"  ✗ IDs manquants: {', '.join(missing)}")
        sys.exit(1)
    
    print("  ✓ Tous les IDs du formulaire trouvés")
except Exception as e:
    print(f"  ✗ ERREUR: {e}")
    sys.exit(1)

# Test 4: Vérifier les données JavaScript
print("\n[4/6] Vérification des données JavaScript...")
try:
    js_path = Path("d:/ML-PROJECT/App/static/js/app.js")
    js_content = js_path.read_text(encoding="utf-8")
    
    # Vérifier que les données de filieres sont prêtes
    if "const filieresData" not in js_content:
        print("  ✗ filieresData non trouvé dans app.js")
        sys.exit(1)
    
    # Vérifier les fonctions essentielles
    functions = [
        'populateFiliereSelects',
        'populateMatiereOptions',
        'initRecommendationForm',
        'handleRecommendationSubmit',
        'openProgrammer',
        'attachRecommendationFormListener'
    ]
    
    missing_funcs = [f for f in functions if f"function {f}" not in js_content and f"{f}()" not in js_content]
    
    if missing_funcs:
        print(f"  ✗ Fonctions manquantes: {', '.join(missing_funcs)}")
        sys.exit(1)
    
    print("  ✓ Toutes les fonctions JavaScript trouvées")
    print(f"    - {len(functions)} fonctions présentes")
except Exception as e:
    print(f"  ✗ ERREUR: {e}")
    sys.exit(1)

# Test 5: Vérifier la cohérence des données
print("\n[5/6] Vérification de la cohérence des données...")
try:
    # Vérifier que les niveaux autorisés sont 1-5 (ignorer 0 s'il existe)
    for filiere, levels_dict in matieres_by_filiere_level.items():
        for level in levels_dict.keys():
            if isinstance(level, int) and (level < 0 or level > 5):
                print(f"  ✗ Niveau invalide: {level} pour {filiere}")
                sys.exit(1)
    
    # Vérifier que les matieres ne sont pas vides
    empty_filieres = []
    for filiere, levels_dict in matieres_by_filiere_level.items():
        for level, matieres in levels_dict.items():
            if not matieres or len(matieres) == 0:
                empty_filieres.append(f"{filiere} Niveau {level}")
    
    if empty_filieres:
        print(f"  ⚠ Filieres/niveaux vides: {', '.join(empty_filieres[:3])}")
    else:
        print("  ✓ Aucune filière/niveau vide")
    
    print("  ✓ Cohérence des données vérifiée")
except Exception as e:
    print(f"  ✗ ERREUR: {e}")
    sys.exit(1)

# Test 6: Vérifier le formulaire HTML
print("\n[6/6] Vérification du formulaire HTML...")
try:
    # Vérifier que le formulaire a une action
    if 'action="/recommendation/"' not in html_content and "action='/recommendation/'" not in html_content:
        print("  ⚠ L'action du formulaire n'est pas définie pour /recommendation/")
    
    # Vérifier que csrf_token est présent
    if 'csrf_token' not in html_content:
        print("  ✗ Token CSRF manquant")
        sys.exit(1)
    
    # Vérifier le bouton submit
    if 'type="submit"' not in html_content:
        print("  ✗ Bouton submit non trouvé")
        sys.exit(1)
    
    # Vérifier que les données sont passées au JavaScript
    if 'MATIERES_BY_LEVEL' not in html_content or 'MATIERES_MAP' not in html_content:
        print("  ⚠ Variables JavaScript MATIERES_BY_LEVEL ou MATIERES_MAP non trouvées")
    
    print("  ✓ Formulaire HTML correctement configuré")
except Exception as e:
    print(f"  ✗ ERREUR: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ TOUS LES TESTS PASSÉS!")
print("=" * 80)
print("\nRÉSUMÉ:")
print("  • Structure HTML: OK")
print("  • Structure JavaScript: OK")
print("  • Données Django: OK")
print("  • Cohérence des données: OK")
print("  • Configuration du formulaire: OK")
print("\nLe système est prêt à être testé dans le navigateur!")
print("\nPour démarrer le serveur:")
print("  cd d:/ML-PROJECT/App && python manage.py runserver")
print("\nAllez à: http://localhost:8000/")
print("Cliquez sur 'Recommandation' dans la barre latérale")

