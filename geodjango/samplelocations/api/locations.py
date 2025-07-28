# from ninja import Router
# from samplelocations.models import Location, Owner
# from django.contrib.gis.geos import Point
# from django.shortcuts import get_object_or_404

# router = Router()

# @router.get('')
# def get_locations(request):
#     """
#     List all sample locations.
#     """    
#     locations = SampleLocation.objects.all()
#     return [
#         {
#             'id': loc.id,
#             'name': loc.name,
#             'lat': loc.point.y,
#             'lon': loc.point.x,
#             'description': loc.description,
#             'visible': loc.visible,
#             'date_created': loc.date_created.isoformat(),
#         }
#         for loc in locations
#     ]

# @router.post("")
# def post_location(request, name: str, lat: float, lon: float, owner_id: int, description: str = None, visible: bool = False):
#     owner = get_object_or_404(Owner, id=owner_id)
#     point = Point(lon, lat)
#     location = SampleLocation.objects.create(
#         name=name,
#         description=description,
#         visible=visible,
#         point=point,
#         owner=owner
#     )
#     return {"id": location.id, "name": location.name}