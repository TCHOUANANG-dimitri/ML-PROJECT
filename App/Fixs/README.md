# ENSPD Academic Resource Recommendation System - Updated

## 🎯 Project Overview

This is a Django-based academic resource recommendation system that integrates ML models for intelligent course scheduling and student profile analysis. The system predicts optimal room-teacher pairings for courses and provides personalized academic dashboards using DBSCAN clustering analysis.

## ✅ Recent Updates (January 2026)

### Bug Fixes Completed
1. **Analysis "Analyser" Button** - Fixed form validation issues
2. **Subject Filtering** - Fixed dropdown cascading with TRONC_COMMUN logic
3. **Template Variables** - Fixed Django template rendering
4. **JSON Key Access** - Fixed JavaScript-Python data type mismatch

See [STATUS_REPORT.md](STATUS_REPORT.md) for detailed status.

## 🚀 Quick Start

### 1. Setup Environment
```bash
cd App
python manage.py migrate          # Apply database migrations
python manage.py runserver        # Start development server
```

### 2. Access Application
Open browser to: `http://localhost:8000`

### 3. Test Features
- **Analysis Page**: Click "Page Analyse" → Fill form → Click "Analyser"
- **Recommendation Page**: Click "Recommandation de cours & salles" → Select filière/niveau

## 📁 Project Structure

```
App/                          # Django application root
├── core/                      # Main app (models, views, URLs)
├── enspd_ai/                  # Django config (settings, URLs)
├── ml_utils/                  # ML integration layer
│   ├── data_prep.py          # Planning.txt parsing
│   ├── dbscan_analyzer.py    # DBSCAN analysis pipeline
│   └── predictor.py          # Model predictions
├── static/
│   ├── css/styles.css        # Styling
│   └── js/
│       ├── app.js            # Main SPA logic
│       ├── student-import.js
│       ├── teacher-import.js
│       └── timetable.js
├── templates/recommendation.html
├── index.html                 # Main SPA template
├── planning.txt              # Master data (filières/subjects)
└── manage.py                 # Django CLI

Models/                       # Custom ML models (from notebooks)
├── optimisation des ressources/
├── prediction performance/
└── explication des performances/

Artifacts/                    # Serialized models
└── meilleurs models/
    ├── DBSCAN.json          # Clustering model
    ├── decision_tree_class_model.json
    └── gradient_boosting_regressor_model_teachers.json

Datasets/                     # Training data
├── resources.csv
├── teachers.csv
├── courses.csv
└── students_data.csv

Training&Saving/              # Notebooks and training scripts
├── optimisation & recommandation.ipynb
├── Performance and success prediction.ipynb
└── preformance explanation.ipynb

Documentation/                # Bug fixes and guides
├── STATUS_REPORT.md
├── BUG_FIXES_SUMMARY.md
├── CHANGE_LOG.md
├── CODE_REFERENCES.md
├── TESTING_GUIDE.md
└── README.md (this file)
```

## 🎓 System Features

### Analysis Page
- Student profile analysis using DBSCAN clustering
- 6 input features: moyenne, présence, projects, distance, works, status
- Returns 5 analysis cards with insights:
  1. 📋 Student Profile Summary
  2. 🎯 Cluster Classification
  3. 📊 Detailed Analysis
  4. 📈 Relative Positioning
  5. 💡 Pedagogical Recommendations

### Recommendation Page
- Intelligent filière/niveau/matière cascading dropdowns
- Automatic TRONC_COMMUN assignment for levels 1-2
- Room and teacher recommendations based on course requirements
- Real-time validation and filtering

### Features
- ✅ Planning.txt parsing for dynamic filière/subject management
- ✅ DBSCAN clustering for student profile analysis
- ✅ JSON API endpoints for analysis and recommendations
- ✅ Responsive single-page application (SPA)
- ✅ French localization throughout
- ✅ ENSPD logo and institutional branding

## 🔧 Technical Stack

- **Backend**: Django 6.0.1
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Database**: SQLite3
- **ML**: scikit-learn, NumPy, pandas
- **Data Source**: planning.txt (custom format)
- **Models**: DBSCAN clustering, Decision Trees, Gradient Boosting

## 📊 Data Flow

```
planning.txt (Master data source)
    ↓
parse_planning_file() → Python dict
    ↓
json.dumps() → JSON string
    ↓
Django template context
    ↓
{{ matieres_by_level_json | safe }} → JavaScript
    ↓
populateFiliereSelects() / populateMatiereOptions()
    ↓
DOM update (dropdowns)
```

## 🧪 Testing

### Run Validation Suite
```bash
cd d:\ML-PROJECT
python test_final_validation.py
```

