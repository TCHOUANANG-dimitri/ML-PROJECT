import numpy as np
import json
import matplotlib.pyplot as plt

class Node:
    def __init__(self):
        self.feature=None # index de feature utiliser pour le split
        self.threshold=None # valeur de seuil pour le split
        self.prediction=None # valeur de prediction
        self.left=None # noeud enfant a gauche
        self.right=None # noeud enfant a droite


class XGBoostRegressor:

    def __init__(self, profondeur_max=10, min_gain=1e-5, n_trees=10, 
                 learning_rate=0.3, reg_lambda=1.0):
        self.profondeur_max = profondeur_max
        self.min_gain = min_gain
        self.n_trees = n_trees
        self.learning_rate = learning_rate
        self.reg_lambda = reg_lambda  #  Régularisation
        self.forest = []
        self.init = None

    def fit(self, X, y):
        # Initialisation: prédiction de base (moyenne)
        self.init = np.mean(y)
        F = np.full(len(y), self.init)  # Prédictions actuelles
            
        for i in range(self.n_trees):
                #  Calcul des gradients et hessians
                #  gradient = -(y - F), hessian = 1
            gradients = -(y - F)  
            hessians = np.ones(len(y))  
                
                # Construire un arbre sur les gradients (avec hessians)
            tree = self.build_tree(X, gradients, hessians)
                
                # Prédictions de l'arbre
            preds = self.predict_tree(tree, X)
                
                # Mise à jour des prédictions avec learning rate
            F += self.learning_rate * preds
                
                # Stocker l'arbre
            self.forest.append(tree)
            
            '''# Visualisation: nuage de points gradient vs hessian
            plt.figure(figsize=(10, 6))
            sizes = np.abs(preds) * 100  # Taille des points basée sur la prédiction
            plt.scatter(gradients, hessians, s=sizes, alpha=0.6, c=preds, cmap='viridis')
            plt.xlabel('Gradient')
            plt.ylabel('Hessian')
            plt.title('Gradient vs Hessian (taille = valeur prédite)')
            plt.colorbar(label='Prédiction')
            plt.grid(True)
            plt.tight_layout()
            plt.show()'''
    
    def build_tree(self, X, gradients, hessians, profondeur=10):
        
        node = Node()
        
        # Calcul de la prédiction optimale pour cette feuille
        # Formule: -sum(gradients) / (sum(hessians) + lambda)
        G = np.sum(gradients)  # Somme des gradients
        H = np.sum(hessians)   # Somme des hessians
        node.prediction = -G / (H + self.reg_lambda)
        
        # Critères d'arrêt
        if profondeur >= self.profondeur_max or len(gradients) <= 1:
            return node
        
        n_features = X.shape[1]
        meilleur_gain = 0
        meilleur_feature = None
        meilleur_seuil = None
        
        # Calcul du score de base (avant split)
        # Formule XGBoost: score = -0.5 * G^2 / (H + lambda)
        score_base = -0.5 * (G**2) / (H + self.reg_lambda)
        
        # Recherche du meilleur split
        for j in range(n_features):
            valeurs_uniques = np.unique(X[:, j])
            
            for seuil in valeurs_uniques:
                gauche_idx = X[:, j] <= seuil
                droite_idx = X[:, j] > seuil
                
                if np.sum(gauche_idx) == 0 or np.sum(droite_idx) == 0:
                    continue
                
                # Séparer les gradients et hessians
                g_gauche = gradients[gauche_idx]
                h_gauche = hessians[gauche_idx]
                g_droite = gradients[droite_idx]
                h_droite = hessians[droite_idx]
                
                # Sommes pour gauche et droite
                G_L = np.sum(g_gauche)
                H_L = np.sum(h_gauche)
                G_R = np.sum(g_droite)
                H_R = np.sum(h_droite)
                
                # Calcul du gain selon la formule XGBoost
                # Gain = 0.5 * [G_L^2/(H_L+lambda) + G_R^2/(H_R+lambda) - G^2/(H+lambda)]
                score_gauche = (G_L**2) / (H_L + self.reg_lambda)
                score_droite = (G_R**2) / (H_R + self.reg_lambda)
                gain = 0.5 * (score_gauche + score_droite - (G**2)/(H + self.reg_lambda))
                
                # Mise à jour du meilleur split
                if gain > meilleur_gain:
                    meilleur_gain = gain
                    meilleur_feature = j
                    meilleur_seuil = seuil
        
        # Vérifier si le gain est suffisant
        if meilleur_gain < self.min_gain or meilleur_feature is None:
            return node
        
        # Stocker le split
        node.feature = meilleur_feature
        node.threshold = meilleur_seuil
        node.gain = meilleur_gain
        
        # Récursion sur les enfants
        gauche_idx = X[:, node.feature] <= node.threshold
        droite_idx = X[:, node.feature] > node.threshold
        
        node.left = self.build_tree(
            X[gauche_idx], 
            gradients[gauche_idx], 
            hessians[gauche_idx], 
            profondeur + 1
        )
        node.right = self.build_tree(
            X[droite_idx], 
            gradients[droite_idx], 
            hessians[droite_idx], 
            profondeur + 1
        )
        
        return node

    def predict_one(self, tree, x):
        if tree.left is None and tree.right is None:
            return tree.prediction
        if x[tree.feature] <= tree.threshold:
            return self.predict_one(tree.left, x)
        else:
            return self.predict_one(tree.right, x)

    def predict_tree(self, tree, X):
        return np.array([self.predict_one(tree, x) for x in X])

    def predict(self, X):
        F = np.full(len(X), self.init)
        for tree in self.forest:
            F += self.learning_rate * self.predict_tree(tree, X)
        return F

    def score(self, X, y):
        y_pred = self.predict(X)
        return 1 - (np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2))

    def save(self, nom):
        def node_to_dict(node):
            if node is None:
                return None
            return {
                'feature': int(node.feature) if node.feature is not None else None,
                'threshold': float(node.threshold) if node.threshold is not None else None,
                'prediction': float(node.prediction) if node.prediction is not None else None,
                'gain': float(getattr(node, 'gain', 0)) if hasattr(node, 'gain') else None,
                'left': node_to_dict(node.left),
                'right': node_to_dict(node.right),
            }

        data = {
            'profondeur_max': self.profondeur_max,
            'min_gain': self.min_gain,
            'n_trees': self.n_trees,
            'learning_rate': self.learning_rate,
            'reg_lambda': self.reg_lambda,
            'init': float(self.init) if self.init is not None else None,
            'forest': [node_to_dict(tree) for tree in self.forest]
        }
        with open(nom, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, nom):
        def dict_to_node(d):
            if d is None:
                return None
            node = Node()
            node.feature = d['feature']
            node.threshold = d['threshold']
            node.prediction = d['prediction']
            if d.get('gain') is not None:
                node.gain = d['gain']
            node.left = dict_to_node(d['left'])
            node.right = dict_to_node(d['right'])
            return node

        with open(nom, 'r', encoding='utf-8') as f:
            data = json.load(f)
        model = cls(profondeur_max=data.get('profondeur_max', 10),
                    min_gain=data.get('min_gain', 1e-5),
                    n_trees=data.get('n_trees', 2),
                    learning_rate=data.get('learning_rate', 0.3),
                    reg_lambda=data.get('reg_lambda', 1.0))
        model.init = data.get('init', None)
        model.forest = [dict_to_node(t) for t in data.get('forest', [])]
        return model