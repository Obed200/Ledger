# The Ledger — Django edition

A business/markets news site with image uploads, built in Django. An
administrator can create author accounts (with a photo), and authors can
publish stories with their own photos attached.

## What's included

- **Two roles**: Administrator and Author, backed by Django's built-in
  `User` model plus a `Profile` model (role, bio, photo).
- **Admin dashboard** (`/accounts/dashboard/`): create author accounts
  (name, username, password, photo, bio), remove accounts, feature or
  delete any story.
- **Author dashboard** (`/dashboard/`): publish stories with a headline,
  category, one-line summary, photo, and body text; manage your own stories.
- **Image uploads** for both author photos and article photos, handled with
  Pillow and Django's `ImageField` — this is the piece the earlier
  HTML-only mockup couldn't do.
- Django's own `/admin/` is also available and fully wired up (useful for
  bulk edits or promoting a user to administrator).

## Setup

```bash
python -m venv venv
source venv/bin/activate          # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser  # creates your first administrator
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

### Optional: load demo content

To see the site populated right away (a demo admin, a demo author, and a
few sample stories), run:

```bash
python manage.py seed_demo
```

This creates:
- Administrator — username `admin`, password `admin12345`
- Author — username `jkim`, password `author12345`

**Change or remove these before deploying anywhere public.**

## How account creation works

1. Sign in as an administrator at `/accounts/login/`.
2. Go to the **Admin dashboard** and fill in the "Create an author account"
   form — name, username, password, an optional photo, and a short bio.
3. Give those credentials to the author. They sign in at the same
   `/accounts/login/` page and land on their own **Author dashboard**,
   where they can publish stories under their byline.

Administrators can remove any author account from the same dashboard
(their published stories stay live, just kept under their original byline).

## Notes for going to production

This is set up for local development (`DEBUG = True`, SQLite, images
served by Django itself). Before deploying anywhere public:

- Set a real `SECRET_KEY` via an environment variable, set `DEBUG = False`,
  and fill in `ALLOWED_HOSTS`.
- Move to Postgres (or another production database).
- Serve uploaded images from cloud storage (e.g. S3 via `django-storages`)
  rather than the local `media/` folder — most hosts don't persist local
  disk writes across deploys.
- Put Django behind a real web server (gunicorn/uwsgi + nginx, or a PaaS).
- Run `python manage.py collectstatic` and serve static files properly
  (e.g. WhiteNoise or a CDN).
