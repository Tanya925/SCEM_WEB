# SCEM Website Project

This project contains the current SCEM public website, its administrator back office, and the Scopus synchronization flow that refreshes staff h-index data and publication records.

## 1. Current Project Scope

The codebase currently covers two main areas:

- `Website application`
  - Public pages for homepage, staff, research projects, publications, and ongoing-project details
  - Administrator pages for homepage content, staff records, research projects, and administrator credential updates
- `Scopus synchronization`
  - Automatic synchronization of staff h-index values
  - Automatic synchronization of publication records from Scopus / SciVal APIs

Features that are no longer part of this project:

- Playwright crawler automation
- Windows Task Scheduler `.bat` scripts
- Manual publication review workflows
- Manual publication management pages
- Separate staff or researcher login accounts

---

## 2. Key Files

- `app.py`
  - Flask entry point, startup configuration, database readiness checks, and blueprint registration
- `routes/`
  - Public routes, authentication routes, and administrator routes
- `services/public_service.py`
  - Public-page data assembly
- `services/admin_service.py`
  - Administrator form handling, uploads, and save/delete flows
- `services/auth_service.py`
  - Administrator login validation and credential updates
- `services/scopus_sync_service.py`
  - Scopus / SciVal API calls and synchronization logic
- `services/scopus_scheduler.py`
  - APScheduler startup and scheduled sync job wiring
- `database/`
  - SQLite helpers, schema-completion helpers, and query/update functions
- `templates/`
  - Jinja templates for public pages and administrator pages
- `static/`
  - CSS, JavaScript, images, audio, PDFs, and uploaded assets
- `schema.sql`
  - Base schema and seed content used when initializing an empty database
- `init_db/seed.py`
  - One-time and repeatable database initialization script for deployment
- `scem.db`
  - SQLite database file used by the application
- `.env`
  - Local environment settings such as `SECRET_KEY`, `ADMIN_USER`, `ADMIN_PASSWORD`, `SCOPUS_API_KEY`, `SCOPUS_SYNC_HOUR`, and `SCOPUS_SYNC_MINUTE`
- `Dockerfile`
  - Container build file for the website
- `docker-compose.yml`
  - Local container runtime configuration

---

## 3. Environment Setup

### 3.1 Install dependencies

```powershell
pip install -r requirements.txt
```

Main packages used by the project:

- `Flask`
- `Flask-APScheduler`
- `python-dotenv`
- `gunicorn`

### 3.2 Configure `.env`

Create a `.env` file in the project root:

```env
SECRET_KEY=replace_with_your_own_secret
ADMIN_USER=admin
ADMIN_PASSWORD=change_this_admin_password
SCOPUS_API_KEY=your_scopus_api_key_here
SCOPUS_SYNC_HOUR=2
SCOPUS_SYNC_MINUTE=0
```

Environment variables:

- `SECRET_KEY`
  - Required for Flask session signing
- `ADMIN_USER`
  - Deployment-time administrator username used by `init_db/seed.py`
- `ADMIN_PASSWORD`
  - Deployment-time administrator password used by `init_db/seed.py`
- `SCOPUS_API_KEY`
  - Required for Scopus / SciVal synchronization requests
- `SCOPUS_SYNC_HOUR`
  - Daily synchronization hour in `Asia/Bangkok`, from `0` to `23`
- `SCOPUS_SYNC_MINUTE`
  - Daily synchronization minute in `Asia/Bangkok`, from `0` to `59`

---

## 4. Running the Site

### 4.1 Initialize the database first

Before starting the website, run the seed script once:

```powershell
python init_db/seed.py
```

Current seed behavior:

- If `scem.db` does not exist, it creates the database from `schema.sql`
- It creates or updates the single administrator account from `.env`
- It attempts one Scopus synchronization pass

If you change `ADMIN_USER` or `ADMIN_PASSWORD` in `.env`, run `init_db/seed.py` again so the database account matches the new values.

### 4.2 Run locally

```powershell
python app.py
```

Default local URL:

```text
http://127.0.0.1:3000
```

Typical startup messages include database readiness and scheduler status. The exact wording may vary depending on whether the scheduler starts in the current process.

Important note:

- `app.py` does not create an empty database automatically
- If `scem.db` is missing or incomplete, start-up will stop and ask you to run `init_db/seed.py`

### 4.3 Run with Docker

