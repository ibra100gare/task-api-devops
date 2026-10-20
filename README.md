# Task API — projet d'apprentissage DevOps

Petite API REST FastAPI pour pratiquer Git/GitHub, les tests, GitHub Actions,
Docker, Docker Hub et le déploiement.

## Endpoints

| Méthode | Route | Fonction |
|---|---|---|
| GET | `/` | Message d'accueil |
| GET | `/health` | Vérification de santé |
| GET | `/tasks` | Lister les tâches |
| POST | `/tasks` | Créer une tâche |
| GET | `/tasks/{task_id}` | Lire une tâche |
| PATCH | `/tasks/{task_id}/complete` | Marquer une tâche terminée |
| DELETE | `/tasks/{task_id}` | Supprimer une tâche |
| GET | `/docs` | Documentation Swagger interactive |

> Pour garder le projet simple, les données sont en mémoire et disparaissent
> au redémarrage. Une amélioration ultérieure consistera à ajouter PostgreSQL.

## Lancer en local

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell : .venv\Scripts\Activate.ps1

pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Ouvrir http://127.0.0.1:8000/docs

## Lancer les tests

```bash
pytest -q
ruff check app tests
```

## Construire et exécuter Docker

```bash
docker build -t task-api:local .
docker run --rm -p 8000:8000 task-api:local
```

Puis ouvrir http://localhost:8000/docs

## Pipeline CI

Le workflow `.github/workflows/ci.yml` lance Ruff et pytest à chaque push sur
`main` et à chaque Pull Request vers `main`. Il construit aussi l'image Docker
si les tests passent.

## Publication Docker Hub (étape facultative)

1. Créer un dépôt Docker Hub nommé `task-api`.
2. Dans GitHub > Settings > Secrets and variables > Actions, ajouter :
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN` (un access token Docker Hub, pas le mot de passe).
3. Renommer `.github/workflows/publish.yml.example` en `publish.yml`.
4. Créer un tag et le pousser :

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Hébergement gratuit

Pour un exercice, Render propose des Web Services gratuits. Ils s'endorment après
15 minutes sans trafic, le premier appel peut donc être lent. Le système de fichiers
est éphémère : ne pas utiliser le stockage en mémoire de cette API pour des données
à conserver. Voir https://render.com/docs/free

Sur Render, créer un **Web Service** depuis le dépôt GitHub, choisir l'offre Free,
et utiliser la commande de démarrage :

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Le Dockerfile accepte aussi la variable `PORT`, ce qui permet un déploiement basé
sur l'image si la plateforme le permet avec le plan choisi.

## Étapes d'évolution

1. Ajouter une base PostgreSQL.
2. Ajouter un endpoint de mise à jour de tâche.
3. Ajouter un scan de dépendances et une analyse de sécurité de l'image.
4. Ajouter un déploiement continu après publication de l'image.
5. Ajouter des logs structurés et de la supervision.
