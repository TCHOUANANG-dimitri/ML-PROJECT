"""
DBSCAN Model Loader and Analysis Generator
Loads the DBSCAN model from Artifacts and generates contextual explanations
"""
import json
import sys
import numpy as np
from pathlib import Path


def _project_root():
    """Return repository root"""
    return Path(__file__).resolve().parents[2]


def _ensure_models_on_path():
    """Add Models folder to sys.path to import custom classes"""
    root = _project_root()
    models_path = str(root / "Models" / "explication des performances")
    if models_path not in sys.path:
        sys.path.insert(0, models_path)


def load_dbscan_model(model_path=None):
    """Load DBSCAN model from JSON file"""
    _ensure_models_on_path()
    
    if model_path is None:
        root = _project_root()
        model_path = root / "Artifacts" / "meilleurs models" / "DBSCAN.json"
    
    try:
        from DBSCAN import DBSCAN
        
        dbscan = DBSCAN()
        model_path = Path(model_path)
        
        # Try to load from JSON if file exists
        if model_path.exists():
            try:
                # First try the built-in load() method
                dbscan.load(str(model_path))
                # The load() method sets X_ and labels_, but they may be lists, convert them
                if isinstance(dbscan.X_, list):
                    dbscan.X_ = np.array(dbscan.X_, dtype=float)
                if isinstance(dbscan.labels_, list):
                    dbscan.labels_ = np.array(dbscan.labels_, dtype=int)
            except Exception as load_error:
                # Fallback: manually parse JSON
                with open(model_path, 'r', encoding='utf-8') as f:
                    model_data = json.load(f)
                    # Handle different possible JSON structures
                    if isinstance(model_data, dict):
                        # Convert nested lists to numpy arrays
                        if 'X_' in model_data:
                            dbscan.X_ = np.array(model_data['X_'], dtype=float)
                        elif 'donnees' in model_data:
                            dbscan.X_ = np.array(model_data['donnees'], dtype=float)
                        
                        if 'labels_' in model_data:
                            dbscan.labels_ = np.array(model_data['labels_'], dtype=int)
                        
                        dbscan.eps = model_data.get('eps', 1)
                        dbscan.min_points = model_data.get('min_points', 5)
        
        return dbscan
    except Exception as e:
        print(f"Error loading DBSCAN model: {e}")
        import traceback
        traceback.print_exc()
        return None


def prepare_analysis_features(form_data):
    """
    Convert form data to feature vector for DBSCAN clustering
    
    Expected form fields:
    - name: Étudiant name/ID
    - average: Moyenne annuelle (0-20)
    - presence: Taux de présence (0-100)
    - projects: Nombre de projets (0+)
    - distance: Distance domicile-école ('<5', '5-15', '>15')
    - works: Travaille ('Oui' / 'Non' / empty)
    - status: Statut ('Admis' / 'Échec')
    """
    try:
        average = float(form_data.get('average', 0))
        presence = float(form_data.get('presence', 0)) / 100  # Convert % to 0-1
        projects = float(form_data.get('projects', 0))
        
        # Encode categorical variables
        distance_map = {'<5': 0, '5-15': 1, '>15': 2}
        distance = distance_map.get(form_data.get('distance', '<5'), 0)
        
        # Works: can be empty (infer as 0 by default) or explicit Oui/Non
        works_val = form_data.get('works', '')
        if works_val == 'Oui':
            works = 1
        elif works_val == 'Non':
            works = 0
        else:
            # Empty: default to 0 (not working)
            works = 0
        
        status = 1 if form_data.get('status', 'Admis') == 'Admis' else 0
        
        # Feature vector: [average, presence, projects, distance, works, status]
        features = [average, presence, projects, distance, works, status]
        return np.array(features, dtype=float)
    except Exception as e:
        print(f"Error preparing features: {e}")
        return None


