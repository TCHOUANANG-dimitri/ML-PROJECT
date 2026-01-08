import numpy as np 

class Node:
    def __init__(self):
        self.feature=None # index de feature utiliser pour le split
        self.threshold=None # valeur de seuil pour le split
        self.prediction=None # valeur de prediction
        self.left=None # noeud enfant a gauche
        self.right=None # noeud enfant a droite

class RandomForestRegressor: # Class foret aleatoire regressif
    def __init__(self,profondeur_max=10,min_gain=1e-5,n_trees=2): # constructeur: il permet d'initialiser les attributs (dans notre cas les hyperparametres d'une instance (objet)
        self.profondeur_max=profondeur_max
        self.min_gain=min_gain
        self.forest=[] # definition de la foret
        self.n_trees=n_trees # nombres d'arbres de la foret
        
    # Fonction permettant l'entrainement du modele en utilisant l'arbre construit dans la fonction plus bas. 
    # On construit ici un arbre a chaque iteration, puis on les stocke dans dans une liste d'arbres (foret)
    def fit(self,X,y): 
        for i in range(self.n_trees):
           self.forest.append(self.build_tree(X,y))
           
    
    def build_tree(self,X,y,seuil_min_gain=1e-5,profondeur_max=10,profondeur=0):
        n_samples = len(X)
        bootstrap_idx = np.random.choice(n_samples, size=n_samples, replace=True)
        X_bootstrap = X[bootstrap_idx]
        y_bootstrap = y[bootstrap_idx]      # creation de l'echantillon bootstrap
        
        node=Node() # creation du noeud racine
        node.prediction=np.mean(y_bootstrap) # initialisation de la prediction/racine (moyenne de la target)
        variance_parent=np.var(y_bootstrap) # initialisation de la variance de la racine (variance de la target)
        meilleur_gain=0
        meilleur_feature=None
        meilleur_seuil=None
    
        # critere d'arret
        if profondeur>=profondeur_max or len(y_bootstrap)<=1 or variance_parent==0:
            return node
        n_features = np.random.choice(
        X_bootstrap.shape[1],
        size=int(np.sqrt(X_bootstrap.shape[1])),  # règle classique
        replace=False
        )
        # selection aleatoire des features.
        # parcour tous les features pour rechercher le celui qui permet d'avoir le meilleur gain d'informations
        # ainsi la valeur de seuil de split (decoupage)
        for j in n_features:   # parcours de chaque feature
            valeurs_uniques=np.unique(X_bootstrap[:,j])
            for seuil in valeurs_uniques: # decoupage en split (deux sous groupes)
                gauche_idx=X_bootstrap[:,j]<=seuil
                droite_idx=X_bootstrap[:,j]>seuil
                if np.sum(gauche_idx)==0 or np.sum(droite_idx)==0:
                    continue
                y_gauche=y_bootstrap[gauche_idx]
                y_droite=y_bootstrap[droite_idx] 
                # calcul du gain d'informations
                erreur_apres=(len(y_gauche)/len(y_bootstrap))*np.var(y_gauche)+(len(y_droite)/len(y_bootstrap))*np.var(y_droite) # moyenne ponderer des varinces des splits
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
        gauche_idx=X_bootstrap[:,node.feature]<=node.threshold
        droite_idx=X_bootstrap[:,node.feature]>node.threshold
        node.left=self.build_tree(X_bootstrap[gauche_idx],y_bootstrap[gauche_idx],seuil_min_gain,profondeur_max,profondeur+1)
        node.right=self.build_tree(X_bootstrap[droite_idx],y_bootstrap[droite_idx],seuil_min_gain,profondeur_max,profondeur+1)
        return node

    def predict_one(self,node,x): # effectue une prediction pour une seule instance ( un vecteur en entrer , unscalaire en sortie)
        if node.left is None and node.right is None:
            return node.prediction
        if x[node.feature]<=node.threshold:
            return self.predict_one(node.left,x)
        else:
            return self.predict_one(node.right,x)
            
    def predict_tree(self,root,X): # effectue une prediction pour plusieurs vecteurs (plusieurs vecteurs en entrez un vecteur de valeurs predite en sortie
        return np.array([self.predict_one(root,x) for x in X])
    
    def predict(self,X):
        preds=[]
        for root in self.forest:
            preds.append(self.predict_tree(root,X))
        return np.mean(preds,axis=0)

    def score(self,X,y): # Calcul du coefficient de determination
        y_pred=self.predict(X)
        return 1-(np.sum((y-y_pred)**2)/np.sum((y-np.mean(y))**2))
    def save(self,nom):
        joblib.dump(self,nom)
        print("Modele sauvegarder")
        
    @classmethod
    def load(self,nom):
        model=joblib.load(nom)
        print("Modele charger")
        return model
    
