from ninja import Router, Schema
from samplelocations.models import Thing, Location, Location_Thing_Junction
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from typing import List

router = Router()


class GeoJSONGeometry(Schema):
    """
    Geometry schema for GeoJSON response.
    """

    type: str  # e.g., "Point", "LineString", "Polygon"
    coordinates: (
        List[float] | List[List[float]] | List[List[List[float]]]
    )  # Supports Point, LineString, Polygon, etc.

class Feature(Schema):
    type: str = "Feature"
    geometry: GeoJSONGeometry

class BaseProperties(Schema):
    thing_id: int
    name: str
    thing_type: str
    release_status: bool
    date_created: str
    description: str | None = None


class WellProperties(BaseProperties):
    well_depth_ft: float | None = None
    hole_depth_ft: float | None = None
    casing_diameter_ft: float | None = None
    casing_depth_ft: float | None = None
    casing_description: str | None = None
    construction_notes: str | None = None

class SpringProperties(BaseProperties):
    spring_type: str | None = None

class WellFeature(Feature):
    properties: WellProperties

class SpringFeature(Feature):
    properties: SpringProperties

class FeatureCollection(Schema):
    type: str = "FeatureCollection"
    features: List[WellFeature | SpringFeature] = []


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
    location_thing_junctions = Location_Thing_Junction.objects.filter(thing_id__in=things.values_list('thing_id', flat=True))
    locations = Location.objects.filter(location_id__in=location_thing_junctions.values_list('location_id', flat=True))

    features = []
    for thing in things:
        if thing.thing_type == "well":
            thing_properties = WellProperties(**thing)
        elif thing.thing_type == "spring":
            thing_properties = SpringProperties(**thing)

        thing_id = thing.thing_id
        location_ids = [junction.location_id for junction in location_thing_junctions if junction.thing_id == thing_id]
        locations = [loc for loc in locations if loc.location_id in location_ids]

        # assuming, for now, that each thing has a single location
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
    """
    Jacob's notes during development: 2025-07-28
    A disadvantage of Django ORM is that you can't make more complicated queries.
    From what I understand, you can use Django ORM to get all the things and their related locations,
    but you can't easily filter or join them in a single query. The "joining" has to be done in
    Python code after fetching the data, which can be less efficient because it's slower than
    SQL and you have to make more SQL queries to get the related data.

    Also, the filtering is kind of confusing...
    """
    things = get_things()
    response = construct_feature_collection(things)
    return response

@router.get('/{thing_id}')
def get_thing_by_id(request, thing_id: int):
    """
    Retrieve a specific thing by its ID.
    """
    thing = get_things(thing_id=thing_id)
    if thing == []:
        return {"detail": f"Thing with id {thing_id} not found"}, 404
    response = construct_feature_collection(thing)
    return response