def predict_cluster(student_features, dbscan_model):
    """
    Predict cluster for a single student using DBSCAN
    
    Returns:
    {
        'cluster_id': int or -1 (noise),
        'is_noise': bool,
        'distances_to_clusters': dict,
        'n_clusters': int,
        'cluster_sizes': dict
    }
    """
    if dbscan_model is None or dbscan_model.X_ is None:
        return {
            'error': 'Model not loaded',
            'cluster_id': -1,
            'is_noise': True
        }
    
    try:
        # Reshape to 2D array for consistency
        student = student_features.reshape(1, -1)
        
        # Find nearest neighbors in training data
        distances = []
        for i, training_point in enumerate(dbscan_model.X_):
            dist = np.sqrt(np.sum((student - training_point) ** 2))
            distances.append({
                'index': i,
                'distance': float(dist),
                'cluster_id': int(dbscan_model.labels_[i])
            })
        
        # Sort by distance
        distances.sort(key=lambda x: x['distance'])
        
        # Determine cluster assignment
        nearest = distances[0] if distances else None
        cluster_id = nearest['cluster_id'] if nearest else -1
        
        # Get cluster information
        unique_clusters = np.unique(dbscan_model.labels_)
        cluster_sizes = {
            int(cid): int(np.sum(dbscan_model.labels_ == cid))
            for cid in unique_clusters
        }
        
        return {
            'cluster_id': cluster_id,
            'is_noise': cluster_id == -1,
            'nearest_distance': float(nearest['distance']) if nearest else None,
            'top_k_neighbors': distances[:5],  # Top 5 nearest neighbors
            'n_clusters': int(len([c for c in unique_clusters if c != -1])),
            'cluster_sizes': cluster_sizes,
            'total_noise_points': int(cluster_sizes.get(-1, 0)),
            'features': {
                'average': float(student[0][0]),
                'presence': float(student[0][1]) * 100,
                'projects': float(student[0][2]),
                'distance': ['<5km', '5-15km', '>15km'][int(student[0][3])],
                'works': bool(int(student[0][4])),
                'status': 'Admis' if int(student[0][5]) == 1 else 'Échec'
            }
        }
    except Exception as e:
        print(f"Error predicting cluster: {e}")
        return {
            'error': str(e),
            'cluster_id': -1,
            'is_noise': True
        }


