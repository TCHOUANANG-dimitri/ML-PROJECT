import numpy as np
import json

class DBSCAN:
    def __init__(self, eps=1, min_points=5):  
        self.eps = eps             # distance max entre deux points pour les consideré comme voisin
        self.min_points = min_points       # nombre min de points pour former un cluster
        self.labels_ = None  # Pour stocker les labels des clusters 
        self.X_ = None     # pour stocker les données d'entrainement 
    
    def fit(self, X):
        X = np.array(X, dtype=float)
        self.X_ = X
        n_samples = X.shape[0]
        
        # Initialisation des labels (-1 = bruit, 0 ou plus = cluster)
        self.labels_ = np.full(n_samples, -1)      # creee un vecteur de n_samples elements comstituer de -1 (indice du bruit)
        cluster_id = 0     # commencons les cluster à 0
        
        for i in range(n_samples):
            # Si déjà visité, passer
            if self.labels_[i] != -1:
                continue     # si ca a deja un numero de cluster continuer 
            
            # Trouver les voisins du point i
            voisins = self.get_voisins(i, X)
            
            # Si pas assez de voisins, marquer comme bruit
            if len(voisins) < self.min_points:
                self.labels_[i] = -1  # Bruit
            else:
                # Créer un nouveau cluster
                self.expand_cluster(i, voisins, cluster_id, X)
                cluster_id += 1
        
        return self
    
    def get_voisins(self, point_idx, X):
        """Retourne les indices des voisins d'un point"""
        voisins = []
        
        for i in range(X.shape[0]):
            # Distance euclidienne (distance entre deux vecteurs)
            distance = np.sqrt(np.sum((X[point_idx] - X[i]) ** 2))
            
            # Si dans le rayon eps
            if distance <= self.eps:
                voisins.append(i)
        
        return voisins
    
    def expand_cluster(self, point_idx, voisins, cluster_id, X):
        """Étend le cluster en explorant les voisins"""
        self.labels_[point_idx] = cluster_id
        
        i = 0
        while i < len(voisins):
            voisin_idx = voisins[i]
            
            # Si pas encore visité
            if self.labels_[voisin_idx] == -1:
                self.labels_[voisin_idx] = cluster_id
                
                # Trouver les voisins de ce voisin
                nouveaux_voisins = self.get_voisins(voisin_idx, X)
                
                # Si c'est un core point, ajouter ses voisins
                if len(nouveaux_voisins) >= self.min_points:
                    voisins.extend(nouveaux_voisins)
            
            i += 1

    
    def predict(self, X):
        """
        Assigne de nouveaux points aux clusters existants.
        
        Logique :
        - Pour chaque nouveau point, trouve le point le plus proche dans X_train
        - Si la distance <= eps, assigne le label de ce point
        - Sinon, marque comme bruit (-1)
        """
        if self.labels_ is None or self.X_ is None:
            raise ValueError("Le modèle n'a pas encore été entraîné. Appelez fit() d'abord.")
        
        X = np.array(X, dtype=float)
        new_labels = []
        
        for point in X:
            # Calculer les distances avec tous les points d'entraînement
            distances = np.sqrt(np.sum((self.X_ - point) ** 2, axis=1))
            
            # Trouver le point le plus proche
            nearest_idx = np.argmin(distances)
            min_distance = distances[nearest_idx]
            
            # Si assez proche, prendre son label, sinon bruit (-1)
            if min_distance <= self.eps:
                new_labels.append(self.labels_[nearest_idx])
            else:
                new_labels.append(-1)  # Bruit
        
        return np.array(new_labels)
    
    def fit_predict(self, X):
        # Entraîne et retourne les labels en une seule étape
        self.fit(X)
        return self.labels_



    def save(self, nom_fichier):
        """
        Sauvegarde le modèle dans un fichier JSON
        
        Args:
            nom_fichier: Chemin du fichier de sauvegarde (ex: 'modele.json')
        """
        if self.labels_ is None:
            raise ValueError("Aucun modèle à sauvegarder. Entraînez d'abord avec fit().")
        
        modele = {
            'eps': self.eps,
            'min_points' : self.min_points,
            'labels_': self.labels_,
            'donnees': self.X_,
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
        
        self.eps = modele['eps']
        self.min_points = modele['min_points']
        self.labels_ = modele['labels_']
        self.X_ = modele['donnees']
        
        print(f"✓ Modèle chargé depuis '{nom_fichier}'")
        
        return self


