import pytest
from fastapi.testclient import TestClient
from property_listing_platform.main import app, setup

# Create a test client for the FastAPI app
client = TestClient(app)

# Mock data for testing
property_data = {
    "location": "New York",
    "price": 1200000.0,
    "property_type": "apartment",
    "description": "A beautiful apartment",
    "amenities": ["gym", "pool"]
}


@pytest.fixture(scope="module", autouse=True)
def initialize_app():
    """
    Run the startup event before tests to initialize shared instances.
    """
    import asyncio
    asyncio.run(setup())


def test_create_property_success():
    """
    Test the /api/v1/properties endpoint for successfully creating a property.
    """
    response = client.post("/api/v1/properties", json=property_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Property created successfully"
    assert "property_id" in response_data


def test_create_property_invalid_price():
    """
    Test the /api/v1/properties endpoint for validation failure on invalid price.
    """
    invalid_data = property_data.copy()
    invalid_data["price"] = -500  # Invalid price
    response = client.post("/api/v1/properties", json=invalid_data)
    assert response.status_code == 422  # Validation error
    assert "Input should be greater than 0" in response.text


def test_search_properties_success():
    """
    Test the /api/v1/properties/search endpoint for a successful search.
    """
    # Add a property first
    client.post("/api/v1/properties", json=property_data)

    # Perform a search with filters
    params = {
        "min_price": 1000000,
        "max_price": 1500000,
        "location": "New York",
        "property_type": "apartment",
        "page": 1,
        "limit": 10
    }
    response = client.get("/api/v1/properties/search", params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["page"] == 1
    assert response_data["limit"] == 10
    assert response_data["total_results"] >= 1
    assert response_data["properties"][0]["details"]["location"] == "New York"


def test_search_properties_no_results():
    """
    Test the /api/v1/properties/search endpoint when no results match.
    """
    params = {
        "min_price": 5000000,  # Price range with no match
        "max_price": 6000000,
        "location": "Nonexistent City",
        "property_type": "villa",
        "page": 1,
        "limit": 10
    }
    response = client.get("/api/v1/properties/search", params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["total_results"] == 0
    assert response_data["properties"] == []


def test_search_properties_invalid_pagination():
    """
    Test the /api/v1/properties/search endpoint with invalid pagination parameters.
    """
    params = {
        "page": 0,  # Invalid page number
        "limit": 200  # Invalid limit
    }
    response = client.get("/api/v1/properties/search", params=params)
    assert response.status_code == 422  # Validation error
    assert "Input should be greater than or equal to 1" in response.text
