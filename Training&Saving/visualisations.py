import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from regression_logistique import RegressionLogistique, roc_curve_from_scratch

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

# Normalisation
X = (X - X.mean(axis=0)) / X.std(axis=0)

# Division Train/Test
indices = np.arange(len(X))
np.random.shuffle(indices)
split = int(0.8 * len(X))

X_train, X_test = X[indices[:split]], X[indices[split:]]
y_train, y_test = y[indices[:split]], y[indices[split:]]

# Entraînement
model = RegressionLogistique(learning_rate=0.05, n_iterations=3000)
print('Entraînement du modèle...')
model.fit(X_train, y_train)

# Prédictions
y_pred_test = model.predict(X_test)
accuracy_test = np.mean(y_pred_test == y_test.reshape(-1, 1))
print(f'Accuracy sur le test : {accuracy_test:.4f}')

# -------------------------------
# Visualisation 1 : Courbe de coût
# -------------------------------
print('\\n📊 Génération des visualisations...')
model.plot_cost()

# -------------------------------
# Visualisation 2 : Comparaison Vrai vs Prédit
# -------------------------------
plt.figure(figsize=(10, 5))
plt.plot(y_test[:50], label='Vrai y', marker='o', linestyle='-', markersize=6)
plt.plot(y_pred_test[:50].flatten(), label='Prédit', marker='x', linestyle='--', markersize=6)
plt.xlabel('Échantillons')
plt.ylabel('Classe')
plt.title('Comparaison Vrai vs Prédit (50 premiers échantillons du test)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------------
# Visualisation 3 : Distribution des probabilités
# -------------------------------
model.plot_probabilities(X_test, y_test)

# -------------------------------
# Visualisation 4 : Courbe ROC
# -------------------------------
y_scores = model.predict_proba(X_test).flatten()
FPR, TPR = roc_curve_from_scratch(y_test, y_scores, n_thresholds=100)

# Calcul de l'AUC (approximation)
auc = np.trapz(TPR, FPR)

plt.figure(figsize=(7, 7))
plt.plot(FPR, TPR, label=f'ROC curve (AUC = {auc:.3f})', linewidth=2)
plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Modèle aléatoire')
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('Courbe ROC (from scratch)')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------------
# Matrice de confusion manuelle
# -------------------------------
y_test_flat = y_test.reshape(-1, 1)
TP = np.sum((y_pred_test == 1) & (y_test_flat == 1))
TN = np.sum((y_pred_test == 0) & (y_test_flat == 0))
FP = np.sum((y_pred_test == 1) & (y_test_flat == 0))
FN = np.sum((y_pred_test == 0) & (y_test_flat == 1))

print('\\n📋 Matrice de confusion:')
print(f'TP (Vrais Positifs)  : {TP}')
print(f'TN (Vrais Négatifs)  : {TN}')
print(f'FP (Faux Positifs)   : {FP}')
print(f'FN (Faux Négatifs)   : {FN}')

# Métriques
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print(f'\\n📈 Métriques:')
print(f'Précision : {precision:.4f}')
print(f'Recall    : {recall:.4f}')
print(f'F1-Score  : {f1_score:.4f}')
print(f'Accuracy  : {accuracy_test:.4f}')

print('\\n✅ Toutes les visualisations ont été générées!')
