# QA Automation Framework — Selenium + Pytest

A production-style test automation framework built with **Python**, **Selenium WebDriver**, and **pytest**, following the **Page Object Model (POM)** design pattern.

---

## 🗂️ Project Structure

```
qa_automation/
├── pages/                      # Page Object classes
│   ├── base_page.py            # Shared methods (wait, navigate, etc.)
│   └── google_page.py          # Google-specific page interactions
├── tests/                      # Test files
│   └── test_google.py          # Google search test suite
├── utils/                      # Helpers
│   ├── driver_factory.py       # WebDriver initialization
│   └── screenshot_helper.py    # Auto screenshot on failure
├── .github/
│   └── workflows/
│       └── tests.yml           # GitHub Actions CI/CD pipeline
├── screenshots/                # Auto-captured on test failure
├── reports/                    # HTML test reports (auto-generated)
├── conftest.py                 # Pytest fixtures & hooks
├── pytest.ini                  # Pytest configuration & markers
└── requirements.txt            # Python dependencies
```

---

## ✅ Features

| Feature | Implementation |
|---|---|
| Page Object Model (POM) | `pages/base_page.py`, `pages/google_page.py` |
| Fixtures with setup/teardown | `conftest.py` |
| Custom markers (smoke / regression) | `pytest.ini` |
| Parameterized tests | `@pytest.mark.parametrize` |
| Screenshot on failure | `conftest.py` hook + `utils/screenshot_helper.py` |
| HTML test reports | `pytest-html` |
| CI/CD pipeline | GitHub Actions (`.github/workflows/tests.yml`) |
| Logging | Python `logging` module throughout |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- Google Chrome installed

### Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running Tests

```bash
# Run all tests
pytest

# Run only smoke tests
pytest -m smoke

# Run only regression tests
pytest -m regression

# Run with visible browser (non-headless) — edit driver_factory.py: headless=False
pytest -m smoke

# Run tests in parallel (4 workers)
pytest -n 4
```

---

## 📊 Test Reports

HTML reports are auto-generated after each run:
```
reports/report.html
```
Open it in a browser to view pass/fail details, logs, and durations.

---

## 🔁 CI/CD

Tests run automatically on every `push` or `pull_request` to `main`/`develop` via **GitHub Actions**.

- Smoke tests run first
- Full regression follows
- Reports and screenshots are uploaded as artifacts

---

## 🧪 Test Cases

### Smoke Tests
- `test_google_title_contains_google` — Homepage title includes "Google"
- `test_google_title_is_exactly_google` — Title is exactly "Google"
- `test_google_url_is_correct` — URL contains "google.com"

### Regression Tests
- `test_search_returns_results` — Parameterized: 4 different queries return results
- `test_search_result_stats_shown` — Result stats text is visible
- `test_first_result_has_valid_link` — First result has a valid https link
- `test_search_title_updates_after_search` — Title changes after search

### Negative Tests
- `test_search_with_special_characters` — Special chars don't crash the browser
- `test_search_with_very_long_query` — Very long input is handled gracefully

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Selenium 4.x**
- **pytest 8.x**
- **webdriver-manager** (auto-downloads ChromeDriver)
- **pytest-html** (HTML reports)
- **pytest-xdist** (parallel test execution)
- **GitHub Actions** (CI/CD)

---

## 📌 Author

Built as a QA Automation portfolio project demonstrating industry-standard practices.
