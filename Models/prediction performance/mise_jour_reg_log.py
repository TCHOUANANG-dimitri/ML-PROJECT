#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

class RegressionLogistique:

    def __init__ (self, learning_rate=0.01, n_iterations=1000): # déclare une méthode privée
        self.lr = learning_rate       
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
        self.cost = []
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def _add_bias(self, X):
        b = np.ones((X.shape[0], 1))
        X = np.hstack((b, X))
        return X # fait une conaténation horizontale de b et X
    
    def predict_proba(self, X):
        X = self._add_bias(X)
        z = X @ self.weights 
        y_pred = self.sigmoid(z) 
        return y_pred
    
    
    def _cost_function(self, X, y): # la fonction coût mésure l'erreur
        m = len(y)
        z = X @ self.weights 
        y_pred = self.sigmoid(z)
        return -(1/m) * np.sum(
            y * np.log(y_pred + np.exp(-15)) + (1 - y) * np.log(1 - y_pred + np.exp(-15))
        ) # On ajoute exp(-15) pour éviter d'avoir 0
    
    def _gradient(self, X, y): # le gradint dit comment réduire l'erreur
        m = len(y)
        z = X @ self.weights 
        y_pred = self.sigmoid(z)
        return (1/m) * X.T @ (y_pred - y)
    
    def fit(self, X, y): 
        n_samples, n_features = X.shape
        X = self._add_bias(X)
        y = y.reshape(-1, 1)
        self.weights = np.zeros((X.shape[1], 1))
        self.bias = 0
        self.cost = []
  
        for i in range(self.n_iterations): # Algorithme de descente du gradient
            self.weights -= self.lr * self._gradient(X, y)
            self.cost.append(self._cost_function(X, y))
        
        return self
    
    
    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)
           
    def score(self, X, y):
        y = y.reshape(-1, 1) # redimensionne y de telle sorte que numpy calcule automatiquement la dim correspondante (-1) et 1 colonne
        y_pred = self.predict(X)
        return np.mean(y_pred == y)
    
    def save_json(self, filepath):
        params = {
            'weights': self.weights.tolist() if self.weights is not None else None,
            'bias': self.bias if self.bias is not None else None,
            'learning_rate': self.lr,
            'n_iterations': self.n_iterations,
            'cost': self.cost
        }
        
        with open(filepath, 'w') as f:
            json.dump(params, f, indent=4)
        print(f"✓ Modèle sauvegardé en JSON dans {filepath}")
    
    @classmethod
    def load_json(cls, filepath):
        with open(filepath, 'r') as f:
            params = json.load(f)
        
        model = cls(
            learning_rate=params['learning_rate'],
            n_iterations=params['n_iterations']
        )
        model.weights = np.array(params['weights']) if params['weights'] is not None else None
        model.bias = params['bias']
        model.cost = params['cost']
        print(f"✓ Modèle chargé depuis {filepath}")
        return model
    
    def plot_cost(self):
        plt.figure(figsize=(8,5))
        plt.plot(self.cost)
        plt.xlabel("Itérations")
        plt.ylabel("Coût J(θ)")
        plt.title("Convergence de la descente de gradient")
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def plot_probabilities(self, X, y):
        probs = self.predict_proba(X).flatten()
        plt.figure(figsize=(8,5))
        plt.hist(probs[y == 0], bins=20, alpha=0.6, label="Classe 0")
        plt.hist(probs[y == 1], bins=20, alpha=0.6, label="Classe 1")
        plt.legend()
        plt.xlabel("Probabilité prédite")
        plt.ylabel("Fréquence")
        plt.title("Distribution des probabilités")
        plt.show()

def train_test_split(X, y, test_size=0.2, random_state=None):
    """
    Divise les données en ensembles d'entraînement et de test
    """
    if random_state is not None:
        np.random.seed(random_state)
    
    # Nombre total d'échantillons
    n_samples = X.shape[0]
    
    # Nombre d'échantillons de test
    n_test = round(n_samples * test_size)
    
    # Indices mélangés aléatoirement
    indices = np.random.permutation(n_samples)
    
    # Indices de test et d'entraînement
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]
    
    # Séparation des données
    X_train = X[train_indices]
    X_test = X[test_indices]
    y_train = y[train_indices]
    y_test = y[test_indices]
    
    return X_train, X_test, y_train, y_test


def roc_curve_from_scratch(y_true, y_scores, n_thresholds=100):
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
        FPR.append(fpr) #append permet d'ajouter la valeur actuelle à la liste
    return np.array(FPR), np.array(TPR)


# ============================================
# 4. MATRICE DE CONFUSION 
# ============================================
def confusion_matrix(y_true, y_pred):
    """
    Calcule la matrice de confusion
    """
    y_true = y_true.flatten()
    y_pred = y_pred.flatten()
    
    TP = np.sum((y_pred == 1) & (y_true == 1))
    TN = np.sum((y_pred == 0) & (y_true == 0))
    FP = np.sum((y_pred == 1) & (y_true == 0))
    FN = np.sum((y_pred == 0) & (y_true == 1))
    
    return TN, FP,FN, TP


def afficher_metriques(y_true, y_pred, nom="jeu"):
    TN, FP, FN, TP = confusion_matrix(y_true, y_pred)
    """
    Affiche les métriques de performance
    """
    
    # Métriques
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print("\n" + "="*50)
    print("MÉTRIQUES DE PERFORMANCE")
    print("="*50)
    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-Score  : {f1_score:.4f}")
    print("\nMatrice de confusion:")
    print(f"                Prédit 0    Prédit 1")
    print(f"Vrai 0 (TN/FP):    {TN:4d}       {FP:4d}")
    print(f"Vrai 1 (FN/TP):    {FN:4d}       {TP:4d}")
    print("="*50)



# In[ ]:


get_ipython().system('git')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




