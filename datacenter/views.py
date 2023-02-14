from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Citizen, Event, EventType, Project, DisabilityType
from reports.models import Tag
from .forms import ImportDataForm
from . import imports
# Create your views here.
@csrf_exempt
@login_required
def events_page(request):
    message = ""
    if request.method == 'POST':
        if 'delete-event' in request.POST:
            event_id = request.POST["id"]
            event = get_object_or_404(Event, id=event_id)
            event.delete()
            message = ["deleted", event]
        elif 'edit-event' in request.POST or 'add-event' in request.POST:
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
                message = ["changed", event]
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
                message = ["added", event]
    events = Event.objects.all()
    event_filter = None
    if request.method == 'POST' and 'filter-events' in request.POST:
        event_filter = []
        event_types = request.POST.getlist("event_types")
        event_filter.append(list(map(int,event_types)))
        if len(event_types) != 0: events = events.filter(
            event_type__in=event_types
        )
        projects = request.POST.getlist("projects")
        event_filter.append(list(map(int, projects)))
        if len(projects) != 0: events = events.filter(project__in=projects)
        tags = request.POST.getlist("tags")
        event_filter.append(list(map(int,tags)))
        if len(tags) != 0: events = events.filter(tags__in=tags)
        start_date = request.POST["start_date"]
        
        if start_date != '': 
            events = events.filter(
                start_date=datetime.strptime(start_date,"%Y-%m-%d")
            )
            event_filter.append(datetime.strptime(start_date,"%Y-%m-%d").strftime("%Y-%m-%d"))
        else:
            event_filter.append('')
        end_date = request.POST["end_date"]
        if end_date != '': 
            events = events.filter(
                end_date=datetime.strptime(end_date,"%Y-%m-%d")
            )
            event_filter.append(datetime.strptime(end_date,"%Y-%m-%d").strftime("%Y-%m-%d"))
    event_types = EventType.objects.all()
    projects = Project.objects.all()
    tags = Tag.objects.all()

    return render(request, "datacenter/events_page.html", {
        "events": events,
        "event_types": event_types,
        "projects": projects,
        "tags": tags,
        "event_filter": event_filter,
        "message": message,
        "page_name": "Мероприятия | ЦОПП СО"
    })

@csrf_exempt
@login_required
def event_reg(request, event_id):
    message = ""
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        if 'delete-event' in request.POST:
            event.delete()
            message = ["deleted", event]
        elif 'edit-event' in request.POST:
            event.name = request.POST["name"]
            event.event_link = request.POST["event_link"]
            event.event_type = get_object_or_404(EventType, id=request.POST["event_type"])
            event.project = get_object_or_404(Project, id=request.POST["project"])
            event.tags.clear()
            event.tags.add(*request.POST.getlist("tags"))
            event.start_date = datetime.strptime(request.POST["start_date"],"%Y-%m-%d")
            event.end_date = datetime.strptime(request.POST["end_date"],"%Y-%m-%d")
            event.notes = request.POST["notes"]
            event.save()
            message = ["changed", event]
        elif 'add-participant' in request.POST:
            citizen = Citizen.objects.filter(snils_number=request.POST["snils"].replace(" ", ""))
            if len(citizen) == 0:
                citizen = Citizen(
                    snils_number=request.POST["snils"].replace(" ", "")
                )
                citizen.save()
                message = ["new_citizen_added", citizen]
            else:
                citizen = citizen[0]
                message = ["citizen_added", citizen]
            citizen.last_name=request.POST["last_name"].strip().capitalize()
            citizen.first_name=request.POST["first_name"].strip().capitalize()
            citizen.middle_name=request.POST["middle_name"].strip().capitalize()
            citizen.birthday=datetime.strptime(request.POST["birthday"],"%Y-%m-%d")
            citizen.sex=request.POST["sex"]
            citizen.email=request.POST["email"].strip()
            citizen.phone_number=request.POST["phone"].strip()
            citizen.snils_number=request.POST["snils"].strip()
            citizen.education_type=request.POST["education_type"]
            citizen.disability_type.add(*request.POST.getlist("disability"))
            if request.POST.getlist("is_russian_citizen") != ['on']:
                    citizen.is_russian_citizen = False
            if request.POST.getlist("is_employed") == ['on']: 
                citizen.is_employed = True
            citizen.save()
            event.participants.add(citizen)
        elif 'delete-participant' in request.POST:
            citizen=get_object_or_404(Citizen, id=request.POST["id"])
            event.participants.remove(citizen)
            event.save()
            message = ["citizen_deleted", citizen]
        elif 'import-participants' in request.POST:
            form = ImportDataForm(request.POST, request.FILES)
            if form.is_valid():
                data = imports.participants(form, event)
                message = data
    event_types = EventType.objects.all()
    projects = Project.objects.all()
    tags = Tag.objects.all()
    disabilities = DisabilityType.objects.all()

    return render(request, "datacenter/event_reg.html", {
        "event": event,
        "event_types": event_types,
        "projects": projects,
        "tags": tags,
        "disabilities": disabilities,
        "message": message,
        'form' : ImportDataForm(),
        "page_name": "Регистрация на мероприятие | ЦОПП СО"
    })