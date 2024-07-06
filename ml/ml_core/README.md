### Installation

1. Cloner le repo
```shell
git clone git@github.com:Arys02/DeepWoke-SpeechModeration.git deepwoke
cd deepwoke
```

### Structure de Répertoire de Haut Niveau

```
ml_core/
├── data/
├── notebooks/
├── embedded_vector/
├── model_weights/
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
  ├── raw/             # Données brutes non modifiées
  ├── embedding_data/  # Données d'embedder  
  ├── processed/       # Données nettoyées et prétraitées
  └── external/        # Données provenant de sources externes
  ```

- **`model_weights/`**: Les modèles entraînés, y compris leurs poids et éventuellement leurs configurations. Cela permet de réutiliser facilement les modèles sans avoir à les réentraîner.

- **`notebooks/`**: Jupyter Notebooks ou autres notebooks pour l'exploration de données, le prototypage de modèles, et les analyses. 
 ```
  notebooks/
  ├── data/         # Notebook lié à l'affichage/modifications des dataset 
  ├── embedding/   # Notebook contenant les algorithme pour sauvegarder les vecteur d'entrainement à partir des différents model d'embedding 
  ├── model/       # Notebook lié au entrainement des différents models
  ```

- **`src/`**: Code source du projet. Ce répertoire contient les scripts et les modules Python qui composent le cœur du projet. Il peut être structuré plus en détail selon les besoins du projet.

  ```
  src/
  ├── core         # Fonctions pour génerer les structure de models 
  ├── data         # Scripts pour la récuperations de datas (notamment sur twitter) 
  ├── embedding    # Scripts pour télécharger les différents model d'embedding 
  ```

- **`tests/`**: Différents notebook de teste 

- **`docs/`**: Documentation du projet.

- **`README.md`**: Un fichier Markdown décrivant le projet, comment l'installer, l'utiliser, et contribuer à celui-ci. Incluez également des informations sur l'objectif du projet, la manière d'exécuter les scripts, et toute autre information pertinente pour les utilisateurs ou les contributeurs.