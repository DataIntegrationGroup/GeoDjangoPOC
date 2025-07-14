from ninja import Router
from .models import Location

router = Router()

@router.get('')
def list_locations(request):
    """
    List all locations.
    """
    locations = Location.objects.all()
    return [
        {
            'id': loc.location_id,
            'name': loc.name,
            'coordinates': loc.coordinate,
            'date_created': loc.date_created.isoformat(),
        }
        for loc in locations
    ]