Build the image:

```powershell
docker compose build
```

Start the container:

```powershell
docker compose up -d
```

Current container behavior:

- One `web` service is defined
- Port `3000` is exposed
- `.env` is loaded into the container
- `scem.db` is mounted
- `static/uploads` is mounted

The current container starts the app with:

```text
gunicorn --bind 0.0.0.0:3000 --workers 1 app:app
```

If application code, templates, or styles change, rebuild the image because the full project source is not bind-mounted into the container.

```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## 5. Site Structure

### 5.1 Public routes

- `/`
  - Homepage
- `/staff`
  - Staff and researcher directory
- `/research`
  - Research project listing
- `/publications`
  - Publications page
- `/project/<id>`
  - Detail page for one ongoing project
- `/api/publications`
  - JSON endpoint used by the publications frontend

### 5.2 Administrator routes

All administrator pages currently live under:

```text
/0630_SCEMadmin
```

Available administrator pages:

- `/0630_SCEMadmin/login`
  - Administrator login page
- `/0630_SCEMadmin/dashboard`
  - Main administrator dashboard
- `/0630_SCEMadmin/general-info`
  - Homepage text and activity-image management
- `/0630_SCEMadmin/staff`
  - Staff management
- `/0630_SCEMadmin/projects`
  - Research project management
- `/0630_SCEMadmin/passwords`
  - Administrator username and password settings

---

## 6. Administrator Account Behavior

The current system uses a single-administrator model.

Important notes:

- `init_db/seed.py` creates or updates the administrator account from `.env`
- `ADMIN_USER` and `ADMIN_PASSWORD` therefore act as the deployment-time source of truth
- The administrator password page updates the existing account credentials
- Changing credentials requires the current password
- The new username must remain unique
- The new password must be at least 8 characters long
- The new password must be different from the current password

Recommended usage:

- Set the initial administrator username and password in `.env`
- Run `init_db/seed.py`
- Log in through `/0630_SCEMadmin/login`
- After that, credentials can also be changed from `/0630_SCEMadmin/passwords`

Use this page to update administrator credentials:

- `/0630_SCEMadmin/passwords`

---

## 7. Scopus Synchronization

The current synchronization flow is:

1. Read each staff record that has a `scopus_author_id`
2. Request h-index and publication data from Scopus / SciVal APIs
3. Update `staff.scopus_hindex`
4. Update `staff.scopus_hindex_updated_at`
5. Import publications from 2020 onward
6. Deduplicate publications by `scopus_eid`
7. Update or insert rows in `publications`
8. Refresh `publications.updated_at`

### 7.1 Scheduler behavior

After the app starts successfully, the scheduler can start automatically.

Notes:

- The daily run time is controlled by `SCOPUS_SYNC_HOUR` and `SCOPUS_SYNC_MINUTE`
- The scheduler uses a `cron` trigger, so the sync runs once per day at the configured `Asia/Bangkok` time
- If `WEB_CONCURRENCY` is not set, the code behaves as if it were `1`
- When `WEB_CONCURRENCY > 1`, the scheduler does not start by default
- This prevents duplicate scheduled runs across multiple workers

### 7.2 Publication link selection

When the site displays a publication link, the current selection order is:

1. DOI URL
2. Scopus URL
3. API fallback URL

If an older database row already contains a better non-Scopus link, the synchronization logic attempts to preserve that link.

---

## 8. Database Notes

Main tables currently used by the app:

- `users`
  - Administrator account data
- `general_info`
  - Homepage text content
- `home_activity_images`
  - Homepage activity images
- `staff`
  - Staff records, including Scopus identifiers and h-index values
- `research_projects`
  - Research project records
- `publications`
  - Public publication records synchronized from Scopus

Additional behavior:

- `finished` projects appear in the public listing page
- `finished` projects still remain searchable by their saved data
- Only `ongoing` projects currently have a public detail page

Important Scopus-related columns:

- `staff.scopus_author_id`
- `staff.scopus_hindex`
- `staff.scopus_hindex_updated_at`
- `publications.scopus_eid`
- `publications.updated_at`

---

## 9. Current Maintenance Responsibilities

Maintained manually in the administrator interface:

- Homepage content
- Staff records
- Research project records
- Uploaded homepage and project-related assets

Maintained automatically by the system:

- Staff h-index data
- Publication records from 2020 onward
