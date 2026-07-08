"""Centralized configuration for the MT India Render module tests."""

import os

BASE_URL = os.environ.get("BASE_URL", "https://mtindia-v2-admin.onrender.com")
ADMIN_ROUTE_PATHS = ("login", "admin", "dashboard")
PROPERTY_TAB_NAMES = ("Hotels", "Resorts", "Home Stays", "Camps & Tents")

IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "screenshots")
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
JSON_REPORT_PATH = os.path.join(REPORT_DIR, "report.json")

# Ensure directories exist
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
