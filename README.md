### Prérequis

* Poetry ([Installation](https://python-poetry.org/docs))

### Installation

1. Cloner le repo
```shell
git clone git@github.com:Arys02/DeepWoke-SpeechModeration.git deepwoke
cd deepwoke
```
2. Installer les dépendances
```shell
poetry install
```

### Structure de Répertoire de Haut Niveau

```
projet-hate-speech/
├── data/
├── models/
├── notebooks/
├── src/
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

### Description des Dossiers et Fichiers

- **`data/`**: Ce dossier contient les ensembles de données utilisés dans le projet. Il peut être subdivisé en sous-dossiers pour séparer les données brutes des données transformées ou prétraitées.

  ```
  data/
  ├── raw/         # Données brutes non modifiées
  ├── processed/   # Données nettoyées et prétraitées
  └── external/    # Données provenant de sources externes
  ```

- **`models/`**: Stockez ici les modèles entraînés, y compris leurs poids et éventuellement leurs configurations. Cela permet de réutiliser facilement les modèles sans avoir à les réentraîner.

- **`notebooks/`**: Jupyter Notebooks ou autres notebooks pour l'exploration de données, le prototypage de modèles, et les analyses. Nommez chaque notebook de manière à refléter son usage ou son contenu (par exemple, `exploration_des_données.ipynb`, `entraînement_du_modèle.ipynb`).

- **`src/`**: Code source du projet. Ce répertoire contient les scripts et les modules Python qui composent le cœur du projet. Il peut être structuré plus en détail selon les besoins du projet.

  ```
  src/
  ├── data         # Scripts pour le chargement et la préparation des données
  ├── features     # Scripts pour la construction et la sélection des caractéristiques
  ├── models       # Définitions des modèles de machine learning/deep learning
  └── visualization # Scripts pour la visualisation des données et des résultats
  ```

- **`tests/`**: Tests unitaires et d'intégration pour vérifier la fiabilité de votre code. Utilisez un framework de test comme pytest pour organiser vos tests.

- **`docs/`**: Documentation du projet, y compris l'installation, l'utilisation, et la description de l'API pour les utilisateurs ou les développeurs qui souhaitent utiliser ou contribuer au projet.

- **`requirements.txt`**: Liste de toutes les dépendances Python nécessaires pour le projet. Permet une installation facile de l'environnement à l'aide de `pip install -r requirements.txt`.

- **`README.md`**: Un fichier Markdown décrivant le projet, comment l'installer, l'utiliser, et contribuer à celui-ci. Incluez également des informations sur l'objectif du projet, la manière d'exécuter les scripts, et toute autre information pertinente pour les utilisateurs ou les contributeurs.

### Bonnes Pratiques

- **Nommez clairement** les fichiers et dossiers pour refléter leur contenu ou fonction.
- **Versionnez les données** si possible, surtout dans les cas où elles sont sujettes à des changements ou des mises à jour fréquentes.
- **Incluez un `.gitignore`** pour exclure les fichiers non nécessaires ou sensibles (comme les données volumineuses, les fichiers temporaires, les environnements virtuels).
- **Documentez** le but et l'utilisation de chaque script et notebook pour faciliter la compréhension et la maintenance par d'autres développeurs.

Cette structure de projet est suffisamment flexible pour être adaptée à la plupart des projets de deep learning et aide à maintenir le code organisé et accessible.