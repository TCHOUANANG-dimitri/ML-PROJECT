import numpy as np
import pandas as pd

class Node:
    def __init__(self):
        self.feature=None # index de feature utiliser pour le split
        self.threshold=None # valeur de seuil pour le split
        self.prediction=None # valeur de prediction
        self.left=None # noeud enfant a gauche
        self.right=None # noeud enfant a droite


class decisionTreeRegressor: # Class arbre de decision regressif
    def __init__(self,profondeur_max=20,min_gain=0.0001): # constructeur: il permet d'initialiser les attributs (dans notre cas les hyperparametres d'une instance (objet)
        self.profondeur_max=profondeur_max
        self.min_gain=min_gain
        self.root=None
        self.last_predict=None

    def fit(self,X,y): # Fonction permettant l'entrainement du modele en utilisant l'arbre construit dans la fonction plus bas
        self.root=self.build_tree(X,y)
    
    def build_tree(self,X,y,seuil_min_gain=0.0001,profondeur_max=20,profondeur=0):
        node=Node() # creation du noeud racine
        node.prediction=np.mean(y) # initialisation de la prediction/racine (moyenne de la target)
        variance_parent=np.var(y) # initialisation de la variance de la racine (variance de la target)
        meilleur_gain=0
        meilleur_feature=None
        meilleur_seuil=None
    
        # critere d'arret
        if profondeur>=profondeur_max or len(y)<=1 or variance_parent==0:
            return node
        n_features=X.shape[1] # compte le nombre de features
        # parcour tous les features pour rechercher le celui qui permet d'avoir le meilleur gain d'informations
        # ainsi la valeur de seuil de split (decoupage)
        for j in range(n_features):   # parcours de chaque feature
            valeurs_uniques=np.unique(X[:,j])
            for seuil in valeurs_uniques: # decoupage en split (deux sous groupes)
                gauche_idx=X[:,j]<=seuil
                droite_idx=X[:,j]>seuil
                if np.sum(gauche_idx)==0 or np.sum(droite_idx)==0:
                    continue
                y_gauche=y[gauche_idx]
                y_droite=y[droite_idx] 
                # calcul du gain d'informations
                erreur_apres=(len(y_gauche)/len(y))*np.var(y_gauche)+(len(y_droite)/len(y))*np.var(y_droite) # moyenne ponderer des varinces des splits
                gain=variance_parent-erreur_apres
                # recherche du meilleur split (maximisant le gain d'informations)
                if(gain>meilleur_gain):
                    meilleur_gain=gain
                    meilleur_feature=j
                    meilleur_seuil=seuil
        # stocker le split
        node.feature=meilleur_feature
        node.threshold=meilleur_seuil
        # verifier si le gain est significatif ou pas
        if meilleur_gain<seuil_min_gain or meilleur_feature is None:
            return node
        # application recursive de l'algorithme sur les noeuds enfants gauche et droit
        gauche_idx=X[:,node.feature]<=node.threshold
        droite_idx=X[:,node.feature]>node.threshold
        node.left=self.build_tree(X[gauche_idx],y[gauche_idx],seuil_min_gain,profondeur_max,profondeur+1)
        node.right=self.build_tree(X[droite_idx],y[droite_idx],seuil_min_gain,profondeur_max,profondeur+1)
        return node

    def predict_one(self,x): # effectue une prediction pour une seule instance ( un vecteur en entrer , unscalaire en sortie)
        return self.predict_recursive(self.root,x)
        
    def predict_recursive(self,node,x):
        if node.left is None and node.right is None:
            return node.prediction
        if x[node.feature]<=node.threshold:
            return self.predict_recursive(node.left,x)
        else:
            return self.predict_recursive(node.right,x)

    def predict(self,X): # effectue une prediction pour plusieurs vecteurs (plusieurs vecteurs en entrez un vecteur de valeurs predite en sortie
        self.last_predict=np.array([self.predict_one(x) for x in X])
        return self.last_predict
        
    def score(self,X,y): # Calcul du coefficient de determination 
        y_pred = self.predict(X)
        return 1-(np.sum((y-y_pred)**2)/np.sum((y-np.mean(y))**2))
    def save(self,nom):
        joblib.dump(self,nom)
        print("modele sauvegarder")
        
    @classmethod
    def load(self,nom):
        model=joblib.load(nom)
        return model