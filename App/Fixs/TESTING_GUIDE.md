# Testing Guide - Analysis & Recommendation Features

## Quick Setup

1. **Start Django Server:**
```bash
cd App
python manage.py runserver 0.0.0.0:8000
```

2. **Open Browser:**
```
http://localhost:8000
```

---

## Test 1: Analysis Page ("Analyser" Button)

### Success Criteria
- Form accepts minimum input (moyenne, présence, status)
- "Analyser" button becomes clickable without selecting "Travaille"
- Clicking button shows analysis without page reload
- 5 analysis cards appear below form

### Test Steps

1. Click **"Page Analyse"** button (left sidebar)
2. Fill the form minimally:
   - **Nom**: Any text (or leave empty)
   - **Moyenne**: `12.5`
   - **Présence (%)**: `85`
   - **Nombre de projets**: Leave empty
   - **Distance domicile-école**: Select `<5km` or any option
   - **Travaille**: Leave empty (don't select anything)
   - **Statut**: Select `Admis`

3. Click **"Analyser"** button

### Expected Result
- Form data is sent to `/api/analyze/`
- 5 HTML cards appear below with:
  1. 📋 Profil de l'étudiant (student details)
  2. 🎯 Classification par cluster (cluster assignment)
  3. 📊 Analyse détaillée (detailed analysis)
  4. 📈 Positionnement relatif (relative position)
  5. 💡 Recommandations pédagogiques (recommendations)

### Possible Issues & Fixes

**Issue:** Button says "disabled" or won't click
- **Fix:** Make sure you filled `Moyenne`, `Présence`, `Distance`, and `Statut`
- **Fix:** Check browser console for JavaScript errors (F12 → Console)

**Issue:** Form reloads instead of showing results
- **Fix:** Form submission is prevented with `event.preventDefault()`
- **Check:** Ensure static/js/app.js loaded correctly

**Issue:** Analysis cards show errors
- **Fix:** Check Django server logs for DBSCAN model loading errors
- **Fix:** Verify Artifacts/meilleurs models/DBSCAN.json exists

---

## Test 2: Recommendation Page (Subject Filtering)

### Success Criteria
- Filière dropdown populates with all available options
- Niveau dropdown changes based on filière
- Matière dropdown auto-populates based on filière + niveau
- Levels 1-2 auto-redirect to TRONC_COMMUN subjects
- Levels 3+ show filière-specific subjects

### Test Steps

**Scenario A: Level 1-2 (TRONC_COMMUN)**

1. Click **"Recommandation de cours & salles"** button (left sidebar)
2. In the recommendation form:
   - Select **Filière**: `💻 GIT Génie Informatique et Télécoms)`
   - Select **Niveau**: `1`
   - Observe **Matière** dropdown

3. Expected result:
   - Matière dropdown shows TRONC subjects:
     - Mathématiques Générales I
     - Physique Générale I
     - Chimie Générale
     - ... etc

4. Now change **Niveau** to `2`
   - Matière should update to show TRONC level 2 subjects:
     - Mathématiques Générales II
     - Physique Générale II
     - ... etc

**Scenario B: Level 3+ (Filière-Specific)**

1. Keep **Filière**: `💻 GIT Génie Informatique et Télécoms)`
2. Select **Niveau**: `3`
3. Observe **Matière** dropdown

4. Expected result:
   - Matière dropdown shows GIT level 3 subjects:
     - Algorithmique Avancée
     - Bases de données
     - Réseaux et Protocoles
     - ... etc

5. Change **Niveau** to `4` or `5` - subjects should update accordingly

**Scenario C: Different Filière**

1. Select **Filière**: `🤖 SDIA Science des Données et IA)`
2. Select **Niveau**: `2`
3. Matière should show TRONC level 2 (automatic redirect)

4. Change **Niveau** to `3`
5. Matière should show SDIA level 3 subjects

### Expected Result
- Dropdown behavior matches above scenarios
- No errors in browser console
- Form fields are responsive

### Possible Issues & Fixes

**Issue:** Filière dropdown is empty
- **Fix:** Template not loading MATIERES_BY_LEVEL correctly
- **Check:** Browser console → View page source → Search for `MATIERES_BY_LEVEL =`
- **Fix:** Verify Django view passes `matieres_by_level_json` in context

**Issue:** Matière dropdown empty after selecting filière + niveau
- **Fix:** Check that niveau is selected before matière
- **Check:** Browser console for JavaScript errors
- **Fix:** Clear browser cache and reload (Ctrl+Shift+R)

**Issue:** Level 1-2 not redirecting to TRONC
- **Check:** Browser console → inspect `MATIERES_BY_LEVEL` object
- **Check:** Verify TRONC_COMMUN exists with levels '1' and '2'

---

## Browser Console Debugging

### Check if MATIERES_BY_LEVEL loaded
```javascript
// In browser console (F12):
console.log(MATIERES_BY_LEVEL);
console.log(Object.keys(MATIERES_BY_LEVEL));
console.log(MATIERES_BY_LEVEL.TRONC_COMMUN);
console.log(MATIERES_BY_LEVEL['TRONC_COMMUN']['1']);
```

### Check if functions exist
```javascript
console.log(typeof populateFiliereSelects);
console.log(typeof populateMatiereOptions);
console.log(typeof validateAnalysisForm);
```

### Manually trigger dropdown updates
```javascript
// After selecting filière and niveau in form
populateMatiereOptions();
```

---

## API Testing (cURL)

### Test Analysis Endpoint
```bash
curl -X POST http://localhost:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Student",
    "average": 12.5,
    "presence": 85,
    "projects": 3,
    "distance": "<5",
    "works": "",
    "status": "Admis"
  }'
```

Expected response:
```json
{
  "success": true,
  "cluster_id": 0,
  "is_noise": false,
  "analysis_cards": [
    {...5 cards...}
  ]
}
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Analyser" button disabled | Ensure minimum form fields filled |
| Form reloads on submit | Check static/js/app.js loaded and `event.preventDefault()` present |
| Empty matière dropdown | Verify JSON data loaded → Check console for MATIERES_BY_LEVEL |
| Analysis shows 404 error | Check Django server running on http://localhost:8000 |
| TRONC not redirecting for L1-2 | Check JavaScript has `levelKey = String(level)` conversion |
| Filière dropdown empty | Verify Django passed `matieres_by_level_json` to template |

---

## Success Checklist

- [ ] Analysis page loads without errors
- [ ] Form accepts incomplete input (empty "Travaille" field)
- [ ] "Analyser" button visible and clickable
- [ ] Clicking button doesn't reload page
- [ ] 5 analysis cards display after submission
- [ ] Recommendation page loads without errors
- [ ] Filière dropdown has options
- [ ] Niveau dropdown responds to filière selection
- [ ] Matière dropdown populates correctly
- [ ] Level 1-2 show TRONC subjects (any filière)
- [ ] Level 3+ show filière-specific subjects
- [ ] No errors in browser console
- [ ] No errors in Django server logs

