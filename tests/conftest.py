from pathlib import Path
from datetime import datetime, timezone
import json
import sys

import pytest

# Ensure project root is on sys.path so imports like `utils` and `pages` work
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.config import BASE_URL, JSON_REPORT_PATH
from utils.driver_factory import get_driver


_JSON_REPORT = {
    "base_url": BASE_URL,
    "started_at": None,
    "finished_at": None,
    "duration_seconds": None,
    "summary": {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
    },
    "tests": [],
}


@pytest.fixture
def driver():
    browser = get_driver()
    try:
        yield browser
    finally:
        browser.quit()


def pytest_configure(config):
    _JSON_REPORT["started_at"] = datetime.now(timezone.utc).isoformat()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    status = report.outcome
    if status == "failed" and hasattr(report, "wasxfail"):
        status = "xpassed"

    _JSON_REPORT["tests"].append(
        {
            "nodeid": report.nodeid,
            "name": item.name,
            "file": str(item.path),
            "markers": [marker.name for marker in item.iter_markers()],
            "status": status,
            "duration_seconds": round(report.duration, 3),
            "message": report.longreprtext if report.failed else "",
        }
    )


def pytest_sessionfinish(session, exitstatus):
    finished_at = datetime.now(timezone.utc)
    started_at = datetime.fromisoformat(_JSON_REPORT["started_at"])
    tests = _JSON_REPORT["tests"]

    summary = _JSON_REPORT["summary"]
    summary["total"] = len(tests)
    summary["passed"] = sum(1 for test in tests if test["status"] == "passed")
    summary["failed"] = sum(1 for test in tests if test["status"] == "failed")
    summary["skipped"] = sum(1 for test in tests if test["status"] == "skipped")
    summary["errors"] = session.testsfailed - summary["failed"]

    _JSON_REPORT["finished_at"] = finished_at.isoformat()
    _JSON_REPORT["duration_seconds"] = round((finished_at - started_at).total_seconds(), 3)
    _JSON_REPORT["exitstatus"] = exitstatus

    report_path = Path(JSON_REPORT_PATH)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(_JSON_REPORT, indent=2), encoding="utf-8")
