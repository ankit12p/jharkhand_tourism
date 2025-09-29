# Copilot Instructions for AI Coding Agents

## Project Overview
- This is a Django project with a modular structure:
  - `core/`: Project settings, URLs, and WSGI/ASGI entrypoints.
  - `tourism/`: Main Django app for tourism-related features, with models, views, admin, and templates.
- Templates are organized under `tourism/templates/tourism/` (e.g., `dashboard.html`, `index.html`).

## Key Patterns & Conventions
- **App Structure:**
  - Each Django app follows standard conventions: `models.py`, `views.py`, `admin.py`, `apps.py`, `migrations/`.
  - Templates are namespaced by app for clarity and Django's template loader.
- **Settings:**
  - Project-wide settings are in `core/settings.py`.
  - URLs are routed via `core/urls.py`.
- **Migrations:**
  - All database schema changes must be managed via Django migrations in `tourism/migrations/`.
- **Static & Media:**
  - Not explicitly present; if needed, follow Django conventions for static/media directories and settings.

## Developer Workflows
- **Run Development Server:**
  - `python manage.py runserver`
- **Apply Migrations:**
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- **Create Superuser:**
  - `python manage.py createsuperuser`
- **Test:**
  - `python manage.py test tourism`

## Integration & Dependencies
- Assumes standard Django dependencies; check `requirements.txt` if present (not found in this scan).
- No custom service boundaries or external API integrations detected in the scanned structure.

## Project-Specific Notes
- **Template Usage:**
  - Use `{% extends 'tourism/base.html' %}` for consistent layout in tourism templates.
- **App Registration:**
  - Register new apps in `core/settings.py` under `INSTALLED_APPS`.
- **URL Routing:**
  - Add new routes in `core/urls.py` or app-specific `urls.py` (not present, so add if needed).

## Examples
- To add a new model: edit `tourism/models.py`, run migrations, and register in `admin.py` if needed.
- To add a new template: place it in `tourism/templates/tourism/` and reference it in views.

---

_If you are unsure about a workflow or pattern, check the relevant file or ask for clarification. Update this file as the project evolves._
