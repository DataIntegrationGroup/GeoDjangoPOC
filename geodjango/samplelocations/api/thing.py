from ninja import Router
from samplelocations.models import Thing, Location, Location_Thing_Junction
from samplelocations.schemas import FeatureCollection, NotFoundSchema, WellProperties, SpringProperties
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import HttpResponse
from typing import List, Tuple

router = Router()

def get_things(thing_id: int | None = None) -> List[Thing]:
    """
    Retrieve all things or a specific thing by ID.
    """
    if thing_id is None:
        return Thing.objects.all()
    else:
        # If a specific thing ID is provided, return that thing:
        return [Thing.objects.filter(thing_id__in=[thing_id]).first()]
    
def construct_feature_collection(things: List[Thing]) -> FeatureCollection:
    """
    Construct a GeoJSON FeatureCollection from a list of Thing objects.
    """
    """
    Jacob's notes during development: 2025-07-28
    A disadvantage of Django ORM is that you can't make more complicated queries.
    From what I understand, you can use Django ORM to get all the things and their related locations,
    but you can't easily filter or join them in a single query. The "joining" has to be done in
    Python code after fetching the data, which can be less efficient because it's slower than
    SQL and you have to make more SQL queries to get the related data.

    Also, the filtering is kind of confusing...
    """
    thing_ids = [thing.thing_id for thing in things]
    location_thing_junctions = Location_Thing_Junction.objects.filter(thing_id__in=thing_ids)
    location_ids = [junction.location_id.location_id for junction in location_thing_junctions]
    locations = Location.objects.filter(location_id__in=location_ids)

    features = []
    for thing in things:
        thing_dict = model_to_dict(thing)
        thing_dict["location_id"] = thing_dict["location_id"][0].location_id
        thing_dict["date_created"] = thing.date_created.isoformat()
        thing_dict["thing_type"] = thing.get_thing_type_display()  # Get human-readable type
        if thing.thing_type == "W":
            thing_properties = WellProperties(**thing_dict)
        elif thing.thing_type == "S":
            thing_properties = SpringProperties(**thing_dict)

        locations = thing.location_id.all()

        # TODO: assuming, for now, that each thing has a single location. this will have to change if we allow multiple locations per thing.
        location = locations[0]

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [location.coordinate.x, location.coordinate.y, location.coordinate.z],
            },
            "properties": thing_properties.dict(),
        }

        features.append(feature)

    response = FeatureCollection(
        type="FeatureCollection",
        features=features
    )

    return response

@router.get('')
def get_all_things(request):
    """
    List all things.
    """
    things = get_things()
    response = construct_feature_collection(things)
    return response

@router.get('/{thing_id}', response={200: FeatureCollection, 404: NotFoundSchema})
def get_thing_by_id(request, thing_id: int):
    """
    Retrieve a specific thing by its ID.
    """
    thing = get_things(thing_id=thing_id)
    if thing == [None]:
        return 404, {"detail": f"Thing with id {thing_id} not found"}
    response = construct_feature_collection(thing)
    return response