from ninja import Router
from ..models import Well, Contact
from django.shortcuts import get_object_or_404

router = Router()

@router.post("")
def add_contact_for_well(
    request,
    well_id: int,
    name: str,
    email: str,
    phone: str = None
):
    well = get_object_or_404(Well, id=well_id)
    contact = Contact.objects.create(name=name, email=email, phone=phone)
    # Create or update owner for the location if needed
    location = well.location
    owner = location.owner
    owner.contact = contact
    owner.save()
    return {"contact_id": contact.id, "owner_id": owner.id}