import numpy as np
import json

class RandomForestClassification :

    def __init__ (self,nb_arbre = 100, profondeur_max=10, nb_ex_feuilles_min=2 ) :

        self.nb_arbre = nb_arbre        # Nombre d'arbre dans la forêt
        self.profondeur_max = profondeur_max          # Attributs de l'arbre de decision
        self.nb_ex_feuilles_min = nb_ex_feuilles_min        # Nombre d'exemple par feuille minimum: nbre minimum d'instances qui doit arriver jusqu'a cette feuille
        self.forest = []
        

    def fit (self, X, y):

        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)

        for k in range (self.nb_arbre) :

            tree = None

            index_colonnes = np.random.choice(X.shape[1],size= (X.shape[1]//2)+1 ,replace= True)    # selectionne les colonnes au hazard
            index_lignes =  np.random.choice(X.shape[0],size= (X.shape[0]//2)+1 ,replace= True)     # selectionne les lignes au hazard avec remplacement (bootstrap)

            X_reduit = X[:,index_colonnes]           # recupere les colonnes choisi
            X_reduit = X_reduit[index_lignes,:]      # recupere les lignes choisi
            y_reduit = y[index_lignes]            # recupee les resultatas des instances choisi

            tree = self.Arbre(X_reduit,y_reduit)
            self.forest.append(tree)

    def Arbre(self, X, y, profondeur=0):           # Construction de l'arbre
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)

        meilleur_gain = 0
        meilleur_feature = None
        meilleur_seuil = None
        nb_colonnes = X.shape[1]

        # Entropie du parent
        index_yes = y == 1       # Index le resultat positif
        index_no = y == 0        # Index le resultat négatif
        proba_parent_yes = np.sum(index_yes) / len(y)    # Probabilité d'un resultat positif
        proba_parent_no = np.sum(index_no) / len(y)      # Probabilité d'un resultat négatif
        
        # Gestion de l'entropie parent (éviter log(0))
        if proba_parent_yes == 0 or proba_parent_yes == 1:
            entropie_parent = 0
        else:
            entropie_parent = - proba_parent_yes * np.log2(proba_parent_yes) - proba_parent_no * np.log2(proba_parent_no)

        for feature in range(nb_colonnes):
            unique_X = np.unique(X[:, feature])
            
            for seuil in unique_X:
                index_gauche = X[:, feature] <= seuil
                index_droite = X[:, feature] > seuil
                
                # Vérifier qu'il y a des éléments des deux côtés
                if np.sum(index_gauche) == 0 or np.sum(index_droite) == 0:
                    continue

                # Entropie enfants
                y_gauche = y[index_gauche]     # target connaissant X <= seuil
                y_droite = y[index_droite]     # target connaissant X > seuil

                # Du coté gauche
                index_gauche_yes = y_gauche == 1      # index le resultat positif a gauche
                proba_gauche_yes = np.sum(index_gauche_yes) / len(y_gauche)      # probabilité d'un resultat positif a gauche 
                proba_gauche_no = 1 - proba_gauche_yes            # probabilité d'un resultat négatif a gauche
                
                if proba_gauche_yes == 0 or proba_gauche_yes == 1:   # pour eviter log2(0)
                    entropie_gauche = 0
                else:
                    entropie_gauche = - proba_gauche_yes * np.log2(proba_gauche_yes) - proba_gauche_no * np.log2(proba_gauche_no)

                # Du coté droite
                index_droite_yes = y_droite == 1        # index le resultat positif a drite
                proba_droite_yes = np.sum(index_droite_yes) / len(y_droite)         # probabilité d'un resultat positif a droite
                proba_droite_no = 1 - proba_droite_yes               # probabilité d'un resultat négatif a droite
                
                if proba_droite_yes == 0 or proba_droite_yes == 1:   # pour eviter log2(0)
                    entropie_droite = 0
                else:
                    entropie_droite = - proba_droite_yes * np.log2(proba_droite_yes) - proba_droite_no * np.log2(proba_droite_no)

                # Gain d'information
                gain = entropie_parent - (np.sum(index_gauche) / len(y)) * entropie_gauche - (np.sum(index_droite) / len(y)) * entropie_droite

                # Mise à jour des paramètres
                if gain > meilleur_gain:
                    meilleur_gain = gain
                    meilleur_feature = feature
                    meilleur_seuil = seuil

        # reinitialisation de l'arbre des arbre enfants
        arbre_gauche = None
        arbre_droite = None

        # Conditions de continuite : conditions à respecter pour poursuire la construction de l'arbre
        if (profondeur < self.profondeur_max and 
            meilleur_gain > 0 and 
            len(y) >= self.nb_ex_feuilles_min and 
            meilleur_feature is not None):
            
            index_gauche = X[:, meilleur_feature] <= meilleur_seuil
            index_droite = X[:, meilleur_feature] > meilleur_seuil

            arbre_gauche = self.Arbre(X[index_gauche], y[index_gauche], profondeur + 1)
            arbre_droite = self.Arbre(X[index_droite], y[index_droite], profondeur + 1)

        # Décision (classe majoritaire)
        index_yes = y == 1
        if np.sum(index_yes) / len(y) > 0.5:
            decision = 1
        else:
            decision = 0

        return {
            "feature": meilleur_feature,
            "seuil": meilleur_seuil,
            "decision": decision,
            "arbre enfant de gauche": arbre_gauche,
            "arbre enfant de droite": arbre_droite
        }

    def predict(self, X):

        X = np.array(X, dtype=float)     # changer X en tableau de reels
        predictions = np.array([])       
        for i in range(X.shape[0]):      # separé le tableau en plusieurs instances 
            x = X[i, :]
            predict_forest = np.array([]) 

            for j in range (self.nb_arbre) :    # fait une prediction d'une même instance sur chaque arbre
                predict_forest = np.append(predict_forest, self.predict_one_tree(x, self.forest[j]))     # prediction de tous les arbres
                
            # Décision de la foret
            index_yes = predict_forest == 1
            if np.sum(index_yes) / self.nb_arbre > 0.5:
                decision = 1
            else:
                decision = 0
            
            predictions = np.append(predictions,decision)

        return predictions
    
    def predict_one_tree(self, x, noeud):      # prediction d'une instance sur un arbre 
        # Si c'est une feuille, retourner la décision
        if noeud["arbre enfant de gauche"] is None and noeud["arbre enfant de droite"] is None:
            return noeud["decision"]
        
        # Sinon, naviguer dans l'arbre
        if x[noeud["feature"]] <= noeud["seuil"]:
            return self.predict_one_tree(x, noeud["arbre enfant de gauche"])
        else:
            return self.predict_one_tree(x, noeud["arbre enfant de droite"])

    def score(self, X, y):         # taux de prediction correct 
        y_predit = self.predict(X)
        index_bonne_prediction = y_predit == y
        accuracy = np.sum(index_bonne_prediction) / len(y)
        
        return accuracy


    def save(self, nom_fichier):
        """
        Sauvegarde le modèle dans un fichier JSON
        
        Args:
            nom_fichier: Chemin du fichier de sauvegarde (ex: 'modele.json')
        """
        if self.forest is None:
            raise ValueError("Aucun modèle à sauvegarder. Entraînez d'abord avec fit().")
        
        modele = {
            'forest': self.forest,
            'nb_arbre' : self.nb_arbre,
            'profondeur_max': self.profondeur_max,
            'nb_ex_feuilles_min': self.nb_ex_feuilles_min,
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
        
        self.forest = modele['forest']
        self.nb_arbre = modele['nb_arbre']
        self.profondeur_max = modele['profondeur_max']
        self.nb_ex_feuilles_min = modele['nb_ex_feuilles_min']
        
        print(f"✓ Modèle chargé depuis '{nom_fichier}'")
        
        return self



        