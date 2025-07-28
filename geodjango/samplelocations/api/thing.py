from ninja import Router
from samplelocations.models import SampleLocation, Owner
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404

router = Router()

@router.get('')
def get_things(request):
    """
    List all things.
    """
    things = Thing.objects.all()
    return [
        {
            'id': thing.id,
            'name': thing.name,
            'release_status': thing.release_status,
            'date_created': thing.date_created.isoformat(),
        }
        for thing in things
    ]

@router.post("")
def post_thing(request, name: str, release_status: bool, owner_id: int):
    owner = get_object_or_404(Owner, id=owner_id)
    thing = Thing.objects.create(
        name=name,
        release_status=release_status,
        owner=owner
    )
    return {"id": thing.id, "name": thing.name}