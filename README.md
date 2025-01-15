# Property Listing Service

This is a FastAPI-based Property Listing Service designed to manage property data, provide search functionality, and manage various aspects related to property listings.

## Project Structure

The project follows a clean architecture and organized folder structure. Here’s an overview of the directory layout:

```bash
property-listing-platform/
├── .venv/                           # Virtual environment directory
├── src/                              # Source code directory
│   └── property_listing_platform/    # Application code
│       ├── __init__.py
│       ├── main.py                   # FastAPI app and entry point
│       ├── property_manager.py       # Logic for managing property data
│       └── property_search.py        # Logic for property search functionality
├── tests/                            # Unit tests
│   ├── test_main.py                  # Tests for main FastAPI app
├── ├── test_property_service.py      # Tests for property search module
│   └── test_property_manager.py      # Tests for property manager module
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Files to be ignored by Git
└── README.md                         # This file
```

## Setup
### 1. Clone the Repository
Clone the repository to your local machine:

```bash
git clone https://github.com/sameerkumar2907/property-listing-service.git
cd property-listing-service
```

### 2. Create a Virtual Environment
Create a virtual environment to manage your dependencies:

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment
On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies
Install the required dependencies listed in the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 5. Set the PYTHONPATH
To ensure that the src folder is recognized as the root for imports, set the PYTHONPATH:

```bash
export PYTHONPATH=src
```

### 6. Run the Application
Run the FastAPI application using uvicorn:

```bash
uvicorn property_listing_platform.main:app --reload
```

Your app should now be available at http://127.0.0.1:8000  
For example, to list the available properties, visit:
http://127.0.0.1:8000/api/v1/properties/search


### 7. Run Tests
You can run the tests using pytest:

```bash
pytest
```

Or to run a specific test file:

```bash
pytest tests/test_main.py
```
