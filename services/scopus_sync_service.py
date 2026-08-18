"""Synchronize staff h-index values and publication records from the Scopus APIs into local SQLite."""

"""Synchronize staff h-index values and publication data from the Scopus APIs into local SQLite."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from database.publication_db import sync_scopus_publications
from database.staff_db import get_staff_scopus_targets, update_staff_scopus_metrics

AUTHOR_METRICS_URL = "https://api.elsevier.com/analytics/scival/author/metrics"

PUBLICATION_SEARCH_URL = "https://api.elsevier.com/content/search/scopus"

DEFAULT_PUBLICATION_START_YEAR = 2020

DEFAULT_PAGE_SIZE = 25

REQUEST_TIMEOUT_SECONDS = 45

class ScopusSyncError(RuntimeError):
    """Raised when the Scopus synchronization flow cannot be completed safely."""

def get_scopus_api_key() -> str:
    """Read the Scopus API key from the environment."""
    api_key = os.environ.get("SCOPUS_API_KEY", "").strip()
    if not api_key:
        raise ScopusSyncError("SCOPUS_API_KEY is not configured.")
    return api_key

def perform_scopus_request(url: str, params: dict[str, object]) -> dict:
    """
    Call one Scopus API endpoint and return the decoded JSON response.

    This helper is the shared entry point for all Scopus requests.
    """
    query_string = urlencode(
        {
            key: value
            for key, value in params.items()
            if value not in ("", None)
        }
    )
    request = Request(
        f"{url}?{query_string}",
        headers={
            "Accept": "application/json",
            "X-ELS-APIKey": get_scopus_api_key(),
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="ignore")
        raise ScopusSyncError(
            f"Scopus API returned HTTP {error.code}: {error_body or error.reason}"
        ) from error
    except URLError as error:
        raise ScopusSyncError(f"Could not reach the Scopus API: {error.reason}") from error

    try:
        return json.loads(payload)
    except json.JSONDecodeError as error:
        raise ScopusSyncError("Scopus API returned invalid JSON.") from error

def extract_hindex(metrics_payload: dict) -> int | None:
    """Extract the h-index value from a SciVal metrics payload."""
    results = metrics_payload.get("results") or []
    if not results:
        return None

    metrics = results[0].get("metrics") or []
    for metric in metrics:
        if metric.get("metricType") == "HIndices":
            value = metric.get("value")
            try:
                return int(value)
            except (TypeError, ValueError):
                return None

    return None

def fetch_staff_hindex(author_id: str) -> int | None:
    """Fetch one staff member's h-index by Scopus Author ID through the SciVal metrics API."""
    payload = perform_scopus_request(
        AUTHOR_METRICS_URL,
        {
            "authors": author_id,
            "metricTypes": "hIndices",
            "byYear": "false",
            "yearRange": "5yrsAndCurrent",
        },
    )
    return extract_hindex(payload)

def normalize_authors(entry: dict) -> str:
    """Normalize the Scopus author field into the format stored by the website database."""
    author_text = str(entry.get("author_names") or "").strip()
    if author_text:
        return author_text.replace("|", ";")

    creator = str(entry.get("dc:creator") or "").strip()
    return creator

def build_publication_url(entry: dict) -> str:
    """
    Pick the most suitable public-facing link for one publication.

    Priority order: DOI, Scopus page, then the generic API URL.
    """
    doi = str(entry.get("prism:doi") or "").strip()
    if doi:
        return f"https://doi.org/{doi}"

    for link in entry.get("link") or []:
        if link.get("@ref") == "scopus":
            return str(link.get("@href") or "").strip()

    return str(entry.get("prism:url") or "").strip()