def generate_analysis_explanation(cluster_result, student_name):
    """
    Generate contextual explanation for cluster assignment
    
    Returns analysis cards with insights based on:
    - Student characteristics
    - Cluster composition
    - Comparison with cluster peers
    """
    cluster_id = cluster_result.get('cluster_id', -1)
    features = cluster_result.get('features', {})
    
    analysis_cards = []
    
    # Card 1: Profile Summary
    profile_text = f"""
    <strong>Profil étudiant analysé: {student_name}</strong><br/>
    • Moyenne annuelle: <strong>{features.get('average', '?'):.2f}/20</strong><br/>
    • Taux de présence: <strong>{features.get('presence', '?'):.1f}%</strong><br/>
    • Nombre de projets: <strong>{int(features.get('projects', 0))}</strong><br/>
    • Distance domicile-école: <strong>{features.get('distance', '?')}</strong><br/>
    • Travaille: <strong>{'Oui' if features.get('works') else 'Non'}</strong><br/>
    • Statut: <strong>{features.get('status', '?')}</strong>
    """
    
    analysis_cards.append({
        'type': 'text',
        'title': '📋 Profil de l\'étudiant',
        'content': profile_text
    })
    
    # Card 2: Cluster Assignment
    if cluster_id == -1:
        cluster_text = """
        <strong>🔴 Profil atypique détecté</strong><br/>
        Cet étudiant présente un profil <strong>unique</strong> qui ne correspond à aucun cluster prédéfini.
        Il s'agit d'un <strong>point de bruit</strong> dans l'analyse DBSCAN, indiquant une combinaison 
        de caractéristiques rarement observée.<br/><br/>
        <em>Cela peut signifier:</em><br/>
        • Une performance exceptionnelle ou atypique<br/>
        • Des facteurs externes influençant son parcours<br/>
        • Une situation nécessitant un suivi pédagogique personnalisé
        """
    else:
        cluster_sizes = cluster_result.get('cluster_sizes', {})
        cluster_size = cluster_sizes.get(cluster_id, 0)
        
        cluster_text = f"""
        <strong>🟢 Assigné au Cluster #{cluster_id}</strong><br/>
        Cet étudiant appartient à un groupe de <strong>{cluster_size} étudiants</strong> 
        partageant des caractéristiques similaires.<br/><br/>
        <em>Caractéristiques communes du cluster:</em>
        """
    
    analysis_cards.append({
        'type': 'text',
        'title': '🎯 Classification par cluster',
        'content': cluster_text
    })
    
    # Card 3: Detailed Explanation
    works = features.get('works', False)
    presence = features.get('presence', 0)
    average = features.get('average', 0)
    distance = features.get('distance', '?')
    projects = features.get('projects', 0)
    
    explanation_parts = []
    
    # Build contextual explanation
    if works and distance == '>15km':
        explanation_parts.append(
            "📌 <strong>Étudiant travailleur, vivant loin</strong>: "
            "Cette situation complique la conciliation études-travail et accroît la fatigue due aux trajets."
        )
    
    if presence < 75:
        explanation_parts.append(
            "⚠️ <strong>Taux de présence faible</strong>: "
            "Les absences répétées affectent l'assimilation des contenus et les performances académiques."
        )
    
    if average >= 15:
        explanation_parts.append(
            "✅ <strong>Excellente moyenne</strong>: "
            "Malgré les défis (travail, distance), cet étudiant démontre une forte capacité d'adaptation."
        )
    elif average < 10:
        explanation_parts.append(
            "🔴 <strong>Moyenne faible</strong>: "
            "Cela peut indiquer des difficultés d'apprentissage, de concentration ou des contraintes externes."
        )
    
    if int(projects) >= 3:
        explanation_parts.append(
            "⭐ <strong>Engagement excellent</strong>: "
            f"{int(projects)} projets réalisés montrent une implication active dans les activités pratiques."
        )
    
    if distance == '<5km' and presence >= 85:
        explanation_parts.append(
            "📍 <strong>Conditions favorables</strong>: "
            "Proximité et assiduité créent un environnement propice aux apprentissages."
        )
    
    explanation_text = "<br/>".join(explanation_parts) if explanation_parts else (
        "La combinaison de ces facteurs explique l'assignation de cet étudiant à ce profil particulier."
    )
    
    analysis_cards.append({
        'type': 'text',
        'title': '📊 Analyse contextuelle',
        'content': explanation_text
    })
    
    # Card 4: Cluster Comparison
    if cluster_id != -1:
        cluster_sizes = cluster_result.get('cluster_sizes', {})
        total_students = sum(cluster_sizes.values())
        cluster_pct = (cluster_sizes.get(cluster_id, 0) / total_students * 100) if total_students > 0 else 0
        
        comparison_text = f"""
        <strong>Comparaison avec les clusters</strong><br/>
        Nombre total de clusters: <strong>{cluster_result.get('n_clusters', 0)}</strong><br/>
        Taille du cluster de l'étudiant: <strong>{cluster_sizes.get(cluster_id, 0)} étudiants</strong><br/>
        Pourcentage de la population: <strong>{cluster_pct:.1f}%</strong><br/><br/>
        <em>Ce cluster représente</em>:
        """
        
        analysis_cards.append({
            'type': 'text',
            'title': '📈 Position dans l\'ensemble',
            'content': comparison_text
        })
    
    # Card 5: Recommendations
    recommendations = []
    
    if works:
        recommendations.append("✅ Envisager un ajustement du planning pour mieux équilibrer travail et études")
    
    if presence < 80:
        recommendations.append("✅ Améliorer l'assiduité aux cours (sessions de rattrapage recommandées)")
    
    if average < 12:
        recommendations.append("✅ Mettre en place un suivi pédagogique individualisé")
    
    if int(projects) < 2:
        recommendations.append("✅ Encourager la participation à plus de projets pratiques")
    
    if distance == '>15km':
        recommendations.append("✅ Proposer des ressources en ligne ou des réductions de trajets si possible")
    
    if not recommendations:
        recommendations.append("✅ Maintenir le rythme actuel - bonnes performances observées")
    
    rec_text = "<br/>".join(recommendations)
    
    analysis_cards.append({
        'type': 'text',
        'title': '💡 Recommandations',
        'content': rec_text
    })
    
    return analysis_cards
