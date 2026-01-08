import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from regression_logistique import RegressionLogistique

# Chargement des données
df = pd.read_excel('../Datasets/jeu_données_étudiants.xlsx')

features = [
    'Age',
    'Moyenne_annuelle',
    'Nb_heures_presence',
    'ratio_heure',
    'Nb_matieres_non_validees',
    'encodage_dist_dom'
]

X = df[features].values
y = df['Reussite'].values

# -------------------------------
# Normalisation (recommandée)
# -------------------------------
X = (X - X.mean(axis=0)) / X.std(axis=0)

# 2. Division Train/Test (80% pour apprendre, 20% pour tester)
indices = np.arange(len(X))
np.random.shuffle(indices)
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

print('Entraînement du modèle en cours...')
model.fit(X_train, y_train)
print('Entraînement terminé!')

# -------------------------------
# Prédictions
# -------------------------------
y_pred = model.predict(X_train)

# -------------------------------
# Évaluation simple (accuracy)
# -------------------------------
accuracy = np.mean(y_pred == y_train.reshape(-1, 1))

# Sauvegarder en JSON
model.save_json('../Models/modele.json')

# Charger depuis JSON
model_charge = RegressionLogistique.load_json('../Models/modele.json')

# Faire des prédictions
predictions = model_charge.predict(X_test)

print('Accuracy du modèle :', accuracy)
print('Paramètres appris (weights) :')
print(model.weights.flatten())
print('Prédictions (10 premières) :', y_pred[:10].flatten())
print('Vraies valeurs (10 premières) :', y_train[:10])

# Visualisation
model.plot_cost()
