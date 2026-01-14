# Copilot Instructions: ENSPD AI Recommendation System

## Project Overview

This is a **Django-based academic resource recommendation system** that integrates ML models for intelligent scheduling and resource optimization. It predicts optimal room-teacher pairings for courses and provides academic dashboards.

### Architecture

```
App/              → Django monolithic app (views, models, templates)
├── core/         → Main Django app (index, API endpoints, models)
├── enspd_ai/     → Django config (settings, urls, wsgi)
├── ml_utils/     → ML integration layer (model loading, predictions)
├── static/       → Frontend (JS, CSS)
└── templates/    → HTML templates

Models/           → Custom ML model implementations (notebooks-derived)
├── optimisation des ressources/  → Room/resource optimization models
└── prediction performance/        → Teacher performance & room classification

Training&Saving/  → Jupyter notebooks and model training scripts
Datasets/         → CSV data sources (students, teachers, courses, resources)
Artifacts/        → Serialized trained models (JSON format)
```

## Critical Data Flows

### 1. Room-Teacher Recommendation Flow
- **Entry**: `views_recommendation.py::recommendation_view()` (POST form submission)
- **Data Parsing**: `data_prep.parse_planning_file()` → filieres/matieres from `planning.txt`
- **ML Prediction**: `predictor.predict_top_rooms_and_teachers()` → uses Decision Tree + Gradient Boosting
- **Feature Engineering**: `data_prep.prepare_resources()` applies notebooks logic (equipment adequacy, occupancy rate)
- **Output**: JSON with top 3 rooms + top 3 teachers, rendered to same page (no reload)

### 2. Data Source Structure
- **planning.txt**: Master subject/level/filiere mapping (parsed as tab-delimited tables)
- **Datasets/Resources.csv**: Room metadata (name, capacity, video projector, type)
- **Datasets/teachers.csv**: Teacher info (matricule, specialty, available hours)
- **Datasets/courses.csv**: Course definitions (subject, level, hours)

### 3. Model Loading Pattern
- Models are loaded **once at module import** in `views_recommendation.py` (lazy-load inefficiency—consider caching)
- Custom classes imported from `Models/` subfolders via dynamic sys.path manipulation in `predictor._ensure_models_on_path()`
- Models serialized as JSON; deserialization handled by custom `load()` methods

## Key Development Patterns

### Django-ML Integration
- **Dual-layer approach**: Core Django models (`Room`, `Teacher`, `TimetableEntry`) store scheduled data; ML models predict optimal assignments
- **Model path resolution**: All paths computed relative to project root via `_project_root()` helper—use consistently
- **Config in settings.py**: Minimal setup (SQLite, single app `core`, no auth, French localization)

### Feature Engineering (Critical)
Reference `data_prep.prepare_resources()` when adding room/teacher features:
- **besoin_projecteur** logic depends on `Type_cours` + `Filiere` combinations
- **taux_occupation** = attendees / capacity (continuous 0-1)
- **adequation_equipement**: Binary scoring (1 = match, 0.5 = acceptable, 0 = mismatch)
- **adequation_salle**: Lab vs classroom distinction (TP → Labo, CM/TD → Salle)

### API Pattern
- Endpoints in `core/views.py` use `@require_POST`, `@csrf_exempt` for JSON
- Return `JsonResponse` with keys like `"rooms": [], "teachers": [], "errors": []`
- Form data from `request.POST` (form-encoded) or `request.body.decode("utf-8")` (JSON)

## File-Specific Conventions

### planning.txt
- **Format**: Tab-delimited tables with "TRONC COMMUN" and "FILIÈRE [CODE]" section headers
- **Parsing**: `data_prep.parse_planning_file()` returns 2 dicts:
  - `matieres_by_filiere_level`: `{filiere: {level: [subjects]}}`
  - `matieres_map`: `{filiere: [subjects]}`
- **When modifying**: Ensure headers match parser regex; test with `parse_planning_file()`

### Model Serialization
- Custom classes must implement `load(path)` method or be JSON-serializable
- Path hints in `predictor.py`: Decision Tree loaded from `Training&Saving/decision_tree_class_model.json`
- **Do NOT rely on pickle**—use JSON for cross-environment compatibility

## Common Issues & Fixes

### "Matières not displaying" (Recommendation page)
- Add **filiere dropdown** in recommendation.html
- Pass `matieres_by_level_json` context from view
- Client-side: listen for filiere change → filter `matieres_by_level[filiere][niveau]`

### Page reload on predict button
- Prevent default form submission with `event.preventDefault()`
- Make async fetch POST to API endpoint
- Display results in DOM element below form (no redirect)

### Teacher hours not updating
- After `TimetableEntry.save()`: decrement `Teacher.hours_done` by session duration
- Persist via `teacher.save()`
- Validate `hours_remaining` property on frontend

### Timetable slot conflicts
- `TimetableEntry.Meta.unique_together` enforces per-room and per-teacher one course per (day, slot)
- Query: `TimetableEntry.objects.filter(room=r, day=d, slot=s).exists()`

## Frontend Stack Notes

- **Entry template**: `templates/index.html` or `templates/recommendation.html`
- **Static assets**: `static/js/{app.js, student-import.js, teacher-import.js, timetable.js}`
- **CSS**: `static/css/styles.css`
- **Context passing**: Django template tags `{{ matieres_json | safe }}` for JSON data

## Workflow Commands

```bash
# Setup
python App/manage.py migrate
python App/manage.py runserver

# Load sample data
python App/manage.py shell
>>> from core.models import Room, Teacher, Filiere, Subject
>>> Room.objects.create(name="A101", capacity=50)
```

## When Implementing Features

1. **Check planning.txt structure** if modifying matieres/filieres logic
2. **Run `parse_planning_file()` manually** to validate parsing
3. **Feature engineering changes**: Mirror logic in `prepare_resources()` + model retraining
4. **API endpoints**: Always use `JsonResponse` + error keys in response dict
5. **Model predictions**: Call `predict_top_rooms_and_teachers()`, not models directly
6. **No page reloads**: Use fetch + DOM updates for all dynamic interactions

## Known Limitations

- Single JSON model deserialization; no pickle or versioning
- planning.txt is hardcoded source of truth for subjects/levels
- No user authentication (DEBUG=True in production config)
- ML models path resolution assumes fixed folder layout
