# Fuku: spaced-repetition flashcard web app

#### Video Demo: <URL HERE>

#### Description:
**Fuku** is a spaced-repetition flashcard app that uses the SM-2 algorithm. You can write your own cards, import them from CSV, or generate them from your notes with AI, then review them on a schedule that shows each card right before you would forget it.

## Why I built it
I struggled with creating reviewers. I then found out that you can generate flashcards with AI, optimize the prompt to get good cards, and review them in a third-party app. That made me wonder what would happen if one app made this whole process frictionless. Fuku is that app: notes in, flashcards out, review in the same place.

## How to run it

### Requirements
- [Docker](https://docs.docker.com/get-docker/) with Docker Compose
- Git
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com) (only needed for AI generation)

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
   Replace the placeholder values in `.env` (at least `SECRET_KEY` and the database password). For AI generation, also set:
   ```
   GEMINI_API_KEY=your_key_here
   GEMINI_MODEL=gemini-3.5-flash
   ```
   Model names change often. If the model is retired, set another one from the Google AI Studio model list.

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

Then open http://127.0.0.1:8000. The Django admin is at `/admin/`.

To stop the app, press `Ctrl+C`, or run `docker compose down`. Add `-v` to also delete the database data.

### Deployment
Not set up yet.

## Features
- **SM-2 review:** each card has its own ease factor, interval and due date.
- **Learning state:** new cards pass through short steps (minutes) before they graduate to day-based reviews.
- **Decks and tags:** cards are organized per deck, and decks can have tags.
- **Your own cards:** add, edit and delete cards, with optional multiple-choice options.
- **AI generation:** paste notes and get flashcards, in either *general* or *exam* mode.
- **CSV import and export:** `question,answer,choices`, with choices separated by `;`.
- **Undo:** take back your last ratings, as in Anki.
- **Keyboard shortcuts** on the review screen, and adjustable text size.
- **Admin:** user management through Django's built-in admin.

## How it's built
Django, PostgreSQL, Tailwind CSS (standalone CLI), JavaScript, HTML, Docker, and the free Gemini API. Dependencies are managed with `uv` and settings are read with `python-decouple`.

### Project structure
- `apps/accounts/`: the custom user model, sign up and log in.
- `apps/decks/`
  - `models.py`: `Deck`, `Flashcard` (with the SM-2 fields, `state` and `step`) and `Tag`.
  - `views.py`: deck and card pages, the review flow, rating, undo, import, export and generation.
  - `forms.py`: the card form (which converts `a;b;c` to a list and back), the import form and the generation form.
  - `services.py`: the scheduling algorithm (`apply_review`) and the CSV parsing helpers. It knows nothing about HTTP, so it can be tested on its own.
  - `ai.py`: the prompt builder and the Gemini call, with retries and a fallback model.
- `apps/pages/`: the landing, dashboard and about pages.
- `templates/` and `static/`: HTML templates, icons, JavaScript and the Tailwind input and output CSS.
- `theme/`: the Tailwind CLI binary.

## Design decisions
- **Learning steps before review.** A new card goes through steps of 1, 6 and 10 minutes before its first day-based interval, instead of being scheduled in days right away. One success on a new card proves little, so the app checks it a few times first. Failing a graduated card (a lapse) sends it back to learning.
- **SM-2 for graduated cards.** The first intervals are fixed (1 day, then 6), and later ones multiply the previous interval by the ease factor. The ease factor is updated by the rating and never drops below 1.3.
- **The algorithm lives in `services.py`,** apart from the views, so it can be tested in the Django shell without any HTTP requests.
- **Session-based undo.** Before each rating, a snapshot of the card's old values is saved in the user's session, and undo restores the newest one. This is simpler than a database table and matches how Anki's undo only lasts for a session.
- **AI limits.** The app uses the free Gemini API, so generation is limited to 20 cards and 5,000 characters of text. The prompt tells the model to use only the notes, and every row of its output is validated by the same parser that handles CSV imports.
- **Two generation modes.** *General* mode makes recall cards, and *exam* mode keeps the original wording of quiz items, for when a teacher says previous quizzes will appear on the test.
- **Ownership checks everywhere.** Every view fetches decks and cards filtered by the logged-in user, so changing an id in a URL returns a 404.
- **This is an MVP,** built within a limited time frame.

## Challenges and future updates
The hardest parts were CSV import and export, because files must be parsed carefully (quoted cells, commas, line breaks and encodings), and the AI generation, because the prompt has to be good for the cards to come out accurate. Models also fail or get overloaded sometimes, so the app retries, falls back to another model, and shows a friendly message if all fail.

Planned next:
- A further design and UI update, with more themes and customization
- Forgot-password emails
- Direct import of presentations, docs, PDFs and text, converted into flashcards
- A docs and PDF reviewer
- Search and filters
- Making the app a progressive web app

## Author
Made by Joseph Canzana.