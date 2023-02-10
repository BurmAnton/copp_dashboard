from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Event

# Create your views here.
@login_required
def events_page(request):
    events = Event.objects.all()

    return render(request, "datacenter/events_page.html", {
        "events": events,
        "page_name": "Мероприятия | ЦОПП СО"
    })