# QA Automation Framework — Selenium + pytest + REST API

A production-style test automation framework built with **Python**, **Selenium WebDriver**, and **pytest**, following the **Page Object Model (POM)** design pattern. Covers UI automation across two web applications and REST API testing — all integrated with a CI/CD pipeline via GitHub Actions.

---

## 📊 Test Suite Summary

| Suite | Application | Tests | Type |
|---|---|---|---|
| Google Search | google.com | 12 | UI / Selenium |
| Saucedemo E2E | saucedemo.com | 17 | UI / Selenium |
| REST API | jsonplaceholder.typicode.com | 22 | API / requests |
| **Total** | | **51** | |

**CI/CD Status:** All 51 tests passing on GitHub Actions (Ubuntu Linux) ✅

---

## 🗂️ Project Structure

```
qa_automation/
├── pages/                          # Page Object classes
│   ├── base_page.py                # Shared methods (waits, navigation, JS helpers)
│   ├── google_page.py              # Google search page interactions
│   ├── login_page.py               # Saucedemo login page
│   ├── products_page.py            # Saucedemo products/inventory page
│   └── cart_page.py                # Saucedemo cart and checkout pages
├── tests/                          # Test files
│   ├── test_google.py              # 12 Google search tests
│   ├── test_saucedemo.py           # 17 Saucedemo e-commerce tests
│   └── test_api.py                 # 22 REST API tests
├── utils/                          # Shared utilities
│   ├── driver_factory.py           # Chrome WebDriver setup (headless, anti-detection)
│   ├── screenshot_helper.py        # Auto screenshot on test failure
│   └── api_client.py               # HTTP client for API tests (requests wrapper)
├── test_data/
│   └── users.csv                   # Data-driven login test data
├── .github/
│   └── workflows/
│       └── tests.yml               # GitHub Actions CI/CD pipeline
├── screenshots/                    # Auto-captured on test failure
├── reports/                        # HTML test reports (auto-generated)
├── conftest.py                     # pytest fixtures, setup/teardown, failure hooks
├── pytest.ini                      # pytest config — markers, logging, report path
└── requirements.txt                # Python dependencies
```

---

## ✅ Features

| Feature | Implementation |
|---|---|
| Page Object Model (POM) | `pages/` — one class per page, locators + actions separated |
| UI Automation | Selenium WebDriver 4.x with Chrome |
| REST API Testing | Python `requests` library — GET, POST, PUT, DELETE |
| Data-Driven Testing | CSV-based login tests via `@pytest.mark.parametrize` |
| Auto Screenshot on Failure | `conftest.py` hook + `utils/screenshot_helper.py` |
| Smoke / Regression Markers | `pytest.ini` + `@pytest.mark.smoke` / `@pytest.mark.regression` |
| HTML Test Reports | `pytest-html` — self-contained reports with logs and durations |
| CI/CD Pipeline | GitHub Actions — runs on every push to `main` |
| Cross-Platform Driver | `driver_factory.py` — works on Windows (local) and Ubuntu Linux (CI/CD) |
| Logging | Python `logging` module throughout all page objects and utilities |
| React-Compatible Input | Native `HTMLInputElement` setter + `dispatchEvent` for React form fields |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- Google Chrome installed

### Clone and install
```bash
git clone https://github.com/sgr111/qa-automation-framework.git
cd qa-automation-framework
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

## ▶️ Running Tests

```bash
# Run all 51 tests
pytest

# Run only smoke tests (fastest — core functionality)
pytest -m smoke

# Run only regression tests
pytest -m regression

# Run a specific suite
pytest tests/test_google.py -v
pytest tests/test_saucedemo.py -v
pytest tests/test_api.py -v

# Run a single test
pytest tests/test_saucedemo.py::TestSaucedemoCheckout::test_complete_checkout_flow -v

# Run with visible browser (non-headless)
# Edit driver_factory.py — change headless=True to headless=False

