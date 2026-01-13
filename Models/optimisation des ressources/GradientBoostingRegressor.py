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


class GradientBoostingRegressor: # Class arbre de decision regressif
    def __init__(self,profondeur_max=10,min_gain=1e-5,n_trees=10,learning_rate=0.5): # constructeur: il permet d'initialiser les attributs (dans notre cas les hyperparametres d'une instance (objet)
        self.profondeur_max=profondeur_max
        self.min_gain=min_gain
        self.n_trees=n_trees
        self.learning_rate=learning_rate # taux d'apprentissage
        self.forest=[] # definition de la foret
        self.init=None

    def fit(self,X,y): # Fonction permettant l'entrainement du modele en utilisant l'arbre construit dans la fonction plus bas
        r=y-np.mean(y) # calcul des residus initiaux
        self.init=np.mean(y)
        F=np.full(len(y),self.init)
        for i in range(self.n_trees): # construction des differents arbres suivant le nombre fixe
            tree=self.build_tree(X,r) # entrainement sur les residus
            preds=self.predict_tree(tree,X) # prediction locale
            F+= self.learning_rate*preds # mise a jour de la prediction globale
            r=y-F # mise a jour des residus
            self.forest.append(tree) # ajout de l'arbre entrainer a la foret
    
    def build_tree(self,X,y,seuil_min_gain=1e-5,profondeur_max=10,profondeur=0):
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
        if meilleur_gain<seuil_min_gain:
            return node
        # application recursive de l'algorithme sur les noeuds enfants gauche et droit
        gauche_idx=X[:,node.feature]<=node.threshold
        droite_idx=X[:,node.feature]>node.threshold
        node.left=self.build_tree(X[gauche_idx],y[gauche_idx],seuil_min_gain,profondeur_max,profondeur+1)
        node.right=self.build_tree(X[droite_idx],y[droite_idx],seuil_min_gain,profondeur_max,profondeur+1)
        return node

    def predict_one(self,tree,x): # effectue une prediction pour une seule instance ( un vecteur en entrer , un scalaire en sortie). Ici se sont les residus qui sont predit
        if tree.left is None and tree.right is None:
            return tree.prediction
        if x[tree.feature]<=tree.threshold:
            return self.predict_one(tree.left,x)
        else:
            return self.predict_one(tree.right,x)

    def predict_tree(self,tree,X): # effectue une prediction pour plusieurs vecteurs (plusieurs vecteurs en entrez un vecteur de valeurs predite en sortie
        return np.array([self.predict_one(tree,x) for x in X])


    def predict(self, X):
        F = np.full(len(X), self.init)
        for tree in self.forest:
            F += self.learning_rate * self.predict_tree(tree, X)
        return F
        ''' plt.figure(figsize=(12, 6))
        for idx, tree in enumerate(self.forest):
                predictions = self.predict_tree(tree, X)
                plt.plot(predictions, label=f'Tree {idx+1}', alpha=0.7)
        plt.xlabel('Index')
        plt.ylabel('Valeur predite')
        plt.title('Predictions de chaque arbre dans la foret')
        plt.legend()
        plt.show()'''

    def score(self,X,y): # Calcul du coefficient de determination
        y_pred=self.predict(X)
        return 1-(np.sum((y-y_pred)**2)/np.sum((y-y.mean())**2))

    def save(self, nom):
        def node_to_dict(node):
            if node is None:
                return None
            return {
                'feature': int(node.feature) if node.feature is not None else None,
                'threshold': float(node.threshold) if node.threshold is not None else None,
                'prediction': float(node.prediction) if node.prediction is not None else None,
                'left': node_to_dict(node.left),
                'right': node_to_dict(node.right),
            }

        data = {
            'profondeur_max': self.profondeur_max,
            'min_gain': self.min_gain,
            'n_trees': self.n_trees,
            'learning_rate': self.learning_rate,
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
            node.left = dict_to_node(d['left'])
            node.right = dict_to_node(d['right'])
            return node

        with open(nom, 'r', encoding='utf-8') as f:
            data = json.load(f)
        model = cls(profondeur_max=data.get('profondeur_max', 10),
                    min_gain=data.get('min_gain', 1e-5),
                    n_trees=data.get('n_trees', 2),
                    learning_rate=data.get('learning_rate', 0.5))
        model.init = data.get('init', None)
        model.forest = [dict_to_node(t) for t in data.get('forest', [])]
        return model