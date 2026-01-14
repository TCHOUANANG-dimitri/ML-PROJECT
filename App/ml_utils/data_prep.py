from pathlib import Path
import pandas as pd


def _project_root():
    # return repository root (assumes this file is in App/ml_utils)
    return Path(__file__).resolve().parents[2]


def load_datasets():
    root = _project_root()
    data_dir = root / "Datasets"
    resources_raw = pd.read_csv(data_dir / "Resources.csv")
    # The raw file contains one row per scheduled use of a resource; normalize
    # to one row per physical resource (Identifiant_ressource) to avoid
    # duplicate recommendations of the same room multiple times.
    if "Identifiant_ressource" in resources_raw.columns:
        # aggregate sensible defaults: max capacity, any projecteur -> OUI,
        # most frequent Type_cours and Filiere
        def most_common(s):
            try:
                return s.mode().iloc[0]
            except Exception:
                return s.iloc[0] if len(s) else None

        agg = {
            "Type_ressource": "first",
            "Capacite": "max",
            "Videoprojecteur": lambda x: "OUI" if (x == "OUI").any() else "NON",
            "Type_cours": most_common,
            "Filiere": most_common,
            "Nb_personnes": "max",
        }

        grouped = (
            resources_raw.groupby("Identifiant_ressource", dropna=False)
            .agg(agg)
            .reset_index()
            .rename(columns={"Identifiant_ressource": "Identifiant_ressource"})
        )

        # Create stable identifier/name fields expected by downstream code
        grouped["Nom_ressource"] = grouped["Identifiant_ressource"]
        grouped["Id"] = grouped["Identifiant_ressource"]
        resources = grouped
    else:
        resources = pd.read_csv(data_dir / "Resources.csv")
    teachers = pd.read_csv(data_dir / "teachers.csv")
    courses = pd.read_csv(data_dir / "courses.csv")
    return resources, teachers, courses


def prepare_resources(resources: pd.DataFrame) -> pd.DataFrame:
    """Apply same feature engineering as in the notebook 'optimisation & recommandation'.

    Produces columns required by the room model:
    ["Nb_personnes","Capacite","End_Type_ressource","End_Type_cours",
     "End_Videoprojecteur","End_besoin_projecteur"] and a Score column.
    """
    df = resources.copy()

    # besoin_projecteur
    besoin_projecteur = []
    for i in range(df.shape[0]):
        if df.loc[i, "Type_cours"] == "CM":
            besoin_projecteur.append("OUI")
        elif df.loc[i, "Type_cours"] == "TD":
            if df.loc[i, "Filiere"] in ["GIT", "SDIA", "GESI", "EEAT", "Météorologie"]:
                besoin_projecteur.append("OUI")
            else:
                besoin_projecteur.append("NON")
        elif df.loc[i, "Type_cours"] == "TP":
            if df.loc[i, "Filiere"] in ["GIT", "SDIA", "GESI"]:
                besoin_projecteur.append("OUI")
            else:
                besoin_projecteur.append("NON")
        else:
            besoin_projecteur.append("NON")

    df["besoin_projecteur"] = besoin_projecteur

    # taux_occupation
    df["taux_occupation"] = df["Nb_personnes"] / df["Capacite"]

    # adequation_equipement
    adequation_equipement = []
    for i in range(df.shape[0]):
        if (df.loc[i, "Videoprojecteur"] == "OUI" and df.loc[i, "besoin_projecteur"] == "OUI") or (
            df.loc[i, "Videoprojecteur"] == "NON" and df.loc[i, "besoin_projecteur"] == "NON"
        ):
            adequation_equipement.append(1)
        elif df.loc[i, "Videoprojecteur"] == "OUI" and df.loc[i, "besoin_projecteur"] == "NON":
            adequation_equipement.append(0.5)
        elif df.loc[i, "Videoprojecteur"] == "NON" and df.loc[i, "besoin_projecteur"] == "OUI":
            adequation_equipement.append(0)
        else:
            adequation_equipement.append(0)

    df["adequation_equipement"] = adequation_equipement

    # adequation_salle
    adequation_salle = []
    for i in range(df.shape[0]):
        type_cours = df.loc[i, "Type_cours"]
        type_ressource = df.loc[i, "Type_ressource"]
        if (type_cours in ["CM", "TD"] and type_ressource == "Salle") or (
            type_cours == "TP" and type_ressource == "Labo"
        ):
            adequation_salle.append(1)
        else:
            adequation_salle.append(0)

    df["adequation_salle"] = adequation_salle

    # score
    df["Score"] = df["taux_occupation"] * 0.4 + df["adequation_equipement"] * 0.3 + df["adequation_salle"] * 0.3

    # maps
    def map_type_ressource(x):
        if x == "Labo":
            return 2
        if x == "Salle":
            return 1
        return 0

    def map_type_cours(x):
        if x == "CM":
            return 2
        if x == "TD":
            return 1
        return 0

    df["End_Type_ressource"] = df["Type_ressource"].apply(map_type_ressource)
    df["End_Type_cours"] = df["Type_cours"].apply(map_type_cours)
    df["End_Videoprojecteur"] = df["Videoprojecteur"].apply(lambda v: 1 if v == "OUI" else 0)
    df["End_besoin_projecteur"] = df["besoin_projecteur"].apply(lambda v: 1 if v == "OUI" else 0)

    return df


