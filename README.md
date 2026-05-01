README

## Project Description:

A test automation framework built with Python, Pytest, and Playwright, 
covering API testing, UI testing, and end-to-end workflows against 
the FakeStoreAPI.

## Technology Stack

Python, Pytest, Playwright, FakeStoreAPI (fakestoreapi.com)

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

**UI**
- Search functionality on dragracecentral.com


## Project Structure: 

\api_client - API clients to connect and interact with the auth and product APIs (OpenAPI docs are available at fakestoreapi.com/docs)
\config - Base configurations (Service URLs, pointers to default user/password and to test data JSON files)
\tests - Tests and test fixtures
\utils - Helper files including a data loader, validation helpers, and response helpers. 

## Known Limitations

FakeStoreAPI is a mock API that occasionally returns an empty response 
body on GET requests following a POST. Affected tests use pytest.skip() 
to handle this gracefully rather than asserting against unreliable behavior.


## Installation and setup

1. Clone the repository:
   git clone https://github.com/donprather-ctrl/api-test-framework.git
   cd api-test-framework

2. Install dependencies:
   py -m pip install -r requirements.txt

3. Install Playwright browsers:
   py -m playwright install

4. Create a .env file in the project root using .env.example as a template:
   cp .env.example .env
   Then open .env and add your credentials.

## Running the tests

Run the full test suite:
   py -m pytest tests/ -v

Run API tests only:
   py -m pytest tests/test_products_api.py tests/test_auth_api.py -v

Run UI tests only:
   py -m pytest tests/tst_ui_interaction.py -v

##Author

Don Prather
don.prather@protonmail.com
http://www.linkedin.com/in/donprather
