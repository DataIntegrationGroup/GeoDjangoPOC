from ninja import Schema
from typing import List

# ========== General Schemas ==========

class NotFoundSchema(Schema):
    detail: str

class GeoJSONGeometry(Schema):
    """
    Geometry schema for GeoJSON response.
    """

    type: str  # e.g., "Point", "LineString", "Polygon"
    coordinates: (
        List[float] | List[List[float]] | List[List[List[float]]]
    )  # Supports Point, LineString, Polygon, etc.


# ========== Thing Schemas ==========

class Feature(Schema):
    type: str = "Feature"
    geometry: GeoJSONGeometry

class BaseProperties(Schema):
    thing_id: int
    name: str
    thing_type: str
    release_status: bool
    date_created: str


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
    features: List = [] # can be WellFeature or SpringFeature. Specifying a union of both types makes the schema include unrelated fields, which is not desired.

# ========== Location Schemas ==========

class LocationSchema(Schema):
    location_id: int
    coordinates: str
    date_created: str