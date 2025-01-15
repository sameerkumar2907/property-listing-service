import pytest
from property_listing_platform.property_manager import Property, PropertyManager
from property_listing_platform.property_search import PropertySearch

@pytest.fixture
def setup_property_manager():
    # Create a PropertyManager and add some properties
    manager = PropertyManager()

    prop1_details = {"location": "New York", "price": 500000, "property_type": "Apartment"}
    prop2_details = {"location": "San Francisco", "price": 1200000, "property_type": "House"}
    prop3_details = {"location": "New York", "price": 700000, "property_type": "Apartment"}
    
    property_id1 = manager.add_property("user_123", prop1_details)
    property_id2 = manager.add_property("user_123", prop2_details)
    property_id3 = manager.add_property("user_123", prop3_details)
    
    search = PropertySearch(manager)
    search.set_properties_reference(manager.properties)
    
    return search, manager, property_id1, property_id2, property_id3


def test_search_properties_price_range(setup_property_manager):
    search, manager, _, _, _ = setup_property_manager
    
    criteria = {"price_range": (400000, 1000000)}
    search_results = search.search_properties(criteria)
    
    # Check that only properties within the price range are returned
    assert len(search_results) == 2
    assert search_results[0].details["price"] <= 1000000
    assert search_results[1].details["price"] <= 1000000


def test_search_properties_location(setup_property_manager):
    search, manager, _, _, _ = setup_property_manager
    
    criteria = {"location": "New York"}
    search_results = search.search_properties(criteria)
    
    # Check that only properties in New York are returned
    assert len(search_results) == 2
    assert all(prop.details["location"] == "New York" for prop in search_results)


def test_search_properties_property_type(setup_property_manager):
    search, manager, _, _, _ = setup_property_manager
    
    criteria = {"property_type": "Apartment"}
    search_results = search.search_properties(criteria)
    
    # Check that only Apartment properties are returned
    assert len(search_results) == 2
    assert all(prop.details["property_type"] == "Apartment" for prop in search_results)


def test_search_properties_pagination(setup_property_manager):
    search, manager, _, _, _ = setup_property_manager
    
    criteria = {"page": 1, "per_page": 1, "price_range": (0, 1000000)}
    search_results = search.search_properties(criteria)
    
    # Check that the number of results is as per pagination
    assert len(search_results) == 1
    assert search_results[0].details["price"] <= 1000000


def test_shortlist_property(setup_property_manager):
    search, manager, property_id1, _, _ = setup_property_manager
    
    user_id = "user_123"
    
    # Test adding a property to the shortlist
    result = search.shortlist_property(user_id, property_id1)
    assert result is True
    
    # Test adding the same property again, it should not be added
    result = search.shortlist_property(user_id, property_id1)
    assert result is False
    
    # Test adding a non-existent property
    result = search.shortlist_property(user_id, "non_existent_property")
    assert result is False


def test_get_shortlisted_properties(setup_property_manager):
    search, manager, property_id1, property_id2, _ = setup_property_manager
    
    user_id = "user_123"
    
    # Add properties to the shortlist
    search.shortlist_property(user_id, property_id1)
    search.shortlist_property(user_id, property_id2)
    
    # Test fetching shortlisted properties
    shortlisted_properties = search.get_shortlisted(user_id)
    assert len(shortlisted_properties) == 2
    assert all(prop.status == "available" for prop in shortlisted_properties)
