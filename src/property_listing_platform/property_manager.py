import uuid
from datetime import datetime

class Property:
    def __init__(self, property_id: str, user_id: str, details: dict):
        """
        Initialize property with:
        - Basic details (location, price, type)
        - Status (available/sold)
        - Timestamp
        """
        self.property_id = property_id
        self.user_id = user_id
        self.details = details
        self.status = "available"  # Default status
        self.timestamp = datetime.now()

    def update_status(self, new_status: str):
        """Update the property status."""
        self.status = new_status

    def __repr__(self):
        """String representation of the property."""
        return f"Property({self.property_id}, {self.user_id}, {self.details}, {self.status})"


class PropertyManager:
    def __init__(self):
        """
        Initialize data structures for:
        - Property storage
        - User portfolios
        - Search indices
        """
        self.properties = {}  # Maps property_id to Property object
        self.user_portfolios = {}  # Maps user_id to list of property_ids
        self.price_index = []  # Sorted list of (price, property_id)
        self.location_index = {}  # Maps location to list of property_ids
        self.status_index = {"available": set(), "sold": set()}  # Status-based index

    def add_property(self, user_id: str, property_details: dict) -> str:
        """
        Add new property listing:
        - Validate details
        - Generate unique ID
        - Update indices
        Returns:
            property_id: str
        """
        # Generate unique ID for the property
        property_id = str(uuid.uuid4())
        property_obj = Property(property_id, user_id, property_details)

        # Store property in the database
        self.properties[property_id] = property_obj

        # Update user portfolio
        if user_id not in self.user_portfolios:
            self.user_portfolios[user_id] = []
        self.user_portfolios[user_id].append(property_id)

        # Update indices
        self.price_index.append((property_details["price"], property_id))
        self.price_index.sort()  # Keep it sorted for binary search
        location = property_details["location"]
        if location not in self.location_index:
            self.location_index[location] = []
        self.location_index[location].append(property_id)
        self.status_index["available"].add(property_id)

        return property_id

    def update_property_status(self, property_id: str, status: str, user_id: str) -> bool:
        """
        Update property status:
        - Verify ownership
        - Update status
        - Handle search index updates
        """
        # Check if property exists
        if property_id not in self.properties:
            return False

        property_obj = self.properties[property_id]

        # Verify ownership
        if property_obj.user_id != user_id:
            return False

        # Update status
        old_status = property_obj.status
        property_obj.update_status(status)

        # Update status index
        self.status_index[old_status].remove(property_id)
        self.status_index[status].add(property_id)

        return True

    def get_user_properties(self, user_id: str) -> list[Property]:
        """
        Retrieve all properties for a user:
        - Filter by status
        - Sort by date
        """
        if user_id not in self.user_portfolios:
            return []

        # Retrieve properties and sort by timestamp
        user_property_ids = self.user_portfolios[user_id]
        user_properties = [self.properties[prop_id] for prop_id in user_property_ids]
        return sorted(user_properties, key=lambda x: x.timestamp, reverse=True)


# Example usage
if __name__ == "__main__":
    manager = PropertyManager()

    # Add properties
    user_id = "user_123"
    prop1_details = {"location": "New York", "price": 500000, "type": "Apartment"}
    prop2_details = {"location": "San Francisco", "price": 1200000, "type": "House"}
    property_id1 = manager.add_property(user_id, prop1_details)
    property_id2 = manager.add_property(user_id, prop2_details)

    print(f"Added Properties: {manager.properties} \n")

    # Update status
    manager.update_property_status(property_id1, "sold", user_id)
    print(f"Updated Properties: {manager.properties} \n")

    # Get user properties
    user_properties = manager.get_user_properties(user_id)
    print(f"User Properties: {user_properties}")
