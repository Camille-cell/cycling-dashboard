# Cycling Globalisation

Projet d'analyse de la globalisation du cyclisme à partir des classements
ProCyclingStats, avec agrégation des points par pays et visualisation Dash.

## Organisation

- `src/cycling_globalisation/ingestion.py` collecte les classements bruts.
- `src/cycling_globalisation/processing.py` agrège les points par pays et par année.
- `src/cycling_globalisation/dashboard.py` lance le tableau de bord interactif.
- `data/raw/` contient les données sources, y compris les anciens exports conservés.
- `data/processed/` contient les données agrégées utilisées par le tableau de bord.
- `assets/reference/` contient les pages HTML sauvegardées et leurs ressources.
- `archive/legacy/` conserve les scripts et copies de code historiques.

## Installation

Depuis la racine du projet, crée et active un environnement virtuel, puis installe
les dépendances :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Utilisation

Depuis la racine du projet, active l'environnement virtuel :

```powershell
.\.venv\Scripts\Activate.ps1
```

### Préparer les données (facultatif)

Les fichiers traités sont déjà présents dans `data/processed/yearly/`. Si tu
souhaites les régénérer à partir des classements locaux, exécute :

```powershell
python src\cycling_globalisation\processing.py
```

### Lancer le dashboard

Dans le terminal, à la racine du projet et avec l'environnement virtuel activé,
lancer :

```powershell
python src\cycling_globalisation\dashboard.py
```
.

### Télécharger de nouvelles données

Pour récupérer à nouveau les classements depuis ProCyclingStats, lance la
collecte séparément :

```powershell
python src\cycling_globalisation\ingestion.py
```

La collecte dépend de la disponibilité du site et de ses conditions d'accès. Elle
remplace `data/raw/cycling_rankings_by_year.csv`. Après une nouvelle collecte,
régénère les données traitées avant de relancer le dashboard.
