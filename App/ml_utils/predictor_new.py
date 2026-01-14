"""ML Prediction module - loads trained models and generates recommendations."""

from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd

from .data_prep import load_datasets, prepare_resources, prepare_teachers


def _project_root():
    return Path(__file__).resolve().parents[2]


def _ensure_models_on_path():
    """Add Models subfolders to sys.path for custom classes."""
    root = _project_root()
    models_paths = [
        root / "Models",
        root / "Models" / "optimisation des ressources",
        root / "Models" / "prediction performance",
    ]
    for p in models_paths:
        pstr = str(p)
        if p.exists() and pstr not in sys.path:
            sys.path.insert(0, pstr)


def load_models(decision_tree_path=None, gradient_boosting_path=None):
    """Load ML models from trained artifacts.
    
    Returns: (dt_model for rooms, gb_model for teachers)
    Falls back to None if models don't exist.
    """
    _ensure_models_on_path()
    
    NotebookRegTree = None
    NotebookGB = None
    
    try:
        from DecisionTreeRegressor import decisionTreeRegressor as NotebookRegTree_class
        NotebookRegTree = NotebookRegTree_class
    except Exception:
        pass
    
    try:
        from GradientBoostingRegressor import GradientBoostingRegressor as NotebookGB_class
        NotebookGB = NotebookGB_class
    except Exception:
        pass
    
    dt_model = None
    gb_model = None
    
    root = _project_root()
    
    if decision_tree_path is None:
        decision_tree_path = root / "Artifacts" / "model_decision_tree_classification.json"
    if gradient_boosting_path is None:
        gradient_boosting_path = root / "Artifacts" / "modele_ia.json"
    
    # Load decision tree (for rooms)
    if NotebookRegTree is not None:
        try:
            dt_model = NotebookRegTree()
            if hasattr(dt_model, "load"):
                dt_model.load(str(decision_tree_path))
        except Exception:
            pass
    
    # Load gradient boosting (for teachers)
    if NotebookGB is not None:
        try:
            gb_model = NotebookGB()
            if hasattr(gb_model, "load"):
                gb_model.load(str(gradient_boosting_path))
        except Exception:
            pass
    
    return dt_model, gb_model


