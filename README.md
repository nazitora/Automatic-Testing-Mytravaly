# MyTravaly Automation Testing

Automated testing suite for MyTravaly application using Selenium and Pytest.

## Project Overview

This project contains automated UI tests for the MyTravaly admin module, focusing on:
- Location search functionality
- Date picker interactions
- Guest selection management
- Property tab navigation

## Project Structure
```
MyTravalyAutomation/
├── pages/                    # Page Object Models
│   ├── admin_module_page.py  # Admin module page interactions
│   └── __init__.py
├── tests/                    # Test files
│   ├── test_admin_interactions.py    # Admin module interaction tests
│   ├── test_admin_routes.py          # Admin route tests
│   ├── test_admin_smoke.py           # Smoke tests
│   ├── conftest.py                   # Pytest configuration & fixtures
│   └── __init__.py
├── utils/                    # Utility modules
│   ├── config.py             # Configuration settings
│   ├── driver_factory.py     # WebDriver factory
│   └── __init__.py
├── reports/                  # Test reports
│   ├── report.html
│   └── report.json
├── screenshots/              # Test screenshots
├── requirements.txt          # Python dependencies
├── pytest.ini                # Pytest configuration
└── README.md                 # This file
```


## Requirements

- Python 3.x
- Selenium
- Pytest



## Installation
 Install dependencies:
 ```
pip install -r requirements.txt
```


## Running Tests

### Run all tests:
```
pytest -v
```

### Run tests with  report:
```
pytest -v \
  --html=reports/report.html \
  --self-contained-html \
  --json-report \
  --json-report-file=reports/report.json
```

## Key Test Cases

### Admin Module Interactions
- **Search Flow**: Tests location search and results navigation
- **Date Picker**: Tests date range selection
- **Guest Selector**: Tests guest count updates
- **Property Tabs**: Tests tab switching and content updates

## Configuration

Configuration settings can be found in `utils/config.py`. Update this file to configure:
- Application URL
- Browser settings
- Timeouts
- Other environment-specific settings

## Page Objects

The project follows the Page Object Model pattern:
- `AdminModulePage`: Encapsulates interactions with the admin module





