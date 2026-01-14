#!/usr/bin/env python3
"""
Fix recommendation page HTML structure
"""
import re
from pathlib import Path

html_path = Path('App/index.html')
content = html_path.read_text(encoding='utf-8')

# Trouver la section recommendation
pattern = r'(<section class="page" id="page-recommendation".*?<!-- EMPLOI DU TEMPS -->)'
match = re.search(pattern, content, re.DOTALL)

if match:
    old_section = match.group(0)
    print(f"✓ Section trouvée - {len(old_section)} caractères")
    
    new_section = '''<section class="page" id="page-recommendation" aria-label="Recommandation &amp; Planification intelligente">
          <h1 class="page-title">Recommandation &amp; Planification intelligente</h1>

          <!-- FORMULAIRE EN HAUT - PLEINE LARGEUR -->
          <div class="card form" style="margin-bottom:20px;">
            <form id="recommendationForm" method="post" action="/recommendation/">
              <div class="card-header">
                <h2>Paramètres de la séance</h2>
              </div>
              <div class="form-grid">
                <div class="form-group">
                  <label for="rec-Nb_personnes">Effectif estimé *</label>
                  <input name="Nb_personnes" id="rec-Nb_personnes" type="number" min="1" required />
                </div>
                <div class="form-group">
                  <label for="rec-Type_cours">Type de séance *</label>
                  <select name="Type_cours" id="rec-Type_cours" required>
                    <option value="CM">CM</option>
                    <option value="TD">TD</option>
                    <option value="TP">TP</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="rec-besoin_projecteur">Besoin vidéoprojecteur</label>
                  <select name="besoin_projecteur" id="rec-besoin_projecteur">
                    <option value="OUI">OUI</option>
                    <option value="NON">NON</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="rec-niveau">Niveau *</label>
                  <select name="niveau" id="rec-niveau" required>
                    <option value="">Sélectionner</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="rec-filiere">Filière *</label>
                  <select name="filiere" id="rec-filiere" required>
                    <option value="">Sélectionner</option>
                  </select>
                </div>
                <div class="form-group">
                  <label for="rec-nom_matiere">Nom de la matière *</label>
                  <select name="nom_matiere" id="rec-nom_matiere" required>
                    <option value="">Choisir une matière</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="rec-jour">Date / jour</label>
                  <input name="jour" id="rec-jour" type="date" />
                </div>
                <div class="form-group">
                  <label for="rec-heure">Tranche horaire</label>
                  <select name="heure" id="rec-heure">
                    <option value="morning">7:30 - 11:30</option>
                    <option value="afternoon">12:30 - 16:30</option>
                  </select>
                </div>
              </div>

              <div class="form-footer">
                {% csrf_token %}
                <button type="submit" class="btn primary">Prédire</button>
                <div class="form-help">
                  L'IA utilise la disponibilité, la spécialité, les heures restantes et l'historique des enseignants.
                </div>
              </div>
            </form>
          </div>

          <!-- RÉSULTATS EN BAS - 2 COLONNES (SALLES À GAUCHE, ENSEIGNANTS À DROITE) -->
          <div class="card" id="recommendationResults">
            <div class="card-header space-between">
              <h2>Résultats de la recommandation IA</h2>
              <span class="chip chip-ai">IA</span>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:16px;">
              <!-- COLONNE GAUCHE: SALLES -->
              <div class="recommendation-block">
                <h3>🏫 Top 3 salles recommandées</h3>
                <div class="recommendation-list" id="roomRecommendations">
                  {% for item in rooms %}
                    <div class="recommendation-item">
                      <div style="display:flex;justify-content:space-between;align-items:start;">
                        <div>
                          <strong>{{ item.id }}</strong>
                          <div class="small">{{ item.row.Nom_ressource }}</div>
                        </div>
                        <div style="text-align:right;">
                          <div>{{ item.stars_str }}</div>
                          <div class="small" style="color:#666;">Score: {{ item.score|floatformat:3 }}</div>
                        </div>
                      </div>
                      <div style="margin-top:6px;font-size:12px;color:#666;">
                        Capacité: {{ item.row.Capacite }} • Projecteur: {{ item.row.Videoprojecteur }}
                      </div>
                      <div style="margin-top:8px;">
                        <button type="button" class="btn program-btn" data-room="{{ item.id }}" data-room-name="{{ item.row.Nom_ressource }}">Programmer</button>
                      </div>
                    </div>
                  {% empty %}
                    <p style="color:#999;">Effectuez une prédiction pour voir les recommandations</p>
                  {% endfor %}
                </div>
              </div>

              <!-- COLONNE DROITE: ENSEIGNANTS -->
              <div class="recommendation-block">
                <h3>👨‍🏫 Top 3 enseignants recommandés</h3>
                <div class="recommendation-list" id="teacherRecommendations">
                  {% for item in teachers %}
                    <div class="recommendation-item">
                      <div style="display:flex;justify-content:space-between;align-items:start;">
                        <div>
                          <strong>{% if item.row.Nom %}{{ item.row.Nom }}{% else %}{{ item.id }}{% endif %}</strong>
                          <div class="small">{{ item.row.Enseignant_id }}</div>
                        </div>
                        <div style="text-align:right;">
                          <div>{{ item.stars_str }}</div>
                          <div class="small" style="color:#666;">Score: {{ item.score|floatformat:3 }}</div>
                        </div>
                      </div>
                      <div style="margin-top:6px;font-size:12px;color:#666;">
                        Spécialité: {{ item.row.Specialite }} • Ancienneté: {{ item.row.Anciennete }}
                      </div>
                      <div style="margin-top:8px;">
                        <button type="button" class="btn program-btn" data-teacher="{{ item.row.Enseignant_id|default:item.id }}" data-teacher-name="{% if item.row.Nom %}{{ item.row.Nom }}{% else %}{{ item.id }}{% endif %}">Programmer</button>
                      </div>
                    </div>
                  {% empty %}
                    <p style="color:#999;">Effectuez une prédiction pour voir les recommandations</p>
                  {% endfor %}
                </div>
              </div>
            </div>

            {% if errors %}
              <div style="background:#fee;margin-top:12px;padding:8px;border-left:4px solid #e74c3c;border-radius:2px;">
                <strong>Erreurs</strong>
                <ul style="margin:4px 0 0 20px;font-size:12px;">
                  {% for e in errors %}<li>{{ e }}</li>{% endfor %}
                </ul>
              </div>
            {% endif %}
          </div>
        </section>

        <!-- EMPLOI DU TEMPS -->'''
    
    content = content.replace(old_section, new_section)
    html_path.write_text(content, encoding='utf-8')
    print("✓ HTML mise à jour avec succès!")
    print("✓ Formulaire repositionné en haut")
    print("✓ Résultats en bas avec 2 colonnes")
else:
    print("✗ Section NOT found")