def predict_top_rooms_and_teachers(form_data: dict, dt_model, gb_model, top_n=3):
    """Predict top N rooms and teachers using ML models with correct feature engineering.
    
    Form data expected:
    - Nb_personnes: class size
    - Type_cours: CM/TD/TP
    - filiere: student track
    - niveau: academic level
    - nom_matiere: subject name
    
    Returns dict with 'rooms' and 'teachers' lists, each item normalized with expected keys.
    """
    resources, teachers, courses = load_datasets()
    res_prepared = prepare_resources(resources)
    teachers_prepared = prepare_teachers(teachers, resources, courses)
    
    # ========== PREDICT ROOMS ==========
    # Features: [Nb_personnes, Capacite, End_Type_ressource, End_Type_cours, End_Videoprojecteur, End_besoin_projecteur]
    
    form_type_cours = form_data.get("Type_cours", "CM")
    form_filiere = form_data.get("filiere", "GIT")
    
    def compute_besoin_projecteur(type_cours, filiere):
        if type_cours == "CM":
            return "OUI"
        elif type_cours == "TD":
            return "OUI" if filiere in ["GIT", "SDIA", "GESI", "EEAT", "Météorologie"] else "NON"
        elif type_cours == "TP":
            return "OUI" if filiere in ["GIT", "SDIA", "GESI"] else "NON"
        return "NON"
    
    form_besoin_projecteur = compute_besoin_projecteur(form_type_cours, form_filiere)
    
    room_features = []
    room_rows = []
    
    for _, row in res_prepared.iterrows():
        try:
            nb_personnes = float(form_data.get("Nb_personnes", 30))
            capacite = float(row.get("Capacite", 60))
            end_type_ressource = float(row.get("End_Type_ressource", 1))
            
            # Map Type_cours to numeric
            type_cours_map = {"CM": 2, "TD": 1, "TP": 0}
            end_type_cours = float(type_cours_map.get(form_type_cours, 0))
            
            end_videoprojecteur = float(1 if row.get("Videoprojecteur") == "OUI" else 0)
            end_besoin_projecteur = float(1 if form_besoin_projecteur == "OUI" else 0)
            
            x = [nb_personnes, capacite, end_type_ressource, end_type_cours, 
                 end_videoprojecteur, end_besoin_projecteur]
            room_features.append(x)
            room_rows.append(row)
        except Exception:
            continue
    
    room_X = np.array(room_features)
    
    # Get scores from model or fallback
    room_scores = None
    if dt_model is not None and hasattr(dt_model, "predict"):
        try:
            room_scores = dt_model.predict(room_X)
        except Exception:
            try:
                room_scores = [float(dt_model.predict([xi])[0]) for xi in room_X]
                room_scores = np.array(room_scores)
            except Exception:
                pass
    
    if room_scores is None:
        room_scores = np.array([float(r.get("Score", 0)) for r in room_rows])
    
    # Build rooms list
    rooms_list = []
    for rrow, score in zip(room_rows, room_scores):
        room_id = rrow.get("Identifiant_ressource") or rrow.get("Id") or rrow.get("Nom_ressource", "room")
        rooms_list.append((room_id, float(score), rrow.to_dict()))
    
    # Sort and deduplicate
    rooms_sorted_raw = sorted(rooms_list, key=lambda t: t[1], reverse=True)
    rooms_seen = set()
    rooms_sorted = []
    for rid, sc, rrow in rooms_sorted_raw:
        if rid in rooms_seen:
            continue
        rooms_seen.add(rid)
        rooms_sorted.append((rid, sc, rrow))
    rooms_sorted = rooms_sorted[:top_n]
    
    # ========== PREDICT TEACHERS ==========
    # Features: [Anciennete, Score_appreciation, score_niveau, score_heure, score_pse]
    
    teacher_features = []
    teacher_rows = []
    
    for _, trow in teachers_prepared.iterrows():
        try:
            anciennete = float(trow.get("Anciennete", 0))
            score_appreciation = float(trow.get("Score_appreciation", 0))
            score_niveau = float(trow.get("score_niveau", 0))
            score_heure = float(trow.get("score_heure", 0))
            score_pse = float(trow.get("score_pse", 0))
            
            x = [anciennete, score_appreciation, score_niveau, score_heure, score_pse]
            teacher_features.append(x)
            teacher_rows.append(trow)
        except Exception:
            continue
    
    teacher_X = np.array(teacher_features) if teacher_features else np.array([])
    
    # Get teacher scores from model or fallback
    teacher_scores = None
    if gb_model is not None and hasattr(gb_model, "predict") and len(teacher_X) > 0:
        try:
            teacher_scores = gb_model.predict(teacher_X)
        except Exception:
            try:
                teacher_scores = [float(gb_model.predict([xi])[0]) for xi in teacher_X]
                teacher_scores = np.array(teacher_scores)
            except Exception:
                pass
    
    if teacher_scores is None and len(teacher_X) > 0:
        # Fallback: simple heuristic based on availability
        teacher_scores = np.array([
            float(t.get("Heures_restantes", 0)) / max(1, float(t.get("Heures_totales_assignees", 1)))
            for t in teacher_rows
        ])
    
    # Build teachers list
    teachers_list = []
    for trow, score in zip(teacher_rows, teacher_scores if teacher_scores is not None else [0]*len(teacher_rows)):
        teacher_id = trow.get("Matricule_enseignant") or trow.get("id", "teacher")
        teachers_list.append((teacher_id, float(score), trow.to_dict()))
    
    # Sort and deduplicate
    teachers_sorted_raw = sorted(teachers_list, key=lambda t: t[1], reverse=True)
    teachers_seen = set()
    teachers_sorted = []
    for tid, sc, trow in teachers_sorted_raw:
        if tid in teachers_seen:
            continue
        teachers_seen.add(tid)
        teachers_sorted.append((tid, sc, trow))
    teachers_sorted = teachers_sorted[:top_n]
    
    return {
        "rooms": [{"id": rid, "score": sc, "data": rrow} for rid, sc, rrow in rooms_sorted],
        "teachers": [{"id": tid, "score": sc, "data": trow} for tid, sc, trow in teachers_sorted],
    }
