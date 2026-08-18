# SCEM Website

This repository contains the current SCEM website and its Scopus synchronization workflow.

The project has two main parts:

- `Website application`
  - Public-facing pages and the admin back office
- `Scopus synchronization`
  - Uses the Scopus and SciVal APIs together with Flask-APScheduler to update staff h-index values and publication records

---

## 1. Key Files

- `app.py`
  - Main Flask application entry point
- `services/scopus_sync_service.py`
  - Calls the Scopus APIs and synchronizes h-index values and publication data
- `services/scopus_scheduler.py`
  - Starts Flask-APScheduler and runs the scheduled Scopus synchronization job
- `database/`
  - Database access helpers and startup migration logic
- `routes/`
  - Public, authentication, admin, and publications API routes
- `templates/`
  - HTML templates
- `static/`
  - CSS, JavaScript, images, audio, PDF files, and uploaded assets
- `schema.sql`
  - Base schema and seed data used to initialize an empty database
- `scem.db`
  - Active SQLite database file
- `.env`
  - Local environment settings such as `SECRET_KEY`, `SCOPUS_API_KEY`, and scheduler options
- `Dockerfile`
  - Docker image build configuration using `gunicorn` as the web server
- `docker-compose.yml`
  - Docker runtime configuration, including ports, `.env`, `scem.db`, and `static/uploads`

---

## 2. Environment Setup

### 2.1 Install Dependencies

```powershell
pip install -r requirements.txt
```

Primary packages used by this project:

- `Flask`
- `Flask-APScheduler`
- `python-dotenv`
- `gunicorn`

### 2.2 Configure `.env`

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-with-your-own-secret
SCOPUS_API_KEY=replace-with-your-scopus-key
DEFAULT_ADMIN_USERNAME=SCEM_admin
DEFAULT_ADMIN_PASSWORD=replace-with-your-admin-password
SCOPUS_SYNC_INTERVAL_MINUTES=1440
WEB_CONCURRENCY=1
```

Field descriptions:

- `SECRET_KEY`
  - Secret key used for Flask sessions
- `SCOPUS_API_KEY`
  - API key for Scopus / SciVal requests
- `DEFAULT_ADMIN_USERNAME`
  - Initial administrator username used for account creation or reset
- `DEFAULT_ADMIN_PASSWORD`
  - Initial administrator password used for account creation or reset
- `SCOPUS_SYNC_INTERVAL_MINUTES`
  - Interval, in minutes, for the automatic synchronization job
- `WEB_CONCURRENCY`
  - Number of web workers. Keep this project at `1` unless the scheduler is moved out of process.

---

## 3. Running the Website

### 3.1 Run Locally

```powershell
python app.py
```

Default local URL:

```text
http://127.0.0.1:3000
```

Typical startup output:

```text
Scopus scheduler started.
SQLite database connection succeeded.
In-process Scopus scheduler is running.
```

### 3.2 Run with Docker

Build the image:

```powershell
docker compose build
```

Start the container:

```powershell
docker compose up -d
```

If you change Python code, templates, or CSS, rebuild before restarting because the entire project directory is not bind-mounted into the container:

```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
```

Docker currently preserves:

- `scem.db`
- `static/uploads`

---

## 4. Website Structure

### 4.1 Public Pages

- `/`
  - Homepage
- `/staff`
  - Staff page
- `/research`
  - Research projects page
- `/publications`
  - Publications page
- `/project/<id>`
  - Detail page for a single ongoing project
- `/api/publications`
  - JSON API used by the publications page

### 4.2 Admin Pages

All admin pages currently live under:

```text
/0630_SCEMadmin
```

Available admin pages:

- `/0630_SCEMadmin/login`
  - Administrator login
- `/0630_SCEMadmin/change-credentials`
  - Forced credential change after first login or after a reset
- `/0630_SCEMadmin/dashboard`
  - Admin dashboard
- `/0630_SCEMadmin/general-info`
  - Homepage text and activity image management
- `/0630_SCEMadmin/staff`
  - Staff data management
- `/0630_SCEMadmin/projects`
  - Research project management
- `/0630_SCEMadmin/passwords`
  - Administrator credential reset page

Only a single administrator account is currently supported.

---

## 5. Administrator Login Flow

The initial administrator credentials come from:

- Username: `DEFAULT_ADMIN_USERNAME`
- Password: `DEFAULT_ADMIN_PASSWORD`

After the first login, or after an account reset, the administrator must:

1. Enter the current password
2. Choose a new username
3. Choose a new password
4. Confirm the new password

Rules:

- The new username must differ from the temporary username
- The new username must be unique
- The new password must contain at least 8 characters
- The new password must differ from the current password

---

## 6. Scopus Synchronization

The old browser crawler, manual publication review flow, and manual sync page have been removed.

Current synchronization flow:

1. Read all staff records that have a `scopus_author_id`
2. Call the Scopus / SciVal APIs
3. Update `staff.scopus_hindex`
4. Update `staff.scopus_hindex_updated_at`
5. Import publications from 2020 onward
6. Deduplicate by `scopus_eid`
7. Write results into the `publications` table
8. Update `publications.scopus_last_updated_at`

### 6.1 Scheduler Behavior

The scheduler starts automatically whenever the website starts successfully.

Its interval is controlled by `SCOPUS_SYNC_INTERVAL_MINUTES`.

The application also keeps the multi-worker safeguard:

- If `WEB_CONCURRENCY > 1`
  - The scheduler does not start by default
- This avoids duplicate synchronization runs across multiple workers

### 6.2 Publication URL Selection Rules

Each publication shown on the public site uses the first available URL in this order:

1. DOI URL
2. Scopus URL
3. Fallback URL returned by the API

If an existing record already has a better non-Scopus URL, the synchronization logic tries to preserve it.

---

## 7. Database Notes

Primary tables in use:

- `users`
  - Administrator account and forced password-change state
- `general_info`
  - Homepage text content
- `home_activity_images`
  - Homepage activity images
- `staff`
  - Staff data including Scopus author IDs and h-index values
- `research_projects`
  - Research project data
- `publications`
  - Public publication records synchronized from Scopus

Additional notes:

- `finished` research projects are currently presented as list-only public entries
- In practice, `finished` project records are kept with title and year fields for public display and search
- Detailed public project pages are currently available only for `ongoing` projects

Important Scopus-related columns:

- `staff.scopus_author_id`
- `staff.scopus_hindex`
- `staff.scopus_hindex_updated_at`
- `publications.scopus_eid`
- `publications.scopus_last_updated_at`

Migration notes:

- `publications.source_type` is no longer used
- If an older database still contains that column, startup migration removes it automatically
- Legacy contributor accounts are also cleaned up so the project keeps a single-admin structure

---

## 8. Current Maintenance Scope

Still maintained manually in the admin back office:

- Homepage content
- Staff data
- Research project data
- Uploaded images and related static files

Maintained automatically by the system:

- Staff h-index values
- Publications from 2020 onward

No longer part of this project:

- Playwright crawler
- Windows Task Scheduler `.bat` scripts
- Separate faculty / researcher login accounts
- Publication request and approval flow
- Manual publication management page
