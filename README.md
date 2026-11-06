# Fuku: spaced-repetition flashcard web app

#### Video Demo: <URL HERE>

#### Description:
**Fuku** is a spaced-repetition flashcard app that uses the SM-2 algorithm.

## Why I built it
TODO

## How to run it

### Development
```bash
git clone <repo-url>
cd fuku
cp .env.example .env
# edit .env and replace the placeholder values
docker compose up --build
docker compose exec web uv run python manage.py migrate
```
Then open http://127.0.0.1:8000.

### Deployment
Not set up yet.

## Features
TODO

## How it's built
TODO

## Design decisions
TODO

## Challenges and future updates
TODO