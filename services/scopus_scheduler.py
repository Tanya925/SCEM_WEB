# Attach Flask-APScheduler to the SCEM site and run the Scopus sync job on a schedule.

import os
import time
from zoneinfo import ZoneInfo

try:
    from flask_apscheduler import APScheduler
except ImportError:  # pragma: no cover - optional dependency until installed
    APScheduler = None

from services.scopus_sync_service import sync_scopus_dataset

BANGKOK_TIMEZONE = ZoneInfo("Asia/Bangkok")

scheduler = APScheduler() if APScheduler is not None else None

# Job function executed by APScheduler to run one Scopus synchronization pass and print a short deployment-friendly summary.
def run_scheduled_scopus_sync() -> None:
    started_at = time.time()
    print("Scopus sync started.", flush=True)

    try:
        result = sync_scopus_dataset()
    except Exception as error:
        elapsed_seconds = round(time.time() - started_at, 2)
        print(
            f"Scopus sync failed after {elapsed_seconds} seconds: {error}",
            flush=True,
        )
        raise

    publication_summary = result["publication_summary"]
    elapsed_seconds = round(time.time() - started_at, 2)
    print(
        "Scopus sync completed. "
        f"staff processed: {result['staff_count']}, "
        f"h-index updated: {result['hindex_updated_count']}, "
        f"publications inserted: {publication_summary['inserted_count']}, "
        f"publications refreshed: {publication_summary['updated_count']}, "
        f"duration: {elapsed_seconds} seconds.",
        flush=True,
    )
    if result["errors"]:
        print("Scopus sync completed with staff-level errors:", flush=True)
        for error in result["errors"]:
            print(f"- {error}", flush=True)

#
#     Decide whether this Flask process should start the built-in scheduler.
#
#     This mainly prevents duplicate scheduler startup during debug reloads or
#     when the site is running with multiple web workers.
#     
def should_start_scheduler(flask_app) -> bool:
    if flask_app.debug and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        return False

    worker_count_text = str(os.environ.get("WEB_CONCURRENCY", "1")).strip()
    try:
        worker_count = int(worker_count_text)
    except ValueError:
        worker_count = 1

    force_scheduler = str(os.environ.get("SCOPUS_SCHEDULER_FORCE", "")).strip().lower()
    if worker_count > 1 and force_scheduler not in {"1", "true", "yes", "on"}:
        print(
            "Scopus scheduler was not started because WEB_CONCURRENCY is greater than 1. "
            "This avoids duplicate runs across multiple workers."
        )
        return False

    return True

#
#     Initialize Flask-APScheduler and start it when conditions allow.
#
#     Returns `True` when the scheduler is started in this process.
#     
def init_scopus_scheduler(flask_app) -> bool:
    if scheduler is None:
        print(
            "Flask-APScheduler is not installed yet. "
            "Install it before running the Scopus scheduler."
        )
        return False

    flask_app.config.setdefault("SCHEDULER_API_ENABLED", False)
    flask_app.config["SCHEDULER_TIMEZONE"] = BANGKOK_TIMEZONE
    scheduler.init_app(flask_app)

    if scheduler.get_job("scopus_sync_job") is None:
        hour_text = str(os.environ.get("SCOPUS_SYNC_HOUR", "2")).strip()
        minute_text = str(os.environ.get("SCOPUS_SYNC_MINUTE", "0")).strip()

        try:
            sync_hour = min(max(int(hour_text), 0), 23)
        except ValueError:
            sync_hour = 2

        try:
            sync_minute = min(max(int(minute_text), 0), 59)
        except ValueError:
            sync_minute = 0

        scheduler.add_job(
            id="scopus_sync_job",
            func=run_scheduled_scopus_sync,
            trigger="cron",
            hour=sync_hour,
            minute=sync_minute,
            timezone=BANGKOK_TIMEZONE,
            replace_existing=True,
            max_instances=1,
        )
        print(
            f"Scopus scheduler configured for daily sync at {sync_hour:02d}:{sync_minute:02d} Asia/Bangkok.",
            flush=True,
        )

    if should_start_scheduler(flask_app) and not scheduler.running:
        scheduler.start()
        print("Scopus scheduler started.")
        return True

    return False

