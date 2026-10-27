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

## Noon Commander

The project includes **Noon Commander**, a Textual terminal file manager
available as a Django management command. It lets you browse the project,
preview files, edit or run files, and perform common file operations from the
terminal.

Run it from the project root after activating the virtual environment:

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python manage.py noon .
```

You can open a specific folder by passing its path:

```powershell
python manage.py noon "C:\path\to\folder"
```

On macOS/Linux:

```bash
source .venv/bin/activate
python manage.py noon .
```

Use `--nano` to configure the commander to use Nano instead of Vim when
editing files:

```bash
python manage.py noon . --nano
```

To see all command options:

```bash
python manage.py help noon
```

![Noon Commander showing the project README](docs/noon-commander-readme.png)

The main keyboard shortcuts are:

| Key | Action |
| --- | --- |
| `F1` | Help |
| `F2` | New file |
| `F3` | View file |
| `F4` | Edit file |
| `F5` | Copy file |
| `F6` | Move file |
| `F7` | New directory |
| `F8` | Delete file |
| `F9` | Run file |
| `F10` | Quit |

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
