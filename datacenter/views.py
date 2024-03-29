from datetime import datetime

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import Citizen, Event, EventType, Project, DisabilityType \
                    , Group, EducationProgram, Competence
from reports.models import Tag
from .forms import ImportDataForm
from . import imports

# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse("login"))

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

@csrf_exempt
@login_required
def citizens_list(request):
    message = ""
    citizens_filter = None
    citizens = Citizen.objects.all()
    if request.method == 'POST':
        if 'citizens-filter' in request.POST:
            citizens_filter = []
            education_types = request.POST.getlist("education_types")
            citizens_filter.append(education_types)
            if len(education_types) != 0: 
                citizens = citizens.filter(
                    education_type__in=education_types
                ).distinct()
            disabilities = request.POST.getlist("disabilities")
            citizens_filter.append(list(map(int, disabilities)))
            if len(disabilities) != 0: citizens = citizens.filter(
                    disability_type__in=disabilities).distinct()
            start_date = request.POST["start_date"]
            if start_date != '': 
                citizens = citizens.filter(
                    birthday__gt=datetime.strptime(start_date,"%Y-%m-%d")
                )
                citizens_filter.append(datetime.strptime(start_date,"%Y-%m-%d"
                                                        ).strftime("%Y-%m-%d"))
            else:
                citizens_filter.append('')
            end_date = request.POST["end_date"]
            if end_date != '': 
                citizens = citizens.filter(
                    birthday__lt=datetime.strptime(end_date,"%Y-%m-%d")
                )
                citizens_filter.append(datetime.strptime(end_date,"%Y-%m-%d"
                                                        ).strftime("%Y-%m-%d"))
            else:
                citizens_filter.append('')
            is_russian_citizen = request.POST.getlist("is_russian_citizen")
            if is_russian_citizen != ['on']:
                citizens = citizens.filter(is_russian_citizen=False)
                citizens_filter.append(False)
            else:
                citizens_filter.append(True)
            is_employed = request.POST.getlist("is_employed")
            if is_employed == ['on']:
                citizens = citizens.filter(Q(is_employed=True) | 
                                        Q(is_employed_after=True))
                citizens_filter.append(True)
            else:
                citizens_filter.append(False)
        if 'delete-citizen' in request.POST:
            citizen_id = request.POST["id"]
            citizen = get_object_or_404(Citizen, id=citizen_id)
            citizen.delete()
            message = ["delete-citizen", citizen]
        if 'change-citizen' in request.POST:
            citizen_id = request.POST["id"]
            citizen = get_object_or_404(Citizen, id=citizen_id)
            snils_number=request.POST["snils_number"].replace(" ", "")
            snils_check = Citizen.objects.filter(
                snils_number=snils_number).exclude(id=citizen.id)
            if len(snils_check) == 0:
                citizen.last_name=request.POST["last_name"].strip().capitalize()
                citizen.first_name=request.POST["first_name"].strip().capitalize()
                citizen.middle_name=request.POST["middle_name"].strip().capitalize()
                citizen.birthday=datetime.strptime(request.POST["birthday"],"%Y-%m-%d")
                citizen.sex=request.POST["sex"]
                citizen.email=request.POST["email"].strip()
                citizen.phone_number=request.POST["phone_number"].strip()
                citizen.snils_number=snils_number
                citizen.education_type=request.POST["education_type"]
                citizen.disability_type.add(*request.POST.getlist("disability"))
                if request.POST.getlist("is_russian_citizen") != ['on']:
                        citizen.is_russian_citizen = False
                if request.POST.getlist("is_employed") == ['on']: 
                    citizen.is_employed = True
                if request.POST.getlist("is_employed_after") == ['on']: 
                    citizen.is_employed = True
                citizen.save()
                message = ["citizen_change", citizen]
            else:
                citizen = citizen[0]
                message = ["snils_duplicate", snils_number]

    return render(request, "datacenter/citizens_list.html", {
        "citizens": citizens,
        "citizens_filter": citizens_filter,
        "disabilities": DisabilityType.objects.all(),
        "message": message,
        "education_types": Citizen.EDUCATION_CHOICES,
        "page_name": "Граждани | ЦОПП СО"
    })

@csrf_exempt
@login_required
def groups_page(request):
    message = None
    groups_filter = None
    if 'add-group' in request.POST:
            group = Group(name=request.POST["name"].strip())
            group.save()
            message = ["added",]
    elif 'edit-group' in request.POST:
        group_id = request.POST["id"].strip()
        group = get_object_or_404(Group, id=group_id)
        group.name=request.POST["name"].strip()
        message = ["changed",]
    if 'edit-group' in request.POST or 'add-group' in request.POST:
        education_program_id=request.POST["education_program"].strip()
        education_program=get_object_or_404(EducationProgram,id=education_program_id)
        group.education_program=education_program
        project_id=request.POST["project"].strip()
        project=get_object_or_404(Project,id=project_id)
        group.project=project
        group.tags.clear()
        group.tags.add(*request.POST.getlist("tags"))
        group.start_date=datetime.strptime(request.POST["start_date"],"%Y-%m-%d")
        group.end_date=datetime.strptime(request.POST["end_date"],"%Y-%m-%d")
        group.save()
        message.append(group)
    groups = Group.objects.all()
    if 'filter-groups' in request.POST:
        groups_filter = []
        competencies = request.POST.getlist("competencies")
        groups_filter.append(list(map(int, competencies)))
        if len(competencies) != 0: groups = groups.filter(
            education_program__competence__in=competencies
        )
        education_programs = request.POST.getlist("education_programs")
        groups_filter.append(list(map(int, education_programs)))
        if len(education_programs) != 0: groups = groups.filter(
            education_program__in=education_programs
        )
        projects = request.POST.getlist("projects")
        groups_filter.append(list(map(int, projects)))
        if len(projects) != 0: groups = groups.filter(project__in=projects)
        tags = request.POST.getlist("tags")
        groups_filter.append(list(map(int,tags)))
        if len(tags) != 0: groups = groups.filter(tags__in=tags)
        start_date = request.POST["start_date"]
        if start_date != '': 
            groups = groups.filter(
                start_date__gte=datetime.strptime(start_date,"%Y-%m-%d")
            )
            groups_filter.append(datetime.strptime(start_date,"%Y-%m-%d").strftime("%Y-%m-%d"))
        else:
            groups_filter.append('')
        end_date = request.POST["end_date"]
        if end_date != '': 
            groups = groups.filter(
                end_date__lte=datetime.strptime(end_date,"%Y-%m-%d")
            )
            groups_filter.append(datetime.strptime(end_date,"%Y-%m-%d").strftime("%Y-%m-%d"))

    tags = Tag.objects.filter(tag_type__in=['GRP', 'ALL'])
    projects = Project.objects.all()
    competencies = Competence.objects.all()
    education_programs = EducationProgram.objects.all()

    return render(request, "datacenter/groups_page.html", {
        "tags": tags,
        "projects": projects,
        "groups_filter": groups_filter,
        "groups": groups,
        "competencies": competencies,
        "education_programs": education_programs,
        "message": message,
        "page_name": "Группы | ЦОПП СО"
    })