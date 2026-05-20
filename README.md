![Tests](https://github.com/donprather-ctrl/api-test-framework/actions/workflows/tests.yml/badge.svg)
 
## Project Description
A test automation framework built with Python, Pytest, and Playwright,
covering API testing, UI testing, and end-to-end workflows.
 
## Technology Stack
Python, Pytest, Playwright, dummyjson (dummyjson.com), saucedemo.com, GitHub Actions
 
## CI/CD
This project uses GitHub Actions with two jobs that run automatically
on every push and pull request. README-only changes do not trigger the pipeline.
 
- **Smoke** - runs on every push to any branch; fast critical-path tests
- **Regression** - runs only if smoke passes; full scenario coverage including
  edge cases and end-to-end workflows
- HTML test reports generated after every run and uploaded as downloadable artifacts
## Test Coverage
 
**Authentication (dummyjson)**
- Valid credentials return 200 and a well-formed JWT access token
- JWT structure validation: confirms three-segment format (header, payload, signature)
- JWT payload validation: confirms expected claims, valid expiry, and correct username
- Invalid credentials never return a token (6 parametrized scenarios:
  wrong username, wrong password, both wrong, empty username,
  empty password, both empty)
**Token Handling (dummyjson /auth/me)**
- Valid token accepted and returns current user profile
- Malformed token rejected (documents known dummyjson defect: returns 500 instead of 401)
- Empty token rejected with 401/403
- Tampered token rejected
- Missing auth header rejected with 401/403
**Users API (dummyjson)**
- Get all users
- Get user by ID (valid ID, non-existent ID, invalid type)
- Create user
- Update user
- Delete user
- End-to-end user lifecycle: Create, Get, Update, Delete
**UI (saucedemo.com)**
- Valid login navigates to products page
- Invalid login displays error message
- Add product to cart updates cart count
## Framework Features
- Session-scoped auth fixture: login runs once per test session, token reused across all API tests
- Module-scoped UI login fixture: browser state saved to disk after first login, loaded for subsequent UI tests without repeating the login flow
- Page Object Model: UI tests interact with page objects rather than raw locators, isolating locator changes to a single location
- Test data management: test payloads stored in test_data/users.json with named data sets per scenario, loaded via utils/data_loader.py
- Parametrized negative tests across auth and API layers
- JWT decoder utility for asserting token claims without external libraries
- HTML test reporting: self-contained reports generated locally after every run and uploaded as CI artifacts
## Project Structure
- api_client/ - API clients for auth and users endpoints
- config/ - environment-based configuration (base URL, credentials)
- pages/ - page object classes for UI test interactions
- test_data/ - JSON test data files with named data sets per scenario
- tests/ - tests and fixtures
- utils/ - validators, response helpers, data loader
## Installation and Setup
 
1. Clone the repository:
   git clone https://github.com/donprather-ctrl/api-test-framework.git
   cd api-test-framework
2. Create and activate a virtual environment:
   py -m venv venv
   venv\Scripts\Activate.ps1
3. Install dependencies:
   py -m pip install -r requirements.txt
4. Install Playwright browsers:
   py -m playwright install
5. Create a .env file using .env.example as a template:
   cp .env.example .env
   Then open .env and add your credentials.
## Running the Tests
 
Run the full suite:
   py -m pytest -v
 
Run smoke tests only:
   py -m pytest -m smoke -v
 
Run regression suite:
   py -m pytest -m regression -v
 
Run API tests only:
   py -m pytest -m api -v
 
Run UI tests only:
   py -m pytest -m ui -v
 
A self-contained HTML report is saved to reports/report.html after every run.
 
## Author
Don Prather
don.prather@protonmail.com
http://www.linkedin.com/in/donprather
