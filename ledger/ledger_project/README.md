# The Ledger — Django edition

A news site with photo galleries, in-story links and embedded video, built
in Django. An administrator can create author accounts (with a photo), and
authors can publish stories with as many photos as the story needs.

## What's included

- **Two roles**: Administrator and Author, backed by Django's built-in
  `User` model plus a `Profile` model (role, bio, photo).
- **Eight sections**: News, Economy, Technology, Environment, Education,
  Blogs, Sports and Updates — used by the masthead nav, the sidebar and the
  `?category=` filter on the front page.
- **Admin dashboard** (`/accounts/dashboard/`): create author accounts
  (name, username, password, photo, bio), remove accounts, feature, edit or
  delete any story.
- **Author dashboard** (`/dashboard/`): publish stories with a headline,
  section, one-line summary, body text and photos; edit or delete your own
  stories afterwards.
- **Photo galleries**: a story carries as many photos as it needs. One is the
  **spotlight image** — it leads the story on the front page and at the top
  of the story; the rest appear in a gallery underneath, each with an
  optional caption. The spotlight is chosen from thumbnails while writing,
  and can be changed at any time from the edit page.
- **Links inside the story**: paste a web address anywhere and it becomes a
  link, or write `[words to link](https://example.com)` to link a phrase.
- **Embedded YouTube video**: a YouTube address on a line of its own plays
  on the page; `[Caption](https://youtu.be/…)` captions the player.
- **Per-story switches** to turn clickable links and video players off, so
  an author can show plain addresses instead.
- **Clickable story cards**: the photo, the headline and the summary all
  open the story — not just the headline.
- Django's own `/admin/` is also available and fully wired up (useful for
  bulk edits or promoting a user to administrator).

## Writing a story

Everything an author needs is on the author dashboard.

| To do this | Write this in the story box |
| --- | --- |
| Link an address | `https://example.com/report` |
| Link a phrase | `[the full report](https://example.com/report)` |
| Play a video | a YouTube address on a line of its own |
| Caption a video | `[Site tour](https://youtu.be/VIDEO_ID)` |

Story text is escaped before anything is linked, and only `http`, `https`
and `mailto` addresses ever become links — pasting markup or a
`javascript:` address is safe.

Photos are picked with a single file chooser (select several at once).
Thumbnails appear underneath with a radio button on each: the one you pick
is the spotlight image. Adding more photos, captioning them, changing the
spotlight or removing one is all done from **Edit** on the dashboard.

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

## Upgrading an existing copy

`python manage.py migrate` does the whole move:

- the five old business sections are folded into the new eight (Business,
  Markets and Money become **Economy**; Leadership becomes **Blogs**);
- each story's single cover photo becomes its spotlight photo in the new
  gallery, so no image is lost.

## Tests

```bash
python manage.py test news
```

Covers link and video rendering (including the escaping rules and the two
per-story switches), spotlight-photo selection, publishing with several
photos at once, and the edit page.

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
