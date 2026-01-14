from pathlib import Path
import sys
import json
import numpy as np

from .data_prep import load_datasets, prepare_resources, prepare_teachers


def _project_root():
    return Path(__file__).resolve().parents[2]


def _ensure_models_on_path():
    # Add Models subfolders used in notebooks to sys.path to reuse custom classes
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
    _ensure_models_on_path()
    # Try to import local model classes (as used in your notebooks)
    DT = None
    GB = None
    try:
        from Decision_Tree_Classification import DecisionTreeClassifier as NotebookDT
    except Exception:
        NotebookDT = None

    try:
        # fallback name from training notebooks
        from DecisionTreeRegressor import decisionTreeRegressor as NotebookRegTree
    except Exception:
        NotebookRegTree = None

    try:
        from gradientBoosting_model import GradientBoostingRegressor as NotebookGB
    except Exception:
        NotebookGB = None

    # instantiate or load from json if possible
    dt_model = None
    gb_model = None
    if decision_tree_path and NotebookRegTree is not None:
        try:
            dt_model = NotebookRegTree()
            if hasattr(dt_model, "load"):
                dt_model.load(decision_tree_path)
            else:
                # try reading json and set attributes if available
                with open(decision_tree_path, "r", encoding="utf-8") as f:
                    _ = json.load(f)
        except Exception:
            dt_model = None

    if gradient_boosting_path and NotebookGB is not None:
        try:
            gb_model = NotebookGB()
            if hasattr(gb_model, "load"):
                gb_model.load(gradient_boosting_path)
            else:
                with open(gradient_boosting_path, "r", encoding="utf-8") as f:
                    _ = json.load(f)
        except Exception:
            gb_model = None

    return dt_model, gb_model


def predict_top_rooms_and_teachers(form_data: dict, dt_model, gb_model, top_n=3):
    """Given form input, predict scores for all rooms and teachers and return top N of each.

    - form_data for rooms: expects 'Nb_personnes', 'Type_cours', 'besoin_projecteur'
    - form_data for teachers: expects 'niveau','filiere','nom_matiere'

    Returns dict: {'rooms': [(room_id, score, row_dict)...], 'teachers': [(teacher_id, score, row_dict)...]}
    """
    resources, teachers, courses = load_datasets()
    res_prepared = prepare_resources(resources)
    teachers_prepared = prepare_teachers(teachers, resources, courses)

    # Prepare room feature matrix according to required order
    room_features = []
    room_rows = []
    for _, row in res_prepared.iterrows():
        Nb_personnes = float(form_data.get("Nb_personnes", row.get("Nb_personnes", 0)))
        Capacité = row.get("Capacite", 1)
        End_Type_ressource = row.get("End_Type_ressource", 0)
        End_Type_cours = 2 if form_data.get("Type_cours") == "CM" else (1 if form_data.get("Type_cours") == "TD" else 0)
        End_Videoprojecteur = 1 if row.get("Videoprojecteur") == "OUI" else 0
        End_besoin_projecteur = 1 if form_data.get("besoin_projecteur", row.get("besoin_projecteur", "NON")) == "OUI" else 0

        x = [Nb_personnes, Capacité, End_Type_ressource, End_Type_cours, End_Videoprojecteur, End_besoin_projecteur]
        room_features.append(x)
        room_rows.append(row)

    room_X = np.array(room_features)

    room_scores = None
    if dt_model is not None and hasattr(dt_model, "predict"):
        try:
            room_scores = dt_model.predict(room_X)
        except Exception:
            # try row-wise predict
            room_scores = []
            for xi in room_X:
                try:
                    room_scores.append(float(dt_model.predict([xi])[0]))
                except Exception:
                    room_scores.append(0.0)
            room_scores = np.array(room_scores)
    else:
        # fallback: use prepared Score column
        room_scores = np.array([r.get("Score", 0) for r in room_rows])

    rooms_list = []
    for rrow, score in zip(room_rows, room_scores):
        rooms_list.append((rrow.get("Id") if "Id" in rrow else rrow.get("Nom_ressource", "room"), float(score), rrow.to_dict()))

    rooms_sorted = sorted(rooms_list, key=lambda t: t[1], reverse=True)[:top_n]

    # Teachers: prepare features per teacher
    teacher_features = []
    teacher_rows = []
    # For teacher feature inputs we rely on prepare_teachers mapping
    # We'll generate each teacher's input vector from available columns
    for _, trow in teachers_prepared.iterrows():
        try:
            Anciennete = float(trow.get("Anciennete", 0))
        except Exception:
            Anciennete = 0.0
        try:
            Score_appreciation = float(trow.get("Score_appreciation", 0))
        except Exception:
            Score_appreciation = 0.0
        score_niveau = float(trow.get("score_niveau", 0))
        score_heure = float(trow.get("score_heure", 0))
        score_pse = float(trow.get("score_pse", 0))

        x = [Anciennete, Score_appreciation, score_niveau, score_heure, score_pse]
        teacher_features.append(x)
        teacher_rows.append(trow)

    teach_X = np.array(teacher_features)

    teacher_scores = None
    if gb_model is not None and hasattr(gb_model, "predict"):
        try:
            teacher_scores = gb_model.predict(teach_X)
        except Exception:
            teacher_scores = []
            for xi in teach_X:
                try:
                    teacher_scores.append(float(gb_model.predict([xi])[0]))
                except Exception:
                    teacher_scores.append(0.0)
            teacher_scores = np.array(teacher_scores)
    else:
        teacher_scores = np.array([t.get("Score", 0) for t in teacher_rows])

    teachers_list = []
    for trow, score in zip(teacher_rows, teacher_scores):
        teachers_list.append((trow.get("Enseignant_id", trow.get("Nom", "teacher")), float(score), trow.to_dict()))

    teachers_sorted = sorted(teachers_list, key=lambda t: t[1], reverse=True)[:top_n]

    return {"rooms": rooms_sorted, "teachers": teachers_sorted}
