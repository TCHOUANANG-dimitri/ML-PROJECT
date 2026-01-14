from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from ml_utils.predictor import load_models, predict_top_rooms_and_teachers
from ml_utils.data_prep import load_datasets, parse_planning_file
import pandas as pd
import json
from pathlib import Path

# Paths to trained models (adjust if your files are elsewhere)
ROOT = Path(__file__).resolve().parents[1]
DT_MODEL_PATH = ROOT / ".." / "Training&Saving" / "decision_tree_class_model.json"
GB_MODEL_PATH = ROOT / ".." / "Training&Saving" / "gradient_boosting_regressor_model_teachers.json"


# load models once at import (or lazy-load inside the view)
dt_model, gb_model = load_models(str(DT_MODEL_PATH), str(GB_MODEL_PATH))


@require_http_methods(["GET", "POST"])
def recommendation_view(request):
    """Handle form submit, call predictor and render top 3 rooms and teachers.

    Expects form fields (POST):
    - Nb_personnes, Type_cours, besoin_projecteur
    - niveau, filiere, nom_matiere
    - jour, heure (used client-side or for calendar checks)
    """
    # Parse planning.txt to get filieres and matieres by niveau
    matieres_by_filiere_level, matieres_map = parse_planning_file()
    filieres = sorted(matieres_map.keys())
    # prepare JSON for client-side: matieres_by_filiere_level -> {filiere: {level: [matieres]}}
    matieres_by_level_json = json.dumps(matieres_by_filiere_level, ensure_ascii=False)
    context = {"rooms": [], "teachers": [], "errors": [], "filieres": filieres, "matieres_map": matieres_map, "matieres_json": json.dumps(matieres_map, ensure_ascii=False), "matieres_by_level_json": matieres_by_level_json}

    if request.method == "POST":
        form = request.POST
        form_data = {
            "Nb_personnes": form.get("Nb_personnes"),
            "Type_cours": form.get("Type_cours"),
            "besoin_projecteur": form.get("besoin_projecteur"),
            "niveau": form.get("niveau"),
            "filiere": form.get("filiere"),
            "nom_matiere": form.get("nom_matiere"),
            "jour": form.get("jour"),
            "heure": form.get("heure"),
        }

        try:
            result = predict_top_rooms_and_teachers(form_data, dt_model, gb_model, top_n=3)

            # annotate results with stars and ensure dict-like access in template
            def annotate(items):
                if not items:
                    return []
                scores = [it[1] for it in items]
                max_score = max(scores) if any(scores) else 1.0
                annotated = []
                for ident, score, row in items:
                    # compute 0-5 stars relative to max_score
                    try:
                        stars = int(round((float(score) / float(max_score)) * 5)) if max_score else 0
                    except Exception:
                        stars = 0
                    if stars < 0:
                        stars = 0
                    stars_str = "".join(["★" for _ in range(stars)]) + "".join(["☆" for _ in range(5 - stars)])
                    annotated.append({"id": ident, "score": float(score), "row": row.to_dict() if hasattr(row, 'to_dict') else row, "stars": stars, "stars_str": stars_str})
                return annotated

            context["rooms"] = annotate(result.get("rooms", []))
            context["teachers"] = annotate(result.get("teachers", []))
        except Exception as e:
            context["errors"].append(str(e))

        # Si c'est un fetch (AJAX), retourner JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({
                "rooms": context["rooms"],
                "teachers": context["teachers"],
                "errors": context["errors"]
            })

    return render(request, "index.html", context)
