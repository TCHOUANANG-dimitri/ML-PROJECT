# ✅ SYSTÈME DE RECOMMANDATION - INSTRUCTIONS DE TEST

## 🎯 Objectif
Tester que le système de recommandation de salles et d'enseignants fonctionne **100% correctement**.

---

## 🚀 DÉMARRAGE DU SERVEUR

### 1. Ouvrir un terminal PowerShell
```powershell
cd d:\ML-PROJECT\App
python manage.py runserver
```

### 2. Attendre le message:
```
Starting development server at http://127.0.0.1:8000/
```

### 3. Ouvrir un navigateur à:
```
http://localhost:8000/
```

---

## 📋 CHECKLIST DE TEST

### A. Navigation et affichage ✓
- [ ] La page se charge sans erreurs
- [ ] Le sidebar est visible avec 6 boutons de navigation
- [ ] Le bouton "Recommandation" (icône 🧠) existe

### B. Section Recommandation ✓
- [ ] Cliquer sur "Recommandation" affiche la page correcte
- [ ] Le formulaire s'affiche en haut sur toute la largeur
- [ ] Les champs suivants sont visibles:
  - [ ] Effectif estimé (input number)
  - [ ] Type de séance (dropdown: CM, TD, TP)
  - [ ] Besoin vidéoprojecteur (dropdown: OUI, NON)
  - [ ] Niveau (dropdown: 1, 2, 3, 4, 5)
  - [ ] Filière (dropdown - vide au départ)
  - [ ] Nom de la matière (dropdown - vide au départ)
  - [ ] Date/jour (input date)
  - [ ] Tranche horaire (dropdown: Matin, Après-midi)
- [ ] Un bouton "Prédire" bleu existe au bas du formulaire

### C. Sélection dynamique des matières ✓
- [ ] Sélectionner "Niveau 1" → Dropdown Filière reste vide
- [ ] Sélectionner "TRONC COMMUN" dans Filière
- [ ] **Vérification critique**: Le dropdown "Nom de la matière" se remplit automatiquement avec:
  - [ ] Mathématiques Générales I
  - [ ] Physique Générale I
  - [ ] Chimie Générale
  - [ ] Informatique de base
  - [ ] Algèbre Linéaire
  - [ ] etc.

**Tester avec une autre filière et niveau:**
- [ ] Sélectionner "Niveau 3" → "GIT"
- [ ] Les matières changent vers:
  - [ ] Algorithmique Avancée
  - [ ] Bases de données
  - [ ] Réseaux et Protocoles
  - [ ] etc.

**Résultat attendu**: Les matières changent EN FONCTION du niveau ET de la filière sélectionnés.

