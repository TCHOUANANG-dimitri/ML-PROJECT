import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt



# ============================================
#  ENTRAÎNEMENT DU MODÈLE
# ============================================



df = pd.read_excel("jeu_données_étudiants.xlsx", engine="openpyxl")
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

# Créer et entraîner le modèle
model = RegressionLogistique(learning_rate=0.01, n_iterations=1000)
model.fit(X_train, y_train)

# Afficher la courbe de coût
model.plot_cost()

# Prédictions
# Pour le jeu d'entraînement
y_pred_train = model.predict(X_train)
# Pour le jeu de test
y_pred_test = model.predict(X_test)

# Afficher les métriques
afficher_metriques(y_test, y_pred_test, nom="Test")
afficher_metriques(y_train, y_pred_train, nom="Train")
# Accuracy sur l'entraînement
accuracy_train = np.mean(y_pred_train.flatten() == y_train.flatten())
print("Accuracy sur le train :", accuracy_train)

# Accuracy sur le test
accuracy_test = np.mean(y_pred_test.flatten() == y_test.flatten())
print("Accuracy sur le test :", accuracy_test)


# ============================================
#  VISUALISATIONS
# ============================================

# Comparaison Vrai vs Prédit (50 premiers)
plt.figure(figsize=(10,4))
plt.plot(y_test[:50], label="Vrai y", marker='o', linestyle='-', markersize=6)
plt.plot(y_pred[:50].flatten(), label="Prédit", marker='x', linestyle='--', markersize=6)
plt.legend()
plt.xlabel("Index")
plt.ylabel("Classe")
plt.title("Comparaison Vrai vs Prédit (50 premiers)")
plt.grid(True, alpha=0.3)
plt.show()

# Distribution des probabilités
model.plot_probabilities(X_test, y_test)

# Courbe ROC
y_scores1 = model.predict_proba(X_test).flatten()
y_scores2 = model.predict_proba(X_train).flatten()
FPR, TPR = roc_curve_from_scratch(y_test, y_scores1, n_thresholds=100)
FPR, TPR = roc_curve_from_scratch(y_train, y_scores2, n_thresholds=100)

# Calculer l'AUC (Area Under Curve) manuellement
auc = np.trapz(TPR, FPR)

plt.figure(figsize=(7,7))
plt.plot(FPR, TPR, label=f"ROC curve (AUC = {auc:.3f})", linewidth=2)
plt.plot([0,1], [0,1], linestyle="--", label="Modèle aléatoire", color='gray')
plt.xlabel("False Positive Rate (FPR)")
plt.ylabel("True Positive Rate (TPR)")
plt.title("Courbe ROC (from scratch)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


# ============================================
#  SAUVEGARDE DU MODÈLE
# ============================================

# Sauvegarder en JSON
model.save_json('modele_regression_logistique4.json')

# Charger le modèle (pour tester)
model_charge = RegressionLogistique.load_json('modele_regression_logistique4.json')
y_pred_charge = model_charge.predict(X_test)

print("\n✓ Test du modèle chargé:")
afficher_metriques(y_test, y_pred_charge)

