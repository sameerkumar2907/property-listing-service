from bisect import bisect_left, bisect_right
from property_listing_platform.property_manager import Property, PropertyManager

class PropertySearch:
    def __init__(self, manager: PropertyManager):
        """
        Initialize search system:
        - Price indices
        - Location indices
        - Status tracking
        - User shortlists
        """
        self.manager = manager
        self.user_shortlists = {}  # Maps user_id to list of shortlisted property_ids

    def set_properties_reference(self, properties):
        """Set a reference to the shared property storage."""
        self.properties = properties

    def search_properties(self, criteria: dict) -> list[Property]:
        """
        Search properties based on:
        - Price range
        - Location
        - Property type
        - Status (available only)
        
        Handle:
        - Multiple filters
        - Sorting
        - Pagination
        """
        price_range = criteria.get("price_range", (None, None))
        location = criteria.get("location", None)
        property_type = criteria.get("property_type", None)
        status = "available"  # Search only for available properties

        location_index = self.manager.location_index
        status_index = self.manager.status_index
        price_index = self.manager.price_index
        result = set(status_index["available"])

        # Filter by price range
        if result and (price_range[0] is not None or price_range[1] is not None):
            min_price = price_range[0] if price_range[0] is not None else float('-inf')
            max_price = price_range[1] if price_range[1] is not None else float('inf')

            # Perform binary search to find the range of indices
            start_idx = bisect_left(price_index, (min_price,))
            end_idx = bisect_right(price_index, (max_price,))

            # Extract the property IDs for properties within the price range
            price_results = [property_id for _, property_id in price_index[start_idx:end_idx]]

            # Intersect with the existing result set
            result = set(result).intersection(price_results)

        # Filter by location
        if result and location:
            location_results = set(location_index.get(location, []))
            result = set(result).intersection(location_results)

        # Filter by property type
        if result and property_type:
            type_results = {
                prop_id for prop_id in status_index[status]
                if self.properties[prop_id].details["property_type"] == property_type
            }
            result = set(result).intersection(type_results)

        # Ensure the result is a list of Property objects
        result_properties = [self.properties[prop_id] for prop_id in result]

        # Sort results by price
        result_properties.sort(key=lambda x: x.details["price"])

        # Pagination
        page = criteria.get("page", 1)
        per_page = criteria.get("per_page", 10)
        start = (page - 1) * per_page
        end = start + per_page

        return result_properties[start:end]

    def shortlist_property(self, user_id: str, property_id: str) -> bool:
        """
        Add property to user's shortlist:
        - Verify property exists
        - Check if already shortlisted
        - Update user's shortlist
        """
        # Check if property exists
        if property_id not in self.properties:
            return False

        # Initialize shortlist for user if not already present
        if user_id not in self.user_shortlists:
            self.user_shortlists[user_id] = []

        # Check if already shortlisted
        if property_id in self.user_shortlists[user_id]:
            return False

        # Add to shortlist
        self.user_shortlists[user_id].append(property_id)
        return True

    def get_shortlisted(self, user_id: str) -> list[Property]:
        """
        Get user's shortlisted properties:
        - Filter out sold properties
        - Sort by shortlist date
        """
        if user_id not in self.user_shortlists:
            return []

        # Filter out sold properties
        shortlisted_ids = self.user_shortlists[user_id]
        result = [
            self.properties[prop_id]
            for prop_id in shortlisted_ids
            if self.properties[prop_id].status == "available"
        ]

        # No explicit sort needed since they are already sorted by addition order
        return result


# Example usage
if __name__ == "__main__":
    # PropertyManager manages the properties
    manager = PropertyManager()

    # Add properties
    user_id = "user_123"
    prop1_details = {"location": "New York", "price": 500000, "property_type": "Apartment"}
    prop2_details = {"location": "San Francisco", "price": 1200000, "property_type": "House"}
    property_id1 = manager.add_property(user_id, prop1_details)
    property_id2 = manager.add_property(user_id, prop2_details)

    # Initialize search system and share the properties reference
    search = PropertySearch(manager)
    search.set_properties_reference(manager.properties)

    # Search properties
    criteria = {"price_range": (400000, 1000000), "location": "New York", "property_type": "Apartment"}
    search_results = search.search_properties(criteria)
    print(f"Search Results: {search_results} \n")

    # Shortlist property
    is_shortlisted = search.shortlist_property(user_id, property_id1)
    print(f"Shortlisted: {is_shortlisted} \n")

    # Get shortlisted properties
    shortlisted_properties = search.get_shortlisted(user_id)
    print(f"Shortlisted Properties: {shortlisted_properties}")
