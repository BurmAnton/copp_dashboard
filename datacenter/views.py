from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Event, EventType, Project
from reports.models import Tag

# Create your views here.
@csrf_exempt
@login_required
def events_page(request):
    if request.method == 'POST':
        name = request.POST["name"]
        event_link = request.POST["event_link"]
        event_type_id = request.POST["event_type"]
        event_type = get_object_or_404(EventType, id=event_type_id)
        project_id = request.POST["project"]
        project = get_object_or_404(Project, id=project_id)
        tags = request.POST.getlist("tags")
        start_date = datetime.strptime(request.POST["start_date"],"%Y-%m-%d")
        end_date = datetime.strptime(request.POST["end_date"],"%Y-%m-%d")
        notes = request.POST["notes"]
        if 'edit-event' in request.POST:
            event_id = request.POST["id"]
            event = get_object_or_404(Event, id=event_id)
            event.name = name
            event.event_link = event_link
            event.event_type = event_type
            event.project = project
            event.tags.clear()
            event.tags.add(*tags)
            event.start_date = start_date
            event.end_date = end_date
            event.notes = notes
            event.save()
        elif 'add-event' in request.POST:
            event = Event(
                name=name,
                event_link=event_link,
                event_type=event_type,
                project=project,
                start_date=start_date,
                end_date=end_date,
                notes=notes
            )
            event.save()
            event.tags.add(*tags)
    events = Event.objects.all()
    event_types = EventType.objects.all()
    projects = Project.objects.all()
    tags = Tag.objects.all()

    return render(request, "datacenter/events_page.html", {
        "events": events,
        "event_types": event_types,
        "projects": projects,
        "tags": tags,
        "page_name": "Мероприятия | ЦОПП СО"
    })