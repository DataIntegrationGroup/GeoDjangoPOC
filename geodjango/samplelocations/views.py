from django.shortcuts import render
from .models import SampleLocation

def index(request):
    """
    Render the index page with a list of sample locations.
    """
    locations = SampleLocation.objects.all()
    return render(request, 'samplelocations/index.html', {'locations': locations})
