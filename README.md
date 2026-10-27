# socrates.es

> A personal space for philosophy, art, technology, and the ideas that connect
> them.

![socrates.es screenshot](docs/screenshot.png)

**socrates.es** is a Spanish-language philosophy and culture site built with
Django. It combines a personal journal with essays, a thesis archive, visual
art experiments, and interactive work inspired by classical philosophers.

## Features

- Publish and organize posts with categories, tags, related posts, images, and
  video.
- Rich-text editing and media uploads through Django admin and CKEditor.
- Search, pagination, post likes, and social-sharing counters.
- Public pages for the journal, thesis, biography, contact, and subscriptions.
- Interactive philosophy and art experiences, including augmented-reality
  content and philosopher quotes.
- SQLite for local development and configurable SMTP email support.

## Tech stack

- Python 3.10+
- Django 5.1
- SQLite
- CKEditor
- Sass and static assets

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/beovideskevin/socrates.es.git
cd socrates.es
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. At minimum, set a Django secret key:

```dotenv
SECRET_KEY=replace-with-a-long-random-value
```

The application also supports the following optional settings:

| Variable | Purpose |
| --- | --- |
| `EMAIL_HOST` | SMTP server hostname |
| `EMAIL_PORT` | SMTP server port (defaults to `587`) |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `EMAIL_USE_TLS` | Enable TLS (defaults to `True`) |
| `EMAIL_USE_SSL` | Enable SSL (defaults to `False`) |
| `TURNSTILE_SECRET` | Cloudflare Turnstile secret |
| `ADMIN_USER_NAME` | Name used for error notifications |
| `ADMIN_USER_EMAIL` | Address used for error notifications |
| `SEND_ERROR_EMAILS` | Enable error email notifications |

Keep `.env` out of version control; it is already included in `.gitignore`.

### 5. Prepare the database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. The administration area is
available at <http://127.0.0.1:8000/admin/>.

## Main routes

| Route | Description |
| --- | --- |
| `/` | Journal and latest posts |
| `/tesis` | Philosophy thesis |
| `/acerca` | About the author |
| `/contacto` | Contact form |
| `/buscar` | Search |
| `/arte` | Art section |
| `/ar` | Augmented-reality experience |
| `/aart` | Augmented-art experience |
| `/quotes/<slug>` | Philosopher quotes |
| `/admin/` | Content administration |

## Project layout

```text
.
├── manage.py              # Django command-line entry point
├── socrates/              # Project settings, URLs, ASGI, and WSGI
├── www/                   # Main application, models, views, templates, and assets
├── docs/                  # Documentation assets
├── requirements.txt       # Python dependencies
└── db.sqlite3             # Local database (created after migrations)
```

## Content management

Use the Django admin to create categories, tags, posts, comments, subscribers,
videos, and interactive artwork. Uploaded content is stored under the
configured media directory. For production deployments, configure a persistent
media backend and run:

```bash
python manage.py collectstatic
```

## License and attribution

The site’s original writing, photography, and video belong to the author unless
otherwise noted. Artwork reproduced on the site remains the property of its
respective creators.

Visit the live site at <https://www.socrates.es>.
