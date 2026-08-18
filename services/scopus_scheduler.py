"""Attach Flask-APScheduler to the SCEM site and run the Scopus sync job on a schedule."""

"""Attach Flask-APScheduler to the SCEM site and run the Scopus sync on a schedule."""

import os

try:
    from flask_apscheduler import APScheduler
except ImportError:  # pragma: no cover - optional dependency until installed
    APScheduler = None

from services.scopus_sync_service import sync_scopus_dataset

scheduler = APScheduler() if APScheduler is not None else None

def run_scheduled_scopus_sync() -> None:
    """Job function executed by APScheduler to run one Scopus synchronization pass and print a short deployment-friendly summary."""
    result = sync_scopus_dataset()
    publication_summary = result["publication_summary"]
    print(
        "Scheduled Scopus sync completed. "
        f"h-index updated: {result['hindex_updated_count']}, "
        f"publications inserted: {publication_summary['inserted_count']}, "
        f"publications refreshed: {publication_summary['updated_count']}."
    )
    if result["errors"]:
        print("Scheduled Scopus sync had staff-level errors:")
        for error in result["errors"]:
            print(f"- {error}")

def should_start_scheduler(flask_app) -> bool:
    """
    Decide whether this Flask process should start the built-in scheduler.

    This mainly prevents duplicate scheduler startup during debug reloads or
    when the site is running with multiple web workers.
    """
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

def init_scopus_scheduler(flask_app) -> bool:
    """
    Initialize Flask-APScheduler and start it when conditions allow.

    Returns `True` when the scheduler is started in this process.
    """
    if scheduler is None:
        print(
            "Flask-APScheduler is not installed yet. "
            "Install it before running the Scopus scheduler."
        )
        return False

    flask_app.config.setdefault("SCHEDULER_API_ENABLED", False)
    scheduler.init_app(flask_app)

    if scheduler.get_job("scopus_sync_job") is None:
        interval_minutes_text = str(
            os.environ.get("SCOPUS_SYNC_INTERVAL_MINUTES", "1440")
        ).strip()
        try:
            interval_minutes = max(1, int(interval_minutes_text))
        except ValueError:
            interval_minutes = 1440

        scheduler.add_job(
            id="scopus_sync_job",
            func=run_scheduled_scopus_sync,
            trigger="interval",
            minutes=interval_minutes,
            replace_existing=True,
            max_instances=1,
        )

    if should_start_scheduler(flask_app) and not scheduler.running:
        scheduler.start()
        print("Scopus scheduler started.")
        return True

    return False
