# Property Listing Platform

This is a FastAPI-based Property Listing Platform designed to manage property data, provide search functionality, and manage various aspects related to property listings.

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
├── tests/                            # Unit and integration tests
│   ├── __init__.py
│   ├── test_main.py                  # Tests for main FastAPI app
│   └── test_property_manager.py      # Tests for property manager module
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Files to be ignored by Git
└── README.md                         # This file
