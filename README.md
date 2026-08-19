# SCEM Website Project

This project contains the current SCEM website together with the automation flow that synchronizes Scopus publications and h-index data.

The current codebase is mainly split into two parts:

- `Website application`
  - Contains the public-facing pages and the administrator management interface
- `Scopus synchronization`
  - Uses the Scopus / SciVal API together with `Flask-APScheduler` to automatically update staff h-index data and publication records

---

## 1. Important Files

- `app.py`
  - Main entry point for the Flask application
- `services/scopus_sync_service.py`
  - Calls the Scopus APIs and synchronizes h-index data plus publication records
- `services/scopus_scheduler.py`
  - Starts `Flask-APScheduler` and runs the scheduled Scopus synchronization job
- `database/`
  - Database access helpers and startup-time table completion logic
- `routes/`
  - Routes for the public pages, login, admin pages, and publications API
- `templates/`
  - HTML template files
- `static/`
  - CSS, JavaScript, images, audio, PDF, and uploaded assets
- `schema.sql`
  - Table structure and seed content for initializing an empty database
- `scem.db`
  - The SQLite database currently used by the project
- `.env`
  - Local environment settings such as `SECRET_KEY`, `SCOPUS_API_KEY`, and scheduler settings
- `Dockerfile`
  - Docker build configuration that starts the site with `gunicorn`
- `docker-compose.yml`
  - Docker runtime configuration, including ports, `.env`, `scem.db`, and `static/uploads`

---

## 2. Environment Setup

### 2.1 Install dependencies

```powershell
pip install -r requirements.txt
```

The main packages used by this project include:

- `Flask`
- `Flask-APScheduler`
- `python-dotenv`
- `gunicorn`

### 2.2 Configure `.env`

Create a `.env` file in the project root:

```env
SECRET_KEY=replace_with_your_own_secret
SCOPUS_API_KEY=your_scopus_api_key_here
SCOPUS_SYNC_INTERVAL_MINUTES=1440
WEB_CONCURRENCY=1
```

Field descriptions:

- `SECRET_KEY`
  - Secret used for Flask sessions
- `SCOPUS_API_KEY`
  - API key for Scopus / SciVal requests
- `SCOPUS_SYNC_INTERVAL_MINUTES`
  - Interval for the automatic synchronization job, in minutes
- `WEB_CONCURRENCY`
  - Number of website workers. Keep this at `1` if the scheduler still runs in the same process as the site

---

## 3. Running the Website

### 3.1 Run locally

```powershell
python app.py
```

Default local URL:

```text
http://127.0.0.1:3000
```

Common startup output:

```text
Scopus scheduler started.
SQLite database connected successfully.
The Scopus scheduler is running in this process.
```

### 3.2 Run with Docker

Build the image:

```powershell
docker compose build
```

Start the containers:

```powershell
docker compose up -d
```

If you changed Python files, templates, or CSS, the full project directory is not mounted into the container, so rebuild before starting again:

```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
```

Docker currently preserves:

- `scem.db`
- `static/uploads`

---

## 4. Site Structure

### 4.1 Public pages

- `/`
  - Home page
- `/staff`
  - Team members page
- `/research`
  - Research projects page
- `/publications`
  - Publications page
- `/project/<id>`
  - Detail page for one ongoing project
- `/api/publications`
  - JSON API used by the publications page

### 4.2 Admin pages

All admin pages currently live under:

```text
/0630_SCEMadmin
```

Available admin pages:

- `/0630_SCEMadmin/login`
  - Administrator login page
- `/0630_SCEMadmin/dashboard`
  - Admin dashboard
- `/0630_SCEMadmin/general-info`
  - Home-page text and activity-image management
- `/0630_SCEMadmin/staff`
  - Team member management
- `/0630_SCEMadmin/projects`
  - Research project management
- `/0630_SCEMadmin/passwords`
  - Administrator username and password settings

The current system supports only one administrator account, and the code does not automatically create a default login username or password.

---

## 5. Administrator Credentials

If the administrator username or password needs to be changed later, use:

- `/0630_SCEMadmin/passwords`

The update rules are:

- The new username must not duplicate an existing username
- The current password must be entered before saving
- The new password must be at least 8 characters long
- The new password must not match the current password

---

## 6. Scopus Synchronization Flow

The older browser crawler, manual publication review flow, and manual synchronization page have all been removed.

The current synchronization flow is:

1. Read every staff record that has `scopus_author_id`
2. Call the Scopus / SciVal APIs
3. Update `staff.scopus_hindex`
4. Update `staff.scopus_hindex_updated_at`
5. Import publications from 2020 onward
6. Deduplicate by `scopus_eid`
7. Write the result into the `publications` table
8. Update `publications.scopus_last_updated_at`

### 6.1 Scheduler behavior

After the website starts successfully, the scheduler starts automatically.

The run interval is controlled by `SCOPUS_SYNC_INTERVAL_MINUTES`.

The system still keeps a multi-worker safety guard:

- When `WEB_CONCURRENCY > 1`
  - The scheduler does not start by default
- This prevents multiple workers from running the same synchronization job at the same time

### 6.2 Publication link selection

When displaying a publication on the public site, the link is chosen in this order:

1. DOI URL
2. Scopus URL
3. Fallback URL returned by the API

If the database already has a better non-Scopus link, the synchronization logic tries to preserve it.

---

## 7. Database Notes

Main tables currently used:

- `users`
  - Administrator account data
- `general_info`
  - Home-page text content
- `home_activity_images`
  - Home-page activity images
- `staff`
  - Team member records, including Scopus Author ID and h-index
- `research_projects`
  - Research project records
- `publications`
  - Public publication records synchronized from Scopus

Additional notes:

- `finished` research projects currently appear only in the public list view
- In practice, `finished` projects still retain their titles and years for public display and search
- Only `ongoing` projects currently provide a public detail page

Important Scopus-related columns:

- `staff.scopus_author_id`
- `staff.scopus_hindex`
- `staff.scopus_hindex_updated_at`
- `publications.scopus_eid`
- `publications.scopus_last_updated_at`

The current code assumes the database already follows the active schema:

- `users` uses the single-administrator model
- `publications` uses `scopus_eid` and `scopus_last_updated_at` as the synchronization identity and refresh fields

---

## 8. Current Maintenance Scope

Still maintained manually in the admin interface:

- Home-page content
- Team member data
- Research project data
- Uploaded images and related static assets

Maintained automatically by the system:

- Staff h-index data
- Publication records from 2020 onward

Features that are no longer part of this project:

- Playwright crawler automation
- Windows Task Scheduler `.bat` scripts
- Separate staff / researcher account logins
- Publication request and review workflows
- Manual publication management pages
