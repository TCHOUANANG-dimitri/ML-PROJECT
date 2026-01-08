import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt


df = pd.read_excel("jeu_données_étudiants.xlsx")
features = [
        "Age",
        "Moyenne_annuelle",
        "Nb_heures_presence",
        "ratio_heure",
        "Nb_matieres_non_validees",
        "encodage_dist_dom"
    ]

X = df[features].values
y = df["Reussite"].values


    # -------------------------------
    # Normalisation (recommandée)
    # -------------------------------
X = (X - X.mean(axis=0)) / X.std(axis=0)

# 2. Division Train/Test (80% pour apprendre, 20% pour tester)
indices = np.arange(len(X)) # Crée un tableau d'indices de 0 à n-1, où n est le nombre d'échantillons.
np.random.shuffle(indices) # Mélange pour éviter les biais
split = int(0.8 * len(X))

X_train, X_test = X[indices[:split]], X[indices[split:]]
y_train, y_test = y[indices[:split]], y[indices[split:]]

# -------------------------------
    # Initialisation et entraînement
    # -------------------------------
model = RegressionLogistique(
        learning_rate=0.05,
        n_iterations=3000
    )

model.fit(X_train, y_train)

 # -------------------------------
    # Prédictions
    # -------------------------------
y_pred = model.predict(X_train)


    # -------------------------------
    # Évaluation simple (accuracy)
    # -------------------------------
accuracy = np.mean(y_pred == y)

# Sauvegarder en JSON
model.save_json('modele.json')

# Charger depuis JSON
model_charge = RegressionLogistique.load_json('modele.json')

# Faire des prédictions
predictions = model_charge.predict(X_test)

print("Accuracy du modèle :", accuracy)
print("\nParamètres appris (weights) :")
print(model.weights)
print("Prédiction :", y_train)