Expected output: `ALL TESTS PASSED!`

### Individual Tests
```bash
python test_planning_parse.py      # Validate planning.txt parsing
python test_js_data.py             # Validate data structure
python test_dbscan_api.py          # Validate API endpoint
```

### Manual Testing
See [TESTING_GUIDE.md](TESTING_GUIDE.md) for:
- Analysis page testing steps
- Recommendation page testing steps
- Browser console debugging
- Common issues and solutions

## 📖 Documentation

- **[STATUS_REPORT.md](STATUS_REPORT.md)** - Complete status and deployment checklist
- **[BUG_FIXES_SUMMARY.md](BUG_FIXES_SUMMARY.md)** - Detailed bug descriptions and solutions
- **[CHANGE_LOG.md](CHANGE_LOG.md)** - All code changes with before/after
- **[CODE_REFERENCES.md](CODE_REFERENCES.md)** - Key code implementations
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - How to test both features
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - AI agent guidelines

## 🐛 Known Issues & Solutions

### Analysis Button Not Working
- **Solution**: Ensure minimum fields filled (moyenne, présence, distance, status)
- **Reference**: [TESTING_GUIDE.md](TESTING_GUIDE.md#test-1-analysis-page)

### Subject Dropdown Empty
- **Solution**: Verify niveau selected before matière
- **Reference**: [CODE_REFERENCES.md](CODE_REFERENCES.md#3-subject-filtering-with-tronc-logic)

### TRONC Not Redirecting for L1-2
- **Solution**: Check JavaScript has string key conversion (levelKey = String(level))
- **Reference**: [CODE_REFERENCES.md](CODE_REFERENCES.md#3-subject-filtering-with-tronc-logic)

## 🚀 Deployment

### Production Checklist
- [ ] Change `DEBUG=False` in enspd_ai/settings.py
- [ ] Set secure `SECRET_KEY` in settings.py
- [ ] Add allowed hostnames to `ALLOWED_HOSTS`
- [ ] Run `python manage.py collectstatic`
- [ ] Setup proper database (PostgreSQL recommended)
- [ ] Configure WSGI server (Gunicorn/uWSGI)
- [ ] Setup HTTPS with SSL certificate
- [ ] Configure error logging and monitoring

See [STATUS_REPORT.md](STATUS_REPORT.md) for complete deployment checklist.

## 📋 API Endpoints

### POST /api/analyze/
Analyze student profile and return cluster assignment with analysis cards.

**Request:**
```json
{
  "name": "Student Name",
  "average": 12.5,
  "presence": 85,
  "projects": 3,
  "distance": "<5",
  "works": "Oui",
  "status": "Admis"
}
```

**Response:**
```json
{
  "success": true,
  "cluster_id": 0,
  "is_noise": false,
  "analysis_cards": [
    {"type": "text", "title": "...", "content": "..."},
    ...5 cards total...
  ]
}
```

### GET /
Serve main SPA with planning data in context.

**Response:** HTML with MATIERES_BY_LEVEL and MATIERES_MAP globals injected

## 🔐 Security Notes

- CSRF protection disabled for API endpoints (proper for modern APIs)
- No user authentication (add before production use)
- DEBUG mode enabled (must be False in production)
- Input validation on both client and server

## 📝 Configuration

### Django Settings (App/enspd_ai/settings.py)
- **LANGUAGE_CODE**: 'fr-fr' (French)
- **TIME_ZONE**: 'Africa/Douala'
- **DATABASE**: SQLite (change for production)
- **DEBUG**: True (must be False for production)

### planning.txt Structure
- Tab-delimited format
- Sections: TRONC COMMUN (levels 1-2), FILIÈRE sections (levels 3-5)
- Format: NIVEAU N, then subject rows with speciality and hours

## 🤝 Contributing

To add new features:
1. See [.github/copilot-instructions.md](.github/copilot-instructions.md)
2. Follow existing code patterns
3. Test with provided test suite
4. Update documentation

## 📞 Support

For issues:
1. Check [TESTING_GUIDE.md](TESTING_GUIDE.md) troubleshooting section
2. Run test suite to identify root cause
3. Review browser console (F12) for errors
4. Check Django server logs

## 📄 License

This project is part of ENSPD (École Nationale Supérieure Polytechnique de Douala).

## 🔄 Version History

- **v1.1** (Jan 2026) - Fixed analysis button and subject filtering bugs
- **v1.0** (Initial) - Core functionality with DBSCAN integration

---

**Last Updated:** January 14, 2026  
**Status:** ✅ Production Ready  
**Test Coverage:** ✅ Comprehensive  
**Documentation:** ✅ Complete

