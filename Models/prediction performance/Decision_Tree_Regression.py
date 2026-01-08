import json
import numpy as np

class ArbreRegression:
    """
    Arbre de régression pour prédire la moyenne des étudiants
    Utilise la réduction de variance comme critère de division
    """
    
    def __init__(self, profondeur_max=5, min_echantillons=2, min_variance=0.01):
        """
        Constructeur de l'arbre de régression
        
        Args:
            profondeur_max: Profondeur maximale de l'arbre
            min_echantillons: Nombre minimum d'échantillons pour diviser un noeud
            min_variance: Variance minimale pour continuer à diviser
        """
        self.profondeur_max = profondeur_max
        self.min_echantillons = min_echantillons
        self.min_variance = min_variance
        self.arbre = None
        self.n_features = None
    
    def fit(self, X, y):
        """
        Entraîne l'arbre de régression sur les données
        
        Args:
            X: Caractéristiques (numpy array ou liste) - shape (n_samples, n_features)
            y: Valeurs cibles (moyennes des étudiants) - shape (n_samples,)
        """
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)
        
        # Vérifier les dimensions
        if len(X.shape) == 1:
            X = X.reshape(-1, 1)
        
        self.n_features = X.shape[1]
        
        # Construire l'arbre récursivement
        self.arbre = self._construire_arbre(X, y, profondeur=0)
        
        return self
    
    def _construire_arbre(self, X, y, profondeur):
        """
        Construit récursivement l'arbre de régression
        Utilise la variance comme critère de division
        """
        n_echantillons = len(y)
        variance_actuelle = np.var(y)
        
        # Conditions d'arrêt
        if (profondeur >= self.profondeur_max or 
            n_echantillons < self.min_echantillons or
            variance_actuelle < self.min_variance):
            # Créer une feuille avec la moyenne
            return {
                'feuille': True,
                'valeur': np.mean(y),
                'n_echantillons': n_echantillons,
                'variance': variance_actuelle
            }
        
        # Trouver la meilleure division
        meilleure_feature, meilleur_seuil, meilleur_gain = self._meilleure_division(X, y)
        
        # Si aucun gain significatif, créer une feuille
        if meilleur_gain <= 0 or meilleure_feature is None:
            return {
                'feuille': True,
                'valeur': np.mean(y),
                'n_echantillons': n_echantillons,
                'variance': variance_actuelle
            }
        
        # Diviser les données selon le meilleur critère
        indices_gauche = X[:, meilleure_feature] <= meilleur_seuil
        indices_droite = X[:, meilleure_feature] > meilleur_seuil
        
        # Vérifier que la division n'est pas vide
        if np.sum(indices_gauche) == 0 or np.sum(indices_droite) == 0:
            return {
                'feuille': True,
                'valeur': np.mean(y),
                'n_echantillons': n_echantillons,
                'variance': variance_actuelle
            }
        
        # Construire les sous-arbres récursivement
        gauche = self._construire_arbre(X[indices_gauche], y[indices_gauche], profondeur + 1)
        droite = self._construire_arbre(X[indices_droite], y[indices_droite], profondeur + 1)
        
        return {
            'feuille': False,
            'feature': int(meilleure_feature),
            'seuil': float(meilleur_seuil),
            'gauche': gauche,
            'droite': droite,
            'gain': float(meilleur_gain),
            'n_echantillons': n_echantillons
        }
    
    def _meilleure_division(self, X, y):
        """
        Trouve la meilleure division en maximisant la réduction de variance
        
        Returns:
            meilleure_feature: Index de la meilleure caractéristique
            meilleur_seuil: Meilleur seuil de division
            meilleur_gain: Meilleure réduction de variance
        """
        n_echantillons, n_features = X.shape
        
        if n_echantillons <= 1:
            return None, None, 0
        
        # Variance avant division
        variance_parent = np.var(y)
        meilleur_gain = 0
        meilleure_feature = None
        meilleur_seuil = None
        
        # Parcourir toutes les caractéristiques
        for feature in range(n_features):
            # Obtenir les valeurs uniques triées
            valeurs_uniques = np.unique(X[:, feature])
            
            # Si une seule valeur, pas de division possible
            if len(valeurs_uniques) <= 1:
                continue
            
            # Tester chaque seuil possible (point milieu entre valeurs consécutives)
            for i in range(len(valeurs_uniques) - 1):
                seuil = (valeurs_uniques[i] + valeurs_uniques[i + 1]) / 2.0
                
                # Diviser les données
                indices_gauche = X[:, feature] <= seuil
                indices_droite = X[:, feature] > seuil
                
                # Vérifier que les deux groupes sont non vides
                n_gauche = np.sum(indices_gauche)
                n_droite = np.sum(indices_droite)
                
                if n_gauche == 0 or n_droite == 0:
                    continue
                
                # Calculer les variances des deux groupes
                y_gauche = y[indices_gauche]
                y_droite = y[indices_droite]
                
                var_gauche = np.var(y_gauche)
                var_droite = np.var(y_droite)
                
                # Calculer la variance pondérée après division
                variance_enfants = (n_gauche / n_echantillons) * var_gauche + \
                                   (n_droite / n_echantillons) * var_droite
                
                # Calculer le gain (réduction de variance)
                gain = variance_parent - variance_enfants
                
                # Mettre à jour si meilleur gain
                if gain > meilleur_gain:
                    meilleur_gain = gain
                    meilleure_feature = feature
                    meilleur_seuil = seuil
        
        return meilleure_feature, meilleur_seuil, meilleur_gain
    
    def predict(self, X):
        """
        Prédit les valeurs de régression pour de nouveaux échantillons
        
        Args:
            X: Caractéristiques - shape (n_samples, n_features)
            
        Returns:
            predictions: Valeurs prédites - shape (n_samples,)
        """
        if self.arbre is None:
            raise ValueError("Le modèle n'a pas été entraîné. Appelez fit() d'abord.")
        
        X = np.array(X, dtype=float)
        
        # Gérer le cas d'un seul échantillon
        if len(X.shape) == 1:
            X = X.reshape(1, -1)
        
        # Prédire pour chaque échantillon
        predictions = np.array([self._predire_un(x, self.arbre) for x in X])
        
        return predictions
    
    def _predire_un(self, x, noeud):
        """
        Prédit pour un seul échantillon en descendant dans l'arbre
        
        Args:
            x: Un échantillon
            noeud: Noeud actuel de l'arbre
            
        Returns:
            valeur: Valeur prédite
        """
        # Si c'est une feuille, retourner la valeur moyenne
        if noeud['feuille']:
            return noeud['valeur']
        
        # Sinon, descendre dans l'arbre selon la condition
        if x[noeud['feature']] <= noeud['seuil']:
            return self._predire_un(x, noeud['gauche'])
        else:
            return self._predire_un(x, noeud['droite'])
    
    def score(self, X, y):
        """
        Calcule le coefficient de détermination R² du modèle
        R² = 1 - (SS_res / SS_tot)
        
        Args:
            X: Caractéristiques de test
            y: Valeurs réelles
            
        Returns:
            r2_score: Score R² (1.0 = parfait, 0.0 = médiocre, <0 = très mauvais)
        """
        y = np.array(y, dtype=float)
        predictions = self.predict(X)
        
        # Somme des carrés des résidus
        ss_res = np.sum((y - predictions) ** 2)
        
        # Somme totale des carrés
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        
        # Éviter division par zéro
        if ss_tot == 0:
            return 0.0 if ss_res == 0 else -np.inf
        
        # Calculer R²
        r2 = 1.0 - (ss_res / ss_tot)
        
        # Calculer aussi le RMSE (erreur quadratique moyenne)
        rmse = np.sqrt(np.mean((y - predictions) ** 2))
        
        print(f"R² Score: {r2:.4f}")
        print(f"RMSE: {rmse:.4f}")
        
        return r2
    
    def save(self, nom_fichier):
        """
        Sauvegarde le modèle dans un fichier JSON
        
        Args:
            nom_fichier: Chemin du fichier de sauvegarde (ex: 'modele.json')
        """
        if self.arbre is None:
            raise ValueError("Aucun modèle à sauvegarder. Entraînez d'abord avec fit().")
        
        modele = {
            'arbre': self.arbre,
            'profondeur_max': self.profondeur_max,
            'min_echantillons': self.min_echantillons,
            'min_variance': self.min_variance,
            'n_features': self.n_features
        }
        
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            json.dump(modele, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Modèle sauvegardé dans '{nom_fichier}'")
    
    def load(self, nom_fichier):
        """
        Charge un modèle depuis un fichier JSON
        
        Args:
            nom_fichier: Chemin du fichier à charger
        """
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            modele = json.load(f)
        
        self.arbre = modele['arbre']
        self.profondeur_max = modele['profondeur_max']
        self.min_echantillons = modele['min_echantillons']
        self.min_variance = modele['min_variance']
        self.n_features = modele['n_features']
        
        print(f"✓ Modèle chargé depuis '{nom_fichier}'")
        
        return self


