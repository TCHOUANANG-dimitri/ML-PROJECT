# Code References - Key Implementations

## 1. Template Variable Injection (Django → JavaScript)

### Location: App/index.html (Lines 147-149)
```javascript
<script>
  // MATIERES_BY_LEVEL and MATIERES_MAP provided by view as JSON strings
  const MATIERES_BY_LEVEL = {{ matieres_by_level_json | safe }};
  const MATIERES_MAP = {{ matieres_json | safe }};
```

### What it does:
- Receives JSON from Django context
- Makes data available to JavaScript globally
- Used by populateFiliereSelects() and populateMatiereOptions()

### Example data structure:
```javascript
{
  "TRONC_COMMUN": {
    "1": ["Mathématiques Générales I", "Physique Générale I", ...],
    "2": ["Mathématiques Générales II", "Physique Générale II", ...],
    "0": [...]
  },
  "💻  GIT Génie Informatique et Télécoms)": {
    "3": ["Algorithmique Avancée", "Bases de données", ...],
    "4": [...],
    "5": [...]
  }
}
```

---

## 2. Form Validation Logic

### Location: App/static/js/app.js (Lines 1162-1240)
```javascript
function validateAnalysisForm() {
  const student = {
    name: document.getElementById("anName").value.trim(),
    average: parseFloat(document.getElementById("anAverage").value),
    presence: parseInt(document.getElementById("anPresence").value, 10),
    projects: parseInt(document.getElementById("anProjects").value, 10) || 0,
    distance: document.getElementById("anDistance").value,
    works: document.getElementById("anTravaille").value, // Can be empty
    status: document.getElementById("anStatus").value
  };

  const errors = [];
  
  // Required fields
  if (!student.average || isNaN(student.average) || student.average < 0 || student.average > 20) {
    errors.push("Moyenne invalide (0-20)");
  }
  
  if (!student.presence || isNaN(student.presence) || student.presence < 0 || student.presence > 100) {
    errors.push("Présence invalide (0-100)");
  }
  
  if (!student.distance) {
    errors.push("Veuillez sélectionner la distance");
  }
  
  if (!student.status) {
    errors.push("Veuillez sélectionner le statut");
  }
  
  // works field is now OPTIONAL (allows empty string)
  
  return { valid: errors.length === 0, student, errors };
}
```

### Key change:
- Removed validation for `anTravaille` field
- No longer throws error if field is empty
- Backend defaults empty to 0 (no works)

---

## 3. Subject Filtering with TRONC Logic

### Location: App/static/js/app.js (Lines 376-415)
```javascript
function populateMatiereOptions() {
  const filiere = recFiliereSelect.value;
  const level = parseInt(recNiveauSelect.value, 10);
  const levelKey = String(level);  // KEY FIX: Convert to string for JSON access

  recMatiereSelect.innerHTML = '<option value="">Choisir une matière</option>';

  if (!filiere || !level) return;

  // KEY FIX: Handle TRONC_COMMUN for levels 1 and 2
  let selectedFiliere = filiere;
  if ((level === 1 || level === 2) && filiere !== "TRONC_COMMUN") {
    // Check if TRONC_COMMUN exists and has this level
    if (MATIERES_BY_LEVEL["TRONC_COMMUN"] && MATIERES_BY_LEVEL["TRONC_COMMUN"][levelKey]) {
      selectedFiliere = "TRONC_COMMUN";
      console.log(`Auto-redirecting level ${level} to TRONC_COMMUN`);
    }
  }

  // KEY FIX: Use levelKey (string) instead of level (integer)
  const subjects = (MATIERES_BY_LEVEL[selectedFiliere] && 
                   MATIERES_BY_LEVEL[selectedFiliere][levelKey]) || [];
  
  if (subjects.length === 0) {
    const emptyOpt = document.createElement("option");
    emptyOpt.value = "";
    emptyOpt.textContent = "Aucune matière disponible";
    emptyOpt.disabled = true;
    recMatiereSelect.appendChild(emptyOpt);
  } else {
    subjects.forEach((m) => {
      const opt = document.createElement("option");
      opt.value = m;
      opt.textContent = m;
      recMatiereSelect.appendChild(opt);
    });
  }
}

// Trigger updates when user changes filière or niveau
recFiliereSelect.addEventListener("change", populateMatiereOptions);
recNiveauSelect.addEventListener("change", populateMatiereOptions);
```