### D. Prédiction et résultats ✓
Remplir le formulaire avec:
- Effectif: 30
- Type: CM
- Besoin projecteur: OUI
- Niveau: 3
- Filière: GIT
- Matière: (Algorithmique Avancée)
- Jour: (aujourd'hui)
- Heure: Matin

Cliquer "Prédire"

**Vérifications**:
- [ ] Pas d'erreur JavaScript (console F12 → Console)
- [ ] Les résultats apparaissent **EN BAS du formulaire**
- [ ] Il y a **2 colonnes**:
  - [ ] **Colonne gauche**: "🏫 Top 3 salles recommandées"
  - [ ] **Colonne droite**: "👨‍🏫 Top 3 enseignants recommandés"

### E. Affichage des recommandations ✓
**Colonne gauche (Salles)**:
- [ ] 3 salles affichées
- [ ] Chaque salle montre:
  - [ ] Nom/ID (ex: "A101")
  - [ ] Capacité
  - [ ] Présence de projecteur
  - [ ] Notation en étoiles (★★★★☆)
  - [ ] Score numérique
  - [ ] Bouton "Programmer"

**Colonne droite (Enseignants)**:
- [ ] 3 enseignants affichés
- [ ] Chaque enseignant montre:
  - [ ] Nom ou ID
  - [ ] Spécialité
  - [ ] Ancienneté
  - [ ] Notation en étoiles
  - [ ] Score numérique
  - [ ] Bouton "Programmer"

### F. Fonctionnalité des boutons "Programmer" ✓
Cliquer sur le premier bouton "Programmer" d'une salle

**Vérifications**:
- [ ] Une modal (fenêtre popup) s'affiche
- [ ] La modal montre:
  - [ ] Titre "Programmer salle"
  - [ ] Détails du cours:
    - Salle: (nom de la salle)
    - Matière: (matière sélectionnée)
    - Filière/Niveau: (valeurs)
    - Type: (CM/TD/TP)
    - Effectif: (nombre)
    - Date: (date sélectionnée)
  - [ ] Dropdown pour sélectionner le créneau:
    - [ ] "Matin (7:30 - 11:30)"
    - [ ] "Après-midi (12:30 - 16:30)"
  - [ ] Boutons "Annuler" et "Confirmer"

Sélectionner un créneau et cliquer "Confirmer"

**Vérifications**:
- [ ] Message de succès: "✓ Salle programmée avec succès!"
- [ ] La modal se ferme
- [ ] La page scroll vers la section "Emploi du temps"

### G. Emploi du temps ✓
- [ ] La section "Emploi du temps" apparaît
- [ ] Un tableau se affiche avec:
  - [ ] Lignes: Créneaux (AM, PM)
  - [ ] Colonnes: Jours (Lundi, Mardi, Mercredi, Jeudi, Vendredi, Samedi)
- [ ] Le cours qu'on vient de programmer s'affiche dans une cellule
- [ ] La cellule contient:
  - [ ] Le nom du cours
  - [ ] L'ID de la salle/enseignant

### H. Test supplémentaire - Enseignant ✓
Revenir à la section "Recommandation"
Remplir le même formulaire et cliquer "Prédire"
Cliquer sur "Programmer" d'un enseignant (colonne droite)

**Vérifications**:
- [ ] Modal s'affiche avec "Programmer enseignant"
- [ ] Les détails affichent le nom de l'enseignant
- [ ] Sélectionner un créneau et confirmer
- [ ] Message de succès: "✓ Enseignant programmé(e) avec succès!"

### I. Erreurs et gestion des cas ✓
- [ ] Soumettre le formulaire sans remplir les champs obligatoires
- [ ] Vérifier qu'un message d'erreur s'affiche
- [ ] Changer la filière et vérifier que les matières se mettent à jour
- [ ] Changer le niveau et vérifier que les matières se mettent à jour

### J. Console JavaScript ✓
Ouvrir F12 → Console
- [ ] Aucune erreur en rouge
- [ ] Aucun warning grave (les warnings normaux sont OK)

---

## 🎓 SCÉNARIO DE TEST COMPLET

### Scénario 1: Programmer une salle pour GIT N3
1. Niveau: 3
2. Filière: GIT
3. Matière: Algorithmique Avancée
4. Effectif: 45
5. Type: TP
6. Cliquer "Prédire"
7. Cliquer "Programmer" sur la première salle
8. Confirmer dans la modal
9. Vérifier que le cours apparaît dans l'emploi du temps

### Scénario 2: Programmer un enseignant pour SDIA N4
1. Niveau: 4
2. Filière: SDIA
3. Matière: Deep Learning
4. Effectif: 25
5. Type: CM
6. Cliquer "Prédire"
7. Cliquer "Programmer" sur le premier enseignant
8. Confirmer dans la modal
9. Vérifier qu'il apparaît dans l'emploi du temps

### Scénario 3: TRONC COMMUN Niveau 1-2
1. Niveau: 1
2. Filière: TRONC COMMUN
3. Matière: (Mathématiques Générales I)
4. Prédire
5. Vérifier les recommandations s'affichent

---

## ❌ TESTS DE VÉRIFICATION D'ERREURS

### Tests qui NE DOIVENT PAS ÉCHOUER:
- [ ] Cliquer "Prédire" sans effectif renseigné
- [ ] Cliquer "Programmer" sans remplir tout le formulaire
- [ ] Sélectionner une filière inexistante (impossible via dropdown)
- [ ] Rafraîchir la page (F5) - vérifier que l'app reste stable

---

## 📊 RÉSULTATS ATTENDUS

✅ **SUCCÈS** si:
- Les matières s'affichent correctement selon niveau + filière
- Les résultats s'affichent en 2 colonnes (salles à gauche, enseignants à droite)
- Les boutons "Programmer" ouvrent une modal
- L'emploi du temps se met à jour après confirmation
- Aucune erreur JavaScript en console

❌ **ÉCHEC** si:
- Les matières ne changent pas quand on change de filière/niveau
- Les résultats ne s'affichent pas du tout
- Les boutons "Programmer" ne répondent pas
- Des erreurs rouges apparaissent en console F12
- L'emploi du temps ne se met pas à jour

---

## 🆘 DÉPANNAGE

### Si les matières ne s'affichent pas:
1. Ouvrir F12 → Console
2. Vérifier qu'il n'y a pas d'erreur `undefined`
3. Taper: `console.log(MATIERES_BY_LEVEL)` pour voir les données
4. Vérifier qu'on a bien sélectionné une filière ET un niveau

### Si les résultats ne s'affichent pas:
1. Vérifier en F12 → Network que la requête POST vers `/recommendation/` a un statut 200
2. Vérifier le contenu de la réponse (onglet Response)
3. Vérifier qu'il n'y a pas d'erreur Django en console serveur

### Si les boutons ne répondent pas:
1. Ouvrir F12 → Console
2. Taper: `document.querySelectorAll('.program-btn').length` pour vérifier qu'il y a des boutons
3. Cliquer sur un bouton et vérifier qu'aucune erreur n'apparaît

---

## ✅ VALIDATION FINALE

Quand tous les tests passent:
1. ✅ Fermer le serveur (Ctrl+C)
2. ✅ Relire le fichier [FINAL_SUMMARY.md](FINAL_SUMMARY.md)
3. ✅ Confirmer que 100% des problèmes ont été résolus

**Le système est alors PRÊT POUR LA PRODUCTION!**

---

**Document créé**: 2024-01-XX  
**Système**: Recommandation de salles et d'enseignants  
**Statut**: Prêt pour test final  
**Prochaine étape**: Exécuter le test complet ci-dessus