def prepare_teachers(teachers: pd.DataFrame, resources: pd.DataFrame, courses: pd.DataFrame) -> pd.DataFrame:
    """Merge teachers with resources and courses and compute the scores used by the teacher model.

    Produces columns required by the teacher model:
    ["Anciennete","Score_appreciation","score_niveau","score_heure","score_pse"]
    """
    # The notebook merges teachers with resources on Enseignant_id and then with courses on nom_cours
    df_t = teachers.copy()
    df_r = resources.copy()
    df_c = courses.copy()

    # try to align column names used in the notebook
    if "Matricule_enseignant" in df_t.columns:
        df_t = df_t.rename(columns={"Matricule_enseignant": "Enseignant_id"})

    # minimal merge: try to merge on Enseignant_id if present
    if "Enseignant_id" in df_t.columns and "Enseignant_id" in df_r.columns:
        tr = pd.merge(df_t, df_r, left_on="Enseignant_id", right_on="Enseignant_id", how="inner")
    else:
        # fallback: use teachers as-is
        tr = df_t.copy()

    # columns expected: Nom_matiere -> nom_cours
    if "Nom_matiere" in tr.columns:
        tr = tr.rename(columns={"Nom_matiere": "nom_cours"})

    if "nom_cours" in tr.columns and "nom_cours" in df_c.columns:
        trc = pd.merge(tr, df_c, left_on="nom_cours", right_on="nom_cours", how="inner")
    else:
        trc = tr.copy()

    # compute score components similar to the notebook
    def compute_scores(df):
        score_niveau = []
        score_heure = []
        score_pse = []
        niveau_score_vals = []
        for i in range(df.shape[0]):
            # PSE
            try:
                score_pse.append(1 if df.loc[i, "Specialite"] == df.loc[i, "specialite"] else 0)
            except Exception:
                score_pse.append(0)

            # Heures
            try:
                score_heure.append(1 if df.loc[i, "Heures_restantes"] >= df.loc[i, "total"] else 0)
            except Exception:
                score_heure.append(0)

            # Niveau
            niveau = df.loc[i, "Niveau_academique"] if "Niveau_academique" in df.columns else None
            niveau_score = 0
            if niveau == "INGENIEUR":
                niveau_score += 3
            elif niveau == "MASTER":
                niveau_score += 3
            elif niveau == "DOCTEUR":
                niveau_score += 4
            else:
                niveau_score += 5

            if "Type_enseignant" in df.columns and df.loc[i, "Type_enseignant"] == "PERMANENT":
                niveau_score += 1

            score_niveau.append(niveau_score)
            niveau_score_vals.append(niveau_score)

        return score_niveau, score_heure, score_pse, niveau_score_vals

    sc_niv, sc_heure, sc_pse, niv_vals = compute_scores(trc)
    trc["score_niveau"] = sc_niv
    trc["score_heure"] = sc_heure
    trc["score_pse"] = sc_pse
    trc["niveau_score"] = niv_vals

    # compute overall Score like in notebook
    try:
        trc["Score"] = (
            trc["score_niveau"] * 0.1
            + trc["score_heure"] * 0.4
            + trc["Anciennete"] * 0.2
            + trc["Score_appreciation"] * 0.1
            + trc["score_pse"] * 0.2
        )
    except Exception:
        # if some columns missing, skip Score
        pass

    return trc


def parse_planning_file() -> tuple:
    """Parse App/planning.txt and return two structures:
    - matieres_by_filiere_level: {filiere: {level: [matiere, ...]}}
    - matieres_map: {filiere: [unique matieres across levels]}

    The parser is tolerant to the text format in `App/planning.txt` used in this repo.
    """
    root = _project_root()
    planning_path = root / "App" / "planning.txt"
    matieres_by_filiere_level = {}
    current_filiere = None
    current_level = None

    if not planning_path.exists():
        return matieres_by_filiere_level, {}

    with open(planning_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            up = line.upper()
            
            # Detect 'TRONC' (common trunk) FIRST before filiere check
            if "TRONC" in up:
                current_filiere = "TRONC_COMMUN"
                matieres_by_filiere_level.setdefault(current_filiere, {})
                current_level = None
                continue
            
            # Detect filiere headings (lines containing FILIERE or FILI)
            if ("FILI" in up and up.find("FILI") < 20) or up.startswith("FIL") or ("FILIERE" in up) or ("FILIÈRE" in up):
                # normalize: remove the keyword and emojis
                cleaned = line
                for token in ["FILIERE", "FILIÈRE", "FILIÈRE"]:
                    cleaned = cleaned.replace(token, "")
                # remove emoji prefixes
                cleaned = cleaned.replace("(", "").split("-")[0].strip()
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
                if lvl is None:
                    try:
                        lvl = int(parts[-1])
                    except Exception:
                        lvl = None
                if lvl is not None:
                    current_level = int(lvl)
                    if current_filiere is None:
                        current_filiere = "TRONC_COMMUN"
                        matieres_by_filiere_level.setdefault(current_filiere, {})
                    matieres_by_filiere_level[current_filiere].setdefault(current_level, [])
                continue

            # parse potential subject lines: tab-separated or with multiple spaces or using pipe
            parts = [p.strip() for p in line.split("\t") if p.strip()]
            if len(parts) >= 2:
                matiere = parts[0]
            else:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 2:
                    matiere = parts[0]
                else:
                    import re
                    parts = [p for p in re.split(r"\s{2,}", line) if p.strip()]
                    if parts:
                        matiere = parts[0]
                    else:
                        continue

            if not matiere:
                continue

            lvl = current_level or 0
            fil = current_filiere or "TRONC_COMMUN"
            matieres_by_filiere_level.setdefault(fil, {})
            matieres_by_filiere_level[fil].setdefault(lvl, []).append(matiere)

    # Build matieres_map (filiere -> unique list)
    matieres_map = {}
    for f, levels in matieres_by_filiere_level.items():
        seen = []
        for lvl in sorted(levels.keys()):
            for m in levels[lvl]:
                if m and m not in seen:
                    seen.append(m)
        matieres_map[f] = seen

    return matieres_by_filiere_level, matieres_map
