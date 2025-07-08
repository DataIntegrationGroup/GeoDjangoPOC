from ninja import Router
from ..models import SampleLocation, Well, WellScreen, Lexicon
from django.shortcuts import get_object_or_404

router = Router()


@router.post("")
def post_well(
    request,
    location_id: int,
    ose_pod_id: str = None,
    api_id: str = "",
    usgs_id: str = None,
    well_depth: float = None,
    hole_depth: float = None,
    well_type_id: int = None,
    casing_diameter: float = None,
    casing_depth: float = None,
    casing_description: str = None,
    construction_notes: str = None,
    formation_zone_id: int = None
):
    location = get_object_or_404(SampleLocation, id=location_id)
    well_type = Lexicon.objects.filter(id=well_type_id).first() if well_type_id else None
    formation_zone = Lexicon.objects.filter(id=formation_zone_id).first() if formation_zone_id else None
    well = Well.objects.create(
        location=location,
        ose_pod_id=ose_pod_id,
        api_id=api_id,
        usgs_id=usgs_id,
        well_depth=well_depth,
        hole_depth=hole_depth,
        well_type=well_type,
        casing_diameter=casing_diameter,
        casing_depth=casing_depth,
        casing_description=casing_description,
        construction_notes=construction_notes,
        formation_zone=formation_zone
    )
    return {"id": well.id, "location": well.location.id}


@router.post("well-screens/")
def add_well_screen(request, well_id: int, screen_depth_top: float, screen_depth_bottom: float, screen_type_id: int = None):
    well = get_object_or_404(Well, id=well_id)
    screen_type = Lexicon.objects.filter(id=screen_type_id).first() if screen_type_id else None
    screen = WellScreen.objects.create(
        well=well,
        screen_depth_top=screen_depth_top,
        screen_depth_bottom=screen_depth_bottom,
        screen_type=screen_type
    )
    return {"id": screen.id, "well": screen.well.id}

