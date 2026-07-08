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

See `requirements.txt` for full dependency list.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nazitora/Automatic-Testing-Mytravaly.git
cd MyTravalyAutomation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

### Run all tests:
```bash
pytest -v
```

### Run regression tests:
```bash
pytest -m regression -v
```

### Run smoke tests:
```bash
pytest -m smoke -v
```

### Run tests with HTML report:
```bash
pytest --html=reports/report.html --self-contained-html
```

## Test Categories

- **Regression Tests**: Comprehensive test suite marked with `@pytest.mark.regression`
- **Smoke Tests**: Quick sanity checks marked with `@pytest.mark.smoke`

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

## Contributing

1. Create a new branch for your changes
2. Write tests following the existing pattern
3. Ensure all tests pass before pushing
4. Commit with meaningful messages
5. Push to GitHub

## Reporting Issues

If you find any issues, please open an issue on GitHub with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

## License

[Add your license here]

## Contact

For questions or support, please reach out to the project maintainers.
