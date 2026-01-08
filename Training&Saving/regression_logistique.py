import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

class RegressionLogistique:
    def __init__(self, learning_rate=0.01, n_iterations=1000): # constructeur 
        ''''''
        Initialisation de la régression logistique
        
        Parameters:
        -----------
        learning_rate : float
            Taux d'apprentissage pour la descente de gradient ( c'est le pas de déscente de gradient)
        n_iterations : int
            Nombre d'itérations pour l'entraînement
        ''''''
        self.lr = learning_rate # stocke learning_rate passée dans paramétre dans l'attribut self.learning_rate       
        self.n_iterations = n_iterations
        self.weights = None # crée l'attribut self.weights qui est encore vide
        self.bias = None # crée l'attribut self.biais qui est initialement vide
        self.cost = [] # crée une liste vide qui sera remplit pendant l'entraînement
    
    def sigmoid(self, z):
        ''''''
        Fonction sigmoïde : 1 / (1 + e^(-z))
        ''''''
        return 1 / (1 + np.exp(-z))
    
    def _add_bias(self, X):
        # Crée une colonne de 1 (biais)
        b = np.ones((X.shape[0], 1))
        
        # Concatène la colonne de biais avec les données
        return np.hstack((b, X))

    def _cost_function(self, X, y):
        # Nombre d'exemples
        m = len(y)
        
        # Probabilités prédites
        z = X @ self.weights 
        y_pred = self.sigmoid(z)
        
        # Calcul de la fonction coût de la régression logistique
        return -(1/m) * np.sum(
            y * np.log(y_pred + np.exp(-15)) + (1 - y) * np.log(1 - y_pred + np.exp(-15))
        )

    def _gradient(self, X, y):
        # Nombre d'exemples
        m = len(y)
        z = X @ self.weights 
        # Probabilités prédites
        y_pred = self.sigmoid(z)
        
        # Calcul du gradient ∇J(θ)
        return (1/m) * X.T @ (y_pred - y)
    
    def fit(self, X, y): 
        ''''''
        Entraînement du modèle
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Données d'entraînement
        y : array-like, shape (n_samples,)
            Labels (0 ou 1)
        ''''''
        n_samples, n_features = X.shape # crée la matrice X de n_samples lignes et n_features colonnes
        
        # Ajout du biais aux données
        X = self._add_bias(X)
       
        # S'assure que y est un vecteur colonne
        y = y.reshape(-1, 1)
 
        # Initialisation des poids et du biais
        self.weights = np.zeros((X.shape[1], 1))
        self.bias = 0
        
        # Réinitialisation de l'historique des coûts
        self.cost = []
  
        # Descente de gradient
        for i in range(self.n_iterations):
            # Mise à jour des paramètres
            self.weights -= self.lr * self._gradient(X, y)
            
            # Calcul et sauvegarde du coût
            self.cost.append(self._cost_function(X, y))
            
        # Permet l'appel en chaîne (model.fit().predict())
        return self
    
    def predict_proba(self, X):
        # Ajout du biais
        X = self._add_bias(X)
        z = X @ self.weights 
        # Retourne P(y=1|x)
        return self.sigmoid(z)

    def predict(self, X, threshold=0.5):
        # Retourne 1 si proba >= seuil, sinon 0
        return (self.predict_proba(X) >= threshold).astype(int)
           
    def score(self, X, y):
        ''''''
        Calculer la précision (accuracy)
        ''''''
        # Mise en forme de y
        y = y.reshape(-1, 1)
        y_pred = self.predict(X)
        return np.mean(y_pred == y)
    
    def save_json(self, filepath):
        ''''''Sauvegarde les paramètres du modèle en JSON''''''
        params = {
            'weights': self.weights.tolist() if self.weights is not None else None,
            'bias': float(self.bias) if self.bias is not None else None,
            'learning_rate': self.lr,
            'n_iterations': self.n_iterations,
            'cost': self.cost
        }
        
        with open(filepath, 'w') as f:
            json.dump(params, f, indent=4)
        print(f'Modèle sauvegardé en JSON dans {filepath}')
    
    @classmethod
    def load_json(cls, filepath):
        ''''''Charge les paramètres du modèle depuis JSON''''''
        with open(filepath, 'r') as f:
            params = json.load(f)
        
        model = cls(
            learning_rate=params['learning_rate'],
            n_iterations=params['n_iterations']
        )
        model.weights = np.array(params['weights']) if params['weights'] is not None else None
        model.bias = params['bias']
        model.cost = params['cost']
        print(f'Modèle chargé depuis {filepath}')
        return model

    def plot_cost(self):
        # Trace l'évolution du coût
        plt.plot(self.cost)
        plt.xlabel('Itérations')
        plt.ylabel('Coût J(θ)')
        plt.title('Convergence de la descente de gradient')
        plt.show()
        
    def plot_probabilities(self, X, y):
        # Calcul des probabilités prédites
        probs = self.predict_proba(X).flatten()

        # Histogramme pour la classe 0
        plt.hist(probs[y == 0], bins=20, alpha=0.6, label='Classe 0')
        
        # Histogramme pour la classe 1
        plt.hist(probs[y == 1], bins=20, alpha=0.6, label='Classe 1')
        
        plt.legend()
        plt.title('Distribution des probabilités')
        plt.show()


def roc_curve_from_scratch(y_true, y_scores, n_thresholds=100):
    ''''''Calcule la courbe ROC from scratch''''''
    thresholds = np.linspace(0, 1, n_thresholds)

    TPR = []
    FPR = []

    for t in thresholds:
        y_pred = (y_scores >= t).astype(int)

        TP = np.sum((y_pred == 1) & (y_true == 1))
        TN = np.sum((y_pred == 0) & (y_true == 0))
        FP = np.sum((y_pred == 1) & (y_true == 0))
        FN = np.sum((y_pred == 0) & (y_true == 1))

        tpr = TP / (TP + FN) if (TP + FN) != 0 else 0
        fpr = FP / (FP + TN) if (FP + TN) != 0 else 0

        TPR.append(tpr)
        FPR.append(fpr)

    return np.array(FPR), np.array(TPR)


# Exemple d'utilisation
if __name__ == '__main__':
    print('Module de Régression Logistique chargé avec succès!')
    print('Importez la classe avec: from regression_logistique import RegressionLogistique')