### Key fixes:
1. `String(level)` conversion for JSON key access
2. TRONC_COMMUN redirect for levels 1-2
3. Fallback to empty option if no subjects found

---

## 4. Analysis API Call

### Location: App/static/js/app.js (Lines 1242-1330)
```javascript
analyzeBtn.addEventListener("click", async (event) => {
  event.preventDefault();  // Prevent form submission
  
  const validation = validateAnalysisForm();
  
  if (!validation.valid) {
    alert("Erreurs:\n" + validation.errors.join("\n"));
    return;
  }
  
  const student = validation.student;
  
  // Prepare data for API
  const payload = {
    name: student.name || "Anonymous",
    average: student.average,
    presence: student.presence,
    projects: student.projects,
    distance: student.distance,
    works: student.works,  // Can be empty string
    status: student.status
  };
  
  try {
    const response = await fetch("/api/analyze/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    
    const result = await response.json();
    
    if (!result.success) {
      alert(`Erreur: ${result.error}`);
      return;
    }
    
    // Display analysis cards
    analysisResults.innerHTML = "";
    
    if (result.analysis_cards && result.analysis_cards.length > 0) {
      result.analysis_cards.forEach(card => {
        const cardDiv = document.createElement("div");
        cardDiv.className = "analysis-card";
        cardDiv.innerHTML = `
          <h3>${card.title}</h3>
          <p>${card.content}</p>
        `;
        analysisResults.appendChild(cardDiv);
      });
    }
    
    // Scroll to results
    analysisResults.scrollIntoView({ behavior: "smooth" });
    
  } catch (error) {
    alert(`Erreur de connexion: ${error.message}`);
  }
});
```

### Key features:
- `event.preventDefault()` prevents page reload
- Relaxed validation allows empty works
- Async fetch to API endpoint
- DOM update with analysis cards

---

## 5. Backend Feature Preparation

### Location: App/ml_utils/dbscan_analyzer.py (Lines 50-115)
```python
def prepare_analysis_features(student_dict):
    """
    Convert student form data to 6-element feature vector for DBSCAN
    
    Input: {average, presence, projects, distance, works, status}
    Output: numpy array [avg, pres/100, proj, dist_code, works_binary, status_binary]
    """
    try:
        # Average (0-20)
        average = float(student_dict.get("average", 0))
        
        # Presence (0-100, convert to 0-1)
        presence = float(student_dict.get("presence", 0)) / 100.0
        
        # Projects (count)
        projects = float(student_dict.get("projects", 0))
        
        # Distance (categorical → numeric)
        distance_str = student_dict.get("distance", "<5")
        distance_code = {
            "<5": 0,
            "5-15": 1,
            ">15": 2
        }.get(distance_str, 0)
        
        # Works field: Handle empty string (KEY FIX)
        works_value = student_dict.get("works", "")
        works_code = 0 if not works_value or works_value.lower() not in ["oui", "yes"] else 1
        
        # Status (categorical → numeric)
        status_str = student_dict.get("status", "Admis")
        status_code = 1 if status_str == "Admis" else 0
        
        # Create feature vector
        features = np.array([
            [average, presence, projects, distance_code, works_code, status_code]
        ], dtype=np.float32)
        
        return features.flatten()
        
    except Exception as e:
        print(f"Error preparing features: {e}")
        return None
```

### Key fix:
- Handles empty "works" value gracefully
- Defaults to 0 (no works) instead of crashing

---

## 6. Planning.txt Parser

