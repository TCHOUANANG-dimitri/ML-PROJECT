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
        
import json
import os

def save(self, filepath):
        """Sauvegarde les paramètres du modèle dans un fichier JSON"""
        export_data = {
            "moyenne_initiale": float(self.moyenne_initiale),
            "lr": float(self.lr),
            "arbres": self.arbres
        }
        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=4, ensure_ascii=False)
        print(f"✅ Modèle sauvegardé avec succès dans : {filepath}")