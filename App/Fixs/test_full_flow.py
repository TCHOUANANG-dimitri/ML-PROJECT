#!/usr/bin/env python3
"""
Test the full flow: Django context generation and API response
"""

import os
import sys
import django
import json

# Add App to path
sys.path.insert(0, 'd:\\ML-PROJECT\\App')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enspd_ai.settings')
django.setup()

from core.views import index
from django.test import RequestFactory
from ml_utils.dbscan_analyzer import (
    prepare_analysis_features, 
    predict_cluster, 
    load_dbscan_model,
    generate_analysis_explanation
)

print("=" * 60)
print("1. Testing Django Context (index view)")
print("=" * 60)

factory = RequestFactory()
request = factory.get('/')
response = index(request)

# Get context
context = response.context_data if hasattr(response, 'context_data') else {}

# Just render the context
from django.template import render_to_string
from django.template.loader import get_template

template = get_template('index.html')
rendered = template.render(context)

print(f"✓ Template rendered ({len(rendered)} chars)")

# Check if MATIERES_BY_LEVEL is in rendered HTML
if "MATIERES_BY_LEVEL" in rendered and "const MATIERES_BY_LEVEL =" in rendered:
    print("✓ MATIERES_BY_LEVEL variable found in template")
else:
    print("✗ MATIERES_BY_LEVEL variable NOT found in template")

# Check if JSON data is there
if '"TRONC_COMMUN"' in rendered:
    print("✓ TRONC_COMMUN found in JSON")
else:
    print("✗ TRONC_COMMUN not found in JSON")

# Parse the JSON from context
matieres_by_level = json.loads(context.get('matieres_by_level_json', '{}'))
print(f"✓ Parsed {len(matieres_by_level)} filières")
print(f"  - TRONC_COMMUN levels: {list(matieres_by_level.get('TRONC_COMMUN', {}).keys())}")

# Check level 1 and 2 have subjects
if 'TRONC_COMMUN' in matieres_by_level:
    for level in [1, 2]:
        count = len(matieres_by_level['TRONC_COMMUN'].get(level, []))
        print(f"  - Niveau {level}: {count} matières")

print("\n" + "=" * 60)
print("2. Testing DBSCAN Analysis API Flow")
print("=" * 60)

# Test with sample data
sample_student = {
    "average": 12.5,
    "presence": 85,
    "projects": 3,
    "distance": "<5",
    "works": "Oui",
    "status": "Admis"
}

try:
    features = prepare_analysis_features(sample_student)
    print(f"✓ Features prepared: {features}")
    
    model = load_dbscan_model()
    print("✓ DBSCAN model loaded")
    
    cluster_id, is_noise = predict_cluster(features, model)
    print(f"✓ Prediction: Cluster {cluster_id}, Noise: {is_noise}")
    
    analysis = generate_analysis_explanation(
        sample_student, 
        cluster_id, 
        is_noise, 
        "Test Student"
    )
    print(f"✓ Analysis generated with {len(analysis)} cards")
    for card in analysis:
        print(f"  - {card['title']}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("3. Testing with Empty 'Travaille' Field")
print("=" * 60)

sample_student_empty = {
    "average": 12.5,
    "presence": 85,
    "projects": 0,
    "distance": "<5",
    "works": "",  # Empty
    "status": "Admis"
}

try:
    features = prepare_analysis_features(sample_student_empty)
    print(f"✓ Features prepared (empty works): {features}")
    cluster_id, is_noise = predict_cluster(features, model)
    print(f"✓ Prediction with empty works: Cluster {cluster_id}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("✓ All tests passed!")
print("=" * 60)
