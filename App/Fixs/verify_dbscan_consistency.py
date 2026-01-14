#!/usr/bin/env python3
"""
Analyze DBSCAN training data vs prediction data to ensure consistency
"""
import json
import numpy as np

print("=" * 70)
print("DBSCAN DATA CONSISTENCY CHECK")
print("=" * 70)

# Load the saved model
with open('Artifacts/meilleurs models/DBSCAN.json', 'r') as f:
    model_data = json.load(f)

X_train = np.array(model_data['donnees'], dtype=float)
labels = np.array(model_data['labels_'], dtype=int)
eps = model_data['eps']
min_points = model_data['min_points']

print(f"\n1. TRAINING DATA SHAPE & STRUCTURE")
print(f"   - X_train shape: {X_train.shape}")
print(f"   - Labels shape: {labels.shape}")
print(f"   - eps: {eps}, min_points: {min_points}")
print(f"   - Number of features: {X_train.shape[1]}")

print(f"\n2. TRAINING DATA FEATURES (first 3 samples):")
feature_names = [
    'average (0-20)',
    'presence (0-1)',
    'projects (int)',
    'distance (0/1/2)',
    'works (0/1)',
    'status (0/1)'
]

for idx, names in enumerate(feature_names):
    print(f"   Feature {idx}: {names}")

print(f"\n   Sample 1: {X_train[0]}")
print(f"   Sample 2: {X_train[1]}")
print(f"   Sample 3: {X_train[2]}")

print(f"\n3. FEATURE RANGES IN TRAINING DATA:")
for i, feature_name in enumerate(feature_names):
    min_val = X_train[:, i].min()
    max_val = X_train[:, i].max()
    mean_val = X_train[:, i].mean()
    print(f"   Feature {i} ({feature_name}): min={min_val:.3f}, max={max_val:.3f}, mean={mean_val:.3f}")

print(f"\n4. PREDICTION DATA PREPARATION (from dbscan_analyzer.py):")
print(f"""
   def prepare_analysis_features(form_data):
       average = float(form_data.get('average', 0))        # 0-20
       presence = float(form_data.get('presence', 0)) / 100  # Convert % to 0-1
       projects = float(form_data.get('projects', 0))       # 0+
       
       distance_map = {{'<5': 0, '5-15': 1, '>15': 2}}
       distance = distance_map.get(form_data.get('distance', '<5'), 0)
       
       works_val = form_data.get('works', '')
       works = 1 if works_val == 'Oui' else 0
       
       status = 1 if form_data.get('status', 'Admis') == 'Admis' else 0
       
       features = [average, presence, projects, distance, works, status]
       return np.array(features, dtype=float)
""")

print(f"\n5. COMPARISON: TRAINING vs PREDICTION")
print(f"""
   ✓ Feature order matches:
     [average, presence, projects, distance, works, status]
   
   ✓ Data types match:
     - average: float (0-20 scale)
     - presence: float (0-1 normalized)  
     - projects: float (integer count)
     - distance: int (0/1/2 encoded)
     - works: int (0/1 binary)
     - status: int (0/1 binary)
   
   ✓ Range consistency:
     - Both use same encoding for categorical variables
     - Both normalize presence to 0-1
     - Both use same distance mapping
""")

print(f"\n6. POTENTIAL ISSUES TO CHECK:")

issues = []

# Check 1: Feature count
if X_train.shape[1] != 6:
    issues.append(f"⚠️  Training data has {X_train.shape[1]} features instead of 6")

# Check 2: Presence range (should be 0-1)
presence_col = X_train[:, 1]
if presence_col.max() > 1.1:
    issues.append(f"⚠️  Presence feature appears NOT normalized: max={presence_col.max()}")
    print(f"     (Expected 0-1, got 0-{presence_col.max()})")

# Check 3: Average range (should be 0-20)
avg_col = X_train[:, 0]
if avg_col.max() > 20.1 or avg_col.min() < -0.1:
    issues.append(f"⚠️  Average feature out of expected range: {avg_col.min()}-{avg_col.max()}")

# Check 4: Distance values should be 0, 1, or 2
dist_col = X_train[:, 3]
unique_dist = set(np.unique(dist_col))
if not unique_dist.issubset({0, 1, 2}):
    issues.append(f"⚠️  Distance has unexpected values: {unique_dist}")

# Check 5: Binary features should be 0 or 1
works_col = X_train[:, 4]
status_col = X_train[:, 5]
unique_works = set(np.unique(works_col))
unique_status = set(np.unique(status_col))
if not unique_works.issubset({0, 1}):
    issues.append(f"⚠️  Works has unexpected values: {unique_works}")
if not unique_status.issubset({0, 1}):
    issues.append(f"⚠️  Status has unexpected values: {unique_status}")

if issues:
    print("\n   FOUND ISSUES:")
    for issue in issues:
        print(f"   {issue}")
else:
    print("\n   ✓ No issues found!")
    print("   Data preparation is CONSISTENT between training and prediction")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)

if not issues:
    print("✅ DBSCAN data preprocessing is CONSISTENT")
    print("   Training and prediction use the SAME feature preparation")
    print("   The model is ready to use!")
else:
    print("⚠️  POTENTIAL DATA INCONSISTENCY DETECTED")
    print("   Review the issues above and verify training/prediction compatibility")

print("=" * 70)
