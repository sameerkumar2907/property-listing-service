from fastapi import FastAPI, HTTPException, Depends, Query
from property_listing_platform.property_manager import PropertyManager
from property_listing_platform.property_search import PropertySearch
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import uuid4

app = FastAPI()

property_manager = None  # Placeholder for the shared PropertyManager instance
search_system = None  # Placeholder for the shared PropertySearch instance

# Dependency for current user (mock implementation)
def get_current_user():
    return "user_123"  # Mocked user ID

# Pydantic models for input validation
class PropertyCreate(BaseModel):
    location: str
    price: float = Field(gt=0, description="Price must be greater than 0")
    property_type: str
    description: Optional[str] = None
    amenities: Optional[List[str]] = []

# API endpoints
@app.post("/api/v1/properties")
async def create_property(
    property_data: PropertyCreate,
    current_user: str = Depends(get_current_user)
):
    """
    Create new property listing:
    1. Validate input
    2. Create property
    3. Update indices
    """
    global property_manager

    if not property_manager:
        raise HTTPException(status_code=500, detail="Property manager not initialized")

    # Call the PropertyManager to add the property
    property_id = property_manager.add_property(
        user_id=current_user, 
        property_details=property_data.dict()
    )

    return {"message": "Property created successfully", "property_id": property_id}

@app.get("/api/v1/properties/search")
async def search_properties(
    min_price: Optional[float] = Query(None, gt=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, gt=0, description="Maximum price filter"),
    location: Optional[str] = None,
    property_type: Optional[str] = None,
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Number of results per page")
):
    """
    Search properties with:
    - Price range filter
    - Location filter
    - Type filter
    - Pagination
    """
    global search_system

    if not search_system:
        raise HTTPException(status_code=500, detail="Search system not initialized")

    # Construct search criteria
    criteria = {
        "price_range": (min_price, max_price),
        "location": location,
        "property_type": property_type,
        "page": page,
        "per_page": limit
    }

    # Perform the search
    try:
        results = search_system.search_properties(criteria)
        return {
            "page": page,
            "limit": limit,
            "total_results": len(results),
            "properties": [vars(prop) for prop in results]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during search: {str(e)}")


# App initialization
@app.on_event("startup")
async def setup():
    """
    Initialize the PropertyManager and PropertySearch instances.
    """
    global property_manager, search_system
    # Create shared instances
    property_manager = PropertyManager()
    search_system = PropertySearch(property_manager)

    search_system.set_properties_reference(property_manager.properties)
