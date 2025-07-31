from ninja import Router
from samplelocations.models import Location
from samplelocations.schemas import LocationSchema, NotFoundSchema
from typing import List

router = Router()   

@router.get("")
def get_locations(request) -> List[LocationSchema]:
    """
    List all sample locations.
    """    
    locations = Location.objects.all()

    response = [
        {
            "location_id": location.location_id,
            "coordinates": f"POINT({location.coordinate.x} {location.coordinate.y} {location.coordinate.z})",
            "date_created": location.date_created.isoformat(),
        }
        for location in locations
    ]

    return response

@router.get("/{location_id}", response={200: LocationSchema, 404: NotFoundSchema})
def get_location_by_id(request, location_id: int):
    locations = Location.objects.filter(location_id=location_id)
    if not locations.exists():
        return 404, {"detail": f"Location with location_id {location_id} not found"}

    location = locations.first()
    response = {
        "location_id": location.location_id,
        "coordinates": f"POINT({location.coordinate.x} {location.coordinate.y} {location.coordinate.z})",
        "date_created": location.date_created.isoformat(),
    }
    return response