# Run tests in parallel
pytest -n 4
```

---

## 📊 Test Reports

HTML reports are auto-generated after each run:
```
reports/report.html
```
Open in any browser to view pass/fail results, logs, durations, and inline failure screenshots.

---

## 🧪 Test Cases

### Google Search Suite (12 tests)
| Test | Marker | Description |
|---|---|---|
| `test_google_title_contains_google` | smoke | Homepage title includes "Google" |
| `test_google_title_is_exactly_google` | smoke | Title is exactly "Google" |
| `test_google_url_is_correct` | smoke | URL contains "google.com" |
| `test_search_returns_results` | regression | Parameterized — 4 queries return results |
| `test_search_result_stats_shown` | regression | Result stats text is visible |
| `test_first_result_has_valid_link` | regression | First result has a valid https link |
| `test_search_title_updates_after_search` | regression | Title updates after search |
| `test_search_with_special_characters` | regression | Special chars don't crash browser |
| `test_search_with_very_long_query` | regression | Long input handled gracefully |

### Saucedemo E2E Suite (17 tests)
| Test | Marker | Description |
|---|---|---|
| `test_login_valid_user` | smoke | Standard user can log in successfully |
| `test_login_invalid_password` | regression | Wrong password shows error message |
| `test_login_locked_out_user` | regression | Locked user sees correct error |
| `test_products_page_loads` | smoke | Products page title is correct |
| `test_product_count` | regression | 6 products displayed |
| `test_add_to_cart` | smoke | Add to cart updates badge count |
| `test_remove_from_cart` | regression | Remove from cart clears badge |
| `test_cart_contains_added_item` | regression | Cart shows correct item name |
| `test_sort_price_low_to_high` | regression | Products sort correctly |
| `test_complete_checkout_flow` | regression | Full add → cart → checkout → confirmation |
| *(+ 7 more covering navigation, data-driven login, negative cases)* | | |

### REST API Suite (22 tests)
| Test Class | Coverage |
|---|---|
| `TestPostsAPI` | GET all, GET one, POST, PUT, DELETE, filter by userId, 404 handling |
| `TestUsersAPI` | GET all, GET one, field validation, email format check |
| `TestCommentsAPI` | GET all, filter by postId, field validation |
| `TestAPIHeaders` | Content-Type validation, response time under 2 seconds |

---

## 🔁 CI/CD Pipeline

Tests run automatically on every push to `main` via **GitHub Actions**.

**Pipeline steps:**
1. Spin up Ubuntu Linux runner
2. Install Python 3.11
3. Install Chrome browser
4. Install Python dependencies
5. Run smoke tests → generate smoke report
6. Run regression tests → generate regression report
7. Run full suite → generate full report
8. Upload HTML reports as downloadable artifacts
9. Upload failure screenshots as artifacts (only on failure)

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11 | Core language |
| Selenium WebDriver | 4.x | Browser automation |
| pytest | 8.x | Test framework |
| requests | 2.31.0 | REST API testing |
| webdriver-manager | latest | Auto ChromeDriver management |
| pytest-html | 4.x | HTML test reports |
| pytest-xdist | 3.x | Parallel test execution |
| pytest-mock | 3.12 | Mocking support |
| GitHub Actions | — | CI/CD pipeline |

---

## 🐛 Notable Debugging Challenges Solved

**React Synthetic Event System**
Saucedemo is built with React. Standard `send_keys()` and JavaScript `.value =` assignments are ignored by React's internal state system. Fixed by using React's native `HTMLInputElement` property setter combined with a dispatched `input` event — the only method React recognises as a genuine user input.

**Chrome Password Manager Popup**
Chrome's built-in password breach warning intercepts keyboard and mouse events at the browser level — outside the DOM, invisible to Selenium and JavaScript. Fixed by routing all form interactions through JavaScript rather than simulated keyboard input.

**Cross-Platform ChromeDriver**
Hardcoded Windows paths break on Linux CI runners. Fixed with `os.path.exists()` fallback to `webdriver-manager` on Linux, plus `os.chmod()` to set execute permissions — which Linux requires on downloaded binaries.

---

## 📌 Author

**Sourabh Sagar** — QA Automation Engineer
Built as a portfolio project demonstrating industry-standard automation practices.
GitHub: [github.com/sgr111/qa-automation-framework](https://github.com/sgr111/qa-automation-framework)
