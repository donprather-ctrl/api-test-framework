![Tests](https://github.com/donprather-ctrl/api-test-framework/actions/workflows/tests.yml/badge.svg)

## Project Description
A test automation framework built with Python, Pytest, and Playwright,
covering API testing, UI testing, and end-to-end workflows.

## Technology Stack
Python, Pytest, Playwright, dummyjson (dummyjson.com), saucedemo.com, GitHub Actions

## CI/CD
This project uses GitHub Actions with two jobs that run automatically
on every push and pull request.

- **Smoke** - runs on every push to any branch; fast critical-path tests
- **Regression** - runs only if smoke passes; full scenario coverage including
  edge cases and end-to-end workflows
- Test results are uploaded as artifacts after every run

## Test Coverage

**Authentication (dummyjson)**
- Valid credentials return 200 and an access token
- Invalid credentials never return a token (6 parametrized scenarios:
  wrong username, wrong password, both wrong, empty username,
  empty password, both empty)

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

## Project Structure
- api_client/ - API clients for auth and users endpoints
- config/ - environment-based configuration (base URL, credentials)
- tests/ - tests and fixtures
- utils/ - validators, response helpers

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

## Author
Don Prather
don.prather@protonmail.com
http://www.linkedin.com/in/donprather
