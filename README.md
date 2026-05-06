![Tests](https://github.com/donprather-ctrl/api-test-framework/actions/workflows/tests.yml/badge.svg)
README

## Project Description:

A test automation framework built with Python, Pytest, and Playwright, 
covering API testing, UI testing, and end-to-end workflows against 
the FakeStoreAPI.

## Technology Stack

Python, Pytest, Playwright, FakeStoreAPI (fakestoreapi.com)

## CI/CD

This project uses GitHub Actions to run the smoke test suite automatically 
on every push and pull request.

- Smoke tests run on every push to any branch
- Full regression suite runs on merges to main
- Test results are uploaded as artifacts after every run

FakeStoreAPI - as of 5/5/2026 - was blocking requests from GitHub Actions IP ranges. To demonstrate CI/CD integration with automated tests, the API tests run against mocked
HTTP responses (in CI only, not when running locally) using the responses library, and against 
the real API locally. UI tests run against saucedemo.com which is reasonably CI-friendly.

## Test coverage

**Authentication**
- Valid login returns a token
- Invalid credentials do not return a token

**Products API**
- Get all products
- Get product by ID (valid ID, invalid type, out-of-range ID)
- Create product
- Update product
- Delete product
- End-to-end product lifecycle: Create → Get → Update → Get → Delete

**UI (saucedemo.com)**
- Valid login navigates to products page
- Invalid login displays error message
- Add product to cart updates cart count


## Project Structure: 

- \api_client - API clients to connect and interact with the auth and product APIs (OpenAPI docs are available at fakestoreapi.com/docs)
- \config - Base configurations (Service URLs, pointers to default user/password and to test data JSON files)
- \tests - Tests and test fixtures
- \utils - Helper files including a data loader, validation helpers, and response helpers. 

## Known limitations

**FakeStoreAPI CI compatibility:** FakeStoreAPI inconsistently blocks requests from GitHub 
Actions IP ranges. API tests use the responses library to mock HTTP calls 
in CI, ensuring full test coverage without external dependencies. All tests 
run against the real API locally.

**FakeStoreAPI GET inconsistency:** GET requests following POST operations 
generally return an empty response body. Affected steps in the E2E workflow 
test handle this gracefully — the test continues and validates all write 
operations regardless.


## Installation and setup

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

5. Create a .env file in the project root using .env.example as a template:
   cp .env.example .env
   Then open .env and add your credentials.

## Running the tests

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

##Author

Don Prather
don.prather@protonmail.com
http://www.linkedin.com/in/donprather
