import numpy as np
import pandas as pd

# =================================================================
# SECTION 1 : LE MODÈLE 
# =================================================================
class ENSPD_GradientBoosting_Pure:
    def __init__(self, n_arbres=20, lr=0.1, max_depth=3):
        self.n_arbres = n_arbres
        self.lr = lr
        self.max_depth = max_depth
        self.arbres = []
        self.moyenne_initiale = None

    def _calculer_variance_reduction(self, y, y_gauche, y_droite):
        if len(y_gauche) == 0 or len(y_droite) == 0: return 0
        var_parent = np.var(y) * len(y)
        var_enfants = (np.var(y_gauche) * len(y_gauche)) + (np.var(y_droite) * len(y_droite))
        return var_parent - var_enfants

    def _construire_arbre(self, X, y, depth):
        if depth >= self.max_depth or len(y) <= 2:
            return {'feuille': True, 'valeur': np.mean(y)}

        m_feat, m_seuil, m_gain = None, None, -1
        for f in range(X.shape[1]):
            seuils = np.unique(X[:, f])
            for s in seuils:
                g = X[:, f] <= s
                gain = self._calculer_variance_reduction(y, y[g], y[~g])
                if gain > m_gain:
                    m_gain, m_feat, m_seuil = gain, f, s
        
        if m_gain <= 0: return {'feuille': True, 'valeur': np.mean(y)}

        indices_g = X[:, m_feat] <= m_seuil
        return {
            'feuille': False, 'feature': int(m_feat), 'seuil': float(m_seuil),
            'gauche': self._construire_arbre(X[indices_g], y[indices_g], depth + 1),
            'droite': self._construire_arbre(X[~indices_g], y[~indices_g], depth + 1)
        }

    def _predire_un(self, x, noeud):
        if noeud['feuille']: return noeud['valeur']
        if x[noeud['feature']] <= noeud['seuil']:
            return self._predire_un(x, noeud['gauche'])
        return self._predire_un(x, noeud['droite'])

    def fit(self, X, y):
        X, y = np.array(X), np.array(y)
        self.moyenne_initiale = float(np.mean(y))
        y_pred = np.full(len(y), self.moyenne_initiale)
        
        self.historique_erreur = [] 
        

        for i in range(self.n_arbres):
            residus = y - y_pred
            arbre = self._construire_arbre(X, residus, 0)
            corrections = np.array([self._predire_un(x, arbre) for x in X])
            y_pred += self.lr * corrections
            self.arbres.append(arbre)

            mse = np.mean((y - y_pred)**2)
            self.historique_erreur.append(mse)
            

    def predict(self, X):
        X = np.array(X)
        y_final = np.full(X.shape[0], self.moyenne_initiale)
        for arbre in self.arbres:
            y_final += self.lr * np.array([self._predire_un(x, arbre) for x in X])
        return y_final

    def score(self, X, y):
        """Calcule le coefficient de détermination R²"""
        y = np.array(y)
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        return 1 - (ss_res / ss_tot)

# =================================================================
# SECTION 2 : PRÉPARATION ET ÉVALUATION 
# =================================================================

# 1. Sélection des colonnes

df = pd.read_excel('jeu_données_étudiants.xlsx') 

features_list = ['encodage_dist_dom', 'Nb_projets', 'ratio_heure']
X = df[features_list].values
y = df['Moyenne_annuelle'].values
features_list = ['encodage_dist_dom', 'Nb_projets', 'ratio_heure']
X = df[features_list].values
y = df['Moyenne_annuelle'].values

# 2. Division Train/Test (80% pour apprendre, 20% pour tester)
indices = np.arange(len(X))
np.random.shuffle(indices) # Mélange pour éviter les biais
split = int(0.8 * len(X))

X_train, X_test = X[indices[:split]], X[indices[split:]]
y_train, y_test = y[indices[:split]], y[indices[split:]]

# 3. Entraînement
gb_model = ENSPD_GradientBoosting_Pure(n_arbres=20, lr=0.1, max_depth=3)
gb_model.fit(X_train, y_train)

# 4. Calcul des scores
gb_score_train = gb_model.score(X_train, y_train)
gb_score_test = gb_model.score(X_test, y_test)

# 5. AFFICHAGE FINAL
print("="*60)
print("TEST GRADIENT BOOST REGRESSOR")
print("="*60)
print(f"Gradient boost - Score TRAIN: {gb_score_train:.4f}")
print(f"Gradient boost - Score TEST:  {gb_score_test:.4f}")
print()
print("="*60)
print(f"Gradient boost     - Généralisation: {gb_score_test:.4f}")
print("="*60)
import matplotlib.pyplot as plt

# =================================================================
# SECTION 3 : VISUALISATION
# =================================================================

plt.figure(figsize=(15, 6))

# --- GRAPHIQUE 1 : LA FONCTION DE COÛT (Apprentissage) ---
plt.subplot(1, 2, 1)
plt.plot(range(1, len(gb_model.historique_erreur) + 1), gb_model.historique_erreur, 
         color='#2c3e50', linewidth=2, marker='o', markersize=4)
plt.title("Réduction de l'Erreur (Fonction de Coût)", fontsize=12)
plt.xlabel("Nombre d'Arbres")
plt.ylabel("Erreur Quadratique Moyenne (MSE)")
plt.grid(True, linestyle='--', alpha=0.7)

# --- GRAPHIQUE 2 : RÉEL VS PRÉDICTION (Validation) ---
y_pred_test = gb_model.predict(X_test)
plt.subplot(1, 2, 2)
plt.scatter(y_test, y_pred_test, color='#e67e22', alpha=0.6, label='Données de test')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'k--', lw=2, label='Prédiction Parfaite')
plt.title("Notes Réelles vs Prédictions de l'IA", fontsize=12)
plt.xlabel("Notes Réelles (/20)")
plt.ylabel("Notes Prédites (/20)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
# 4. Sauvegarde JSON

import os
# Définir le chemin
chemin_final = os.path.join(os.path.dirname(__file__), '..', 'Artifacts', 'modele_ia.json')

# Utiliser la nouvelle fonction de la classe
gb_model.save(chemin_final)