# Cycling Globalisation

Projet d'analyse de la mondialisation du cyclisme à partir des résultats des coureurs trouvés sur le site ProCyclingStats. Le calcul est basé sur les points UCI agrégé par pays et une visualisation Dash.

## Organisation

- `src/cycling_globalisation/ingestion.py` collecte les classements bruts.
- `src/cycling_globalisation/processing.py` agrège les points par pays et par année.
- `src/cycling_globalisation/dashboard.py` lance le tableau de bord interactif.
- `data/raw/` contient les données sources, y compris les anciens exports conservés.
- `data/processed/` contient les données agrégées utilisées par le tableau de bord.
- `assets/reference/` contient les pages HTML sauvegardées et leurs ressources.
- `archive/legacy/` conserve les scripts et copies de code historiques.

## Installation

Depuis la racine du projet, créez et activez un environnement virtuel, puis installez
les dépendances :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Utilisation

Depuis la racine du projet, activez l'environnement virtuel :

```powershell
.\.venv\Scripts\Activate.ps1
```

```

### Lancer le dashboard

Dans le terminal, à la racine du projet et avec l'environnement virtuel activé,
lancer :

```powershell
python src\cycling_globalisation\dashboard.py
```
.

