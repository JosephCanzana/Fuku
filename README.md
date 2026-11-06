# Fuku: spaced-repetition flashcard web app

#### Video Demo: <URL HERE>

#### Description:
**Fuku** is a spaced-repetition flashcard app that uses the SM-2 algorithm.

## Why I built it
TODO

## How to run it
## How to run it

### Requirements
- [Docker](https://docs.docker.com/get-docker/) with Docker Compose
- Git

### Development

1. Clone the repository and enter it:
   ```bash
   git clone <repo-url>
   cd fuku
   ```

2. Create your environment file and edit the values:
   ```bash
   cp .env.example .env
   ```
   Replace the placeholder values in `.env` (at least `SECRET_KEY` and the database password).

3. Download the Tailwind CLI. Pick the file for your system (`macos-arm64`, `macos-x64`, `linux-x64`, or `windows-x64.exe`):
   ```bash
   mkdir -p theme
   curl -sL -o theme/tailwindcss \
     https://github.com/tailwindlabs/tailwindcss/releases/download/v4.3.0/tailwindcss-<your-system>
   chmod +x theme/tailwindcss
   ```

4. Start the containers:
   ```bash
   docker compose up --build
   ```

5. In a second terminal, set up the database and create an admin account:
   ```bash
   docker compose exec web uv run python manage.py migrate
   docker compose exec web uv run python manage.py createsuperuser
   ```

6. Build the CSS (use `--watch` instead of a single build while developing):
   ```bash
   ./theme/tailwindcss -i static/css/input.css -o static/css/output.css --watch
   ```

Then open http://127.0.0.1:8000.

To stop the app, press `Ctrl+C`, or run `docker compose down`. Add `-v` to also delete the database data.

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