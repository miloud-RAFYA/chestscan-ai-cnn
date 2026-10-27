# ChestScan AI — Classification de radiographies thoraciques

## 1. Présentation

**ChestScan AI** est un projet de Deep Learning consacré à la classification d'images de radiographies thoraciques en deux catégories :

- `NORMAL` : image classée comme normale.
- `PNEUMONIA` : image classée dans la catégorie associée à la pneumonie.

Le projet explore les réseaux de neurones convolutifs (CNN) et le Transfer Learning avec MobileNetV2. Il comprend également une API REST développée avec FastAPI et une interface utilisateur réalisée avec Streamlit.

> **Avertissement :** ce projet est destiné à l'apprentissage et à l'expérimentation. Les prédictions ne constituent pas un diagnostic médical.

## 2. Objectifs

- Préparer et explorer un dataset de radiographies thoraciques.
- Développer et entraîner un CNN.
- Expérimenter le Transfer Learning et le fine-tuning avec MobileNetV2.
- Comparer les performances de plusieurs modèles.
- Évaluer les résultats avec des métriques de classification.
- Déployer une interface de prédiction avec FastAPI et Streamlit.
- Conteneuriser l'application avec Docker Compose.

## 3. Technologies

- Python
- TensorFlow / Keras
- CNN et MobileNetV2
- NumPy, Pandas et Matplotlib
- Scikit-learn
- FastAPI
- Streamlit
- Docker et Docker Compose
- Jupyter Notebook

## 4. Dataset

Le projet utilise le dataset public *Chest X-Ray Images (Pneumonia)* disponible sur Kaggle.

Source : https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia

Les images sont réparties en deux classes : `NORMAL` et `PNEUMONIA`.

## 5. Architecture du projet

```text
chestscan-ai-cnn/
├── app/
│   └── streamlit_app.py
├── src/
│   ├── api/
│   │   └── main.py
│   ├── data/
│   ├── evaluation/
│   ├── inference/
│   └── models/
├── artifacts/
│   ├── models/
│   └── reports/
├── notebooks/
├── configs/
├── data/
├── scripts/
├── tests/
├── test_model.py
├── requirements.txt
├── requirements-train.txt
├── Dockerfile
├── compose.yaml
└── README.md
```

### Rôle des dossiers

| Dossier | Responsabilité |
|---|---|
| `app/` | Interface utilisateur Streamlit |
| `src/api/` | API FastAPI |
| `src/data/` | Chargement et préparation des données |
| `src/models/` | Code lié aux modèles |
| `src/inference/` | Prédiction sur de nouvelles images |
| `src/evaluation/` | Évaluation et métriques |
| `artifacts/models/` | Modèles entraînés |
| `artifacts/reports/` | Rapports et visualisations |
| `notebooks/` | Exploration et expérimentation |
| `configs/` | Paramètres de configuration |
| `scripts/` | Scripts exécutables |
| `data/` | Données du projet |
| `tests/` | Tests automatisés |

Certains dossiers sont actuellement réservés aux développements futurs.

## 6. Modèles

### CNN personnalisé

Un réseau de neurones convolutif entraîné pour apprendre les caractéristiques visuelles des radiographies thoraciques.

### MobileNetV2

Une architecture préentraînée utilisée pour le Transfer Learning et le fine-tuning sur le dataset du projet.

Les modèles entraînés sont sauvegardés dans `artifacts/models/`.

## 7. Évaluation

Les modèles sont étudiés à l'aide des métriques suivantes :

- Accuracy
- Precision
- Recall (sensibilité)
- F1-score
- Specificity (spécificité)
- ROC-AUC
- Matrice de confusion

Les résultats définitifs seront documentés après vérification des performances sur les ensembles de validation et de test.

## 8. Installation et exécution

### Prérequis

- Python
- pip
- Docker Desktop et Docker Compose, pour l'exécution conteneurisée

### Installation locale

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances de l'application :

```bash
pip install -r requirements.txt
```

Lancer l'interface Streamlit :

```bash
streamlit run app/streamlit_app.py
```

**Remarque :** si Streamlit dépend de l'API FastAPI, démarrer également l'API et configurer son URL conformément au code de l'application.

### Exécution avec Docker Compose

Depuis la racine du projet :

```bash
docker compose up --build
```

Pour arrêter les services :

```bash
docker compose down
```

Les ports et les services disponibles dépendent de `compose.yaml`.

## 9. Dépendances

- `requirements.txt` : dépendances nécessaires à l'application.
- `requirements-train.txt` : dépendances nécessaires à l'entraînement et aux expérimentations.

## 10. Limites et améliorations futures

- Analyser les faux positifs sur les images `NORMAL`.
- Vérifier la cohérence des résultats entre validation et test.
- Améliorer la robustesse du modèle.
- Ajouter des tests automatisés.
- Générer des rapports d'évaluation reproductibles.
- Compléter la documentation des expériences et des résultats.

## 11. Avertissement médical

ChestScan AI est un prototype éducatif. Il n'est pas validé pour un usage clinique et ne doit pas remplacer l'avis d'un professionnel de santé.

---

**Projet de Deep Learning — Computer Vision**
