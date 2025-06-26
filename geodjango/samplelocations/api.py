from ninja import Router
from .models import SampleLocation

router = Router()

@router.get('')
def list_samplelocations(request):
    """
    List all sample locations.
    """
    locations = SampleLocation.objects.all()
    return [
        {
            'id': loc.id,
            'name': loc.name,
            'lat': loc.point.y,
            'lon': loc.point.x,
            'description': loc.description,
            'visible': loc.visible,
            'date_created': loc.date_created.isoformat(),
        }
        for loc in locations
    ]
