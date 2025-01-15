import pytest
from property_listing_platform.property_manager import PropertyManager, Property


@pytest.fixture
def setup_manager():
    """Fixture to set up PropertyManager instance and sample data."""
    manager = PropertyManager()
    user_id = "user_123"
    prop1_details = {"location": "New York", "price": 500000, "type": "Apartment"}
    prop2_details = {"location": "San Francisco", "price": 1200000, "type": "House"}
    return manager, user_id, prop1_details, prop2_details


def test_add_property(setup_manager):
    """Test adding properties."""
    manager, user_id, prop1_details, prop2_details = setup_manager
    property_id1 = manager.add_property(user_id, prop1_details)
    property_id2 = manager.add_property(user_id, prop2_details)

    # Assert properties are added
    assert property_id1 in manager.properties
    assert property_id2 in manager.properties

    # Assert user portfolio is updated
    assert len(manager.user_portfolios[user_id]) == 2

    # Assert indices are updated
    assert len(manager.price_index) == 2
    assert property_id1 in manager.location_index["New York"]
    assert property_id2 in manager.location_index["San Francisco"]
    assert property_id1 in manager.status_index["available"]
    assert property_id2 in manager.status_index["available"]


def test_update_property_status(setup_manager):
    """Test updating property status."""
    manager, user_id, prop1_details, _ = setup_manager
    property_id = manager.add_property(user_id, prop1_details)

    # Update status to "sold"
    result = manager.update_property_status(property_id, "sold", user_id)
    assert result

    # Verify status update
    property_obj = manager.properties[property_id]
    assert property_obj.status == "sold"
    assert property_id not in manager.status_index["available"]
    assert property_id in manager.status_index["sold"]


def test_update_property_status_invalid_user(setup_manager):
    """Test updating property status with invalid user."""
    manager, user_id, prop1_details, _ = setup_manager
    property_id = manager.add_property(user_id, prop1_details)

    # Attempt status update with incorrect user
    result = manager.update_property_status(property_id, "sold", "invalid_user")
    assert not result

    # Verify status remains unchanged
    property_obj = manager.properties[property_id]
    assert property_obj.status == "available"


def test_get_user_properties(setup_manager):
    """Test retrieving properties for a user."""
    manager, user_id, prop1_details, prop2_details = setup_manager
    property_id1 = manager.add_property(user_id, prop1_details)
    property_id2 = manager.add_property(user_id, prop2_details)

    # Retrieve user properties
    user_properties = manager.get_user_properties(user_id)

    # Assert correct properties are retrieved and sorted by timestamp
    assert len(user_properties) == 2
    assert user_properties[0].property_id == property_id2
    assert user_properties[1].property_id == property_id1


def test_get_user_properties_no_properties(setup_manager):
    """Test retrieving properties for a user with no properties."""
    manager, _, _, _ = setup_manager
    user_properties = manager.get_user_properties("nonexistent_user")
    assert user_properties == []


def test_add_property_updates_indices(setup_manager):
    """Test that adding a property updates all relevant indices."""
    manager, user_id, prop1_details, _ = setup_manager
    property_id = manager.add_property(user_id, prop1_details)

    # Verify location index
    assert property_id in manager.location_index["New York"]

    # Verify status index
    assert property_id in manager.status_index["available"]

    # Verify price index is sorted
    assert manager.price_index[0][0] == 500000