def build_publication_record(entry: dict) -> dict | None:
    """
    Convert one Scopus search result into the website publication format.

    Skip entries that do not contain the minimum identity fields needed for a
    safe database write, such as the Scopus EID, title, or publication year.
    """
    scopus_eid = str(entry.get("eid") or "").strip()
    title = str(entry.get("dc:title") or "").strip()
    cover_date = str(entry.get("prism:coverDate") or "").strip()
    year_text = cover_date[:4] if len(cover_date) >= 4 else ""

    try:
        publication_year = int(year_text) if year_text else None
    except ValueError:
        publication_year = None

    if not scopus_eid or not title or publication_year is None:
        return None

    return {
        "scopus_eid": scopus_eid,
        "title": title,
        "authors": normalize_authors(entry),
        "journal": str(entry.get("prism:publicationName") or "").strip(),
        "publication_year": publication_year,
        "volume": str(entry.get("prism:volume") or "").strip(),
        "issue": str(entry.get("prism:issueIdentifier") or "").strip(),
        "article_number": str(entry.get("article-number") or "").strip(),
        "page": str(entry.get("prism:pageRange") or "").strip(),
        "pdf_url": build_publication_url(entry),
    }

def fetch_staff_publications(author_id: str, start_year: int = DEFAULT_PUBLICATION_START_YEAR) -> list[dict]:
    """
    Fetch all publications for one staff member from the selected start year.

    Results are paginated, so this function keeps requesting pages until the
    full result set has been collected.
    """
    publications = []
    start = 0

    while True:
        payload = perform_scopus_request(
            PUBLICATION_SEARCH_URL,
            {
                "query": f"au-id({author_id}) AND PUBYEAR > {start_year - 1}",
                "sort": "-coverDate",
                "count": DEFAULT_PAGE_SIZE,
                "start": start,
            },
        )

        search_results = payload.get("search-results") or {}
        entries = search_results.get("entry") or []
        if not isinstance(entries, list):
            entries = []

        for entry in entries:
            publication = build_publication_record(entry)
            if publication is not None:
                publications.append(publication)

        total_results_text = str(search_results.get("opensearch:totalResults") or "0").strip()
        try:
            total_results = int(total_results_text)
        except ValueError:
            total_results = len(publications)

        start += DEFAULT_PAGE_SIZE
        if not entries or start >= total_results:
            break

    return publications

def deduplicate_publications(publications: list[dict]) -> list[dict]:
    """
    Deduplicate publications by `scopus_eid` before writing to the database.

    The same paper can appear multiple times when several SCEM staff members are
    co-authors, but the public Publications page should keep only one record.
    """
    unique_publications = {}

    for publication in publications:
        scopus_eid = publication["scopus_eid"]
        if scopus_eid not in unique_publications:
            unique_publications[scopus_eid] = publication

    return sorted(
        unique_publications.values(),
        key=lambda item: (
            -(item.get("publication_year") or 0),
            item.get("title", "").lower(),
        ),
    )

def sync_scopus_dataset(start_year: int = DEFAULT_PUBLICATION_START_YEAR) -> dict:
    """
    Run one complete Scopus synchronization pass.

    This is the main orchestration entry point and returns a compact summary for
    the scheduler or any other caller that needs deployment-friendly output.
    """
    staff_targets = get_staff_scopus_targets()
    if not staff_targets:
        return {
            "staff_count": 0,
            "hindex_updated_count": 0,
            "publication_summary": {
                "inserted_count": 0,
                "updated_count": 0,
                "adopted_existing_count": 0,
                "active_count": 0,
            },
            "errors": [],
        }

    metric_rows = []
    publication_rows = []
    errors = []

    for staff in staff_targets:
        author_id = str(staff.get("scopus_author_id") or "").strip()
        display_name = staff.get("name_en") or staff.get("name_th") or f"staff-{staff['id']}"
        if not author_id:
            continue

        try:
            hindex = fetch_staff_hindex(author_id)
            metric_rows.append(
                {
                    "author_id": author_id,
                    "hindex": hindex,
                    "status": "success",
                }
            )

            publication_rows.extend(fetch_staff_publications(author_id, start_year=start_year))
        except Exception as error:
            errors.append(f"{display_name} ({author_id}): {error}")

    update_staff_scopus_metrics(metric_rows)

    publication_summary = sync_scopus_publications(
        deduplicate_publications(publication_rows)
    )

    return {
        "staff_count": len(staff_targets),
        "hindex_updated_count": len(metric_rows),
        "publication_summary": publication_summary,
        "errors": errors,
    }