### Location: App/ml_utils/data_prep.py (Lines 210-300)
```python
def parse_planning_file():
    matieres_by_filiere_level = {}
    current_filiere = None
    current_level = None

    with open(planning_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            up = line.upper()
            
            # KEY FIX: Detect 'TRONC' FIRST (before filière)
            if "TRONC" in up:
                current_filiere = "TRONC_COMMUN"
                matieres_by_filiere_level.setdefault(current_filiere, {})
                current_level = None
                continue
            
            # Then detect filière headings
            if ("FILI" in up and up.find("FILI") < 20) or ("FILIERE" in up) or ("FILIÈRE" in up):
                # Extract filière name (preserving emojis)
                cleaned = line
                for token in ["FILIERE", "FILIÈRE"]:
                    cleaned = cleaned.replace(token, "")
                cleaned = cleaned.strip()
                if cleaned:
                    current_filiere = cleaned
                    matieres_by_filiere_level.setdefault(current_filiere, {})
                    current_level = None
                continue

            # Detect level lines like 'NIVEAU 3'
            if up.startswith("NIVEAU") or up.startswith("NIV"):
                parts = line.split()
                lvl = None
                for p in parts:
                    if p.isdigit():
                        lvl = int(p)
                        break
                if lvl is not None:
                    current_level = int(lvl)
                    if current_filiere is None:
                        current_filiere = "TRONC_COMMUN"
                        matieres_by_filiere_level.setdefault(current_filiere, {})
                    matieres_by_filiere_level[current_filiere].setdefault(current_level, [])
                continue

            # Parse subject lines (tab-delimited)
            parts = [p.strip() for p in line.split("\t") if p.strip()]
            if len(parts) >= 2:
                matiere = parts[0]
                if matiere and current_level is not None:
                    fil = current_filiere or "TRONC_COMMUN"
                    matieres_by_filiere_level.setdefault(fil, {})
                    matieres_by_filiere_level[fil].setdefault(current_level, []).append(matiere)

    # Build map (filière → all subjects across all levels)
    matieres_map = {}
    for f, levels in matieres_by_filiere_level.items():
        seen = []
        for lvl in sorted(levels.keys()):
            for m in levels[lvl]:
                if m and m not in seen:
                    seen.append(m)
        matieres_map[f] = seen

    return matieres_by_filiere_level, matieres_map
```

### Key fix:
- TRONC_COMMUN detection happens BEFORE filière detection
- Prevents misclassification of TRONC sections as filière

---

## 7. Django View Context

### Location: App/core/views.py (Lines 16-30)
```python
def index(request):
    # Serve the SPA with planning data in context
    try:
        matieres_by_filiere_level, matieres_map = parse_planning_file()
    except Exception:
        matieres_by_filiere_level, matieres_map = {}, {}

    context = {
        "filieres": sorted(matieres_map.keys()),
        "matieres_json": json.dumps(matieres_map, ensure_ascii=False),
        "matieres_by_level_json": json.dumps(matieres_by_filiere_level, ensure_ascii=False),
    }
    return render(request, "index.html", context)
```

### What it does:
- Parses planning.txt on each request
- Converts to JSON for template rendering
- Makes data available to JavaScript

---

## Testing Commands

### Run all validation tests:
```bash
cd d:\ML-PROJECT
python test_final_validation.py
```

### Test planning.txt parsing:
```bash
python test_planning_parse.py
```

### Test JavaScript data structure:
```bash
python test_js_data.py
```

### Test API endpoint:
```bash
python test_dbscan_api.py
```

---

## Quick Reference: What Changed Where

| Feature | File | Lines | Change |
|---------|------|-------|--------|
| Template vars | index.html | 147-149 | Syntax fix `{{}}` |
| Form validation | app.js | 1162-1240 | Allow empty works |
| Subject filter | app.js | 376-415 | String keys + TRONC |
| Analysis API | app.js | 1242-1330 | Form data send |
| Feature prep | dbscan_analyzer.py | 50-115 | Handle empty works |
| Parser order | data_prep.py | 210-300 | TRONC before FILIERE |
| Django context | views.py | 16-30 | JSON dumps context |

---

**All code is production-ready and tested** ✅

