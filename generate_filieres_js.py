#!/usr/bin/env python3
"""Generate JavaScript-ready JSON for filieres and matieres."""

import sys
sys.path.insert(0, 'd:/ML-PROJECT/App')

from ml_utils.data_prep import parse_planning_file
import json

matieres_by_filiere_level, matieres_map = parse_planning_file()

# Créer une version JavaScript
js_code = f"""// Données extraites du planning.txt
const filieresMatieres = {json.dumps(matieres_by_filiere_level, ensure_ascii=False, indent=2)};
"""

print(js_code)
