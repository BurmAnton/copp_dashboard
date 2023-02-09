from django.contrib import admin

from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter

from datacenter.models import EducationProgram, DisabilityType, Citizen, \
                              Group, Event, EventType, Competence, Project

# Register your models here.
@admin.register(DisabilityType)
class DisabilityTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description'
    )


@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'middle_name',
        'snils_number',
        'email',
        'phone_number',
        'education_type'
    )
    list_filter = (
        ('education_type', ChoiceDropdownFilter),
    )


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    pass


@admin.register(EducationProgram)
class EducationProgramAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass