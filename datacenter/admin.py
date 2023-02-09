from django.contrib import admin

from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter, \
                                                     RelatedOnlyDropdownFilter

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
    list_display = (
        'name',
        'block',
        'competence_stage',
        'competence_type'
    )
    list_filter = (
        ('block', ChoiceDropdownFilter),
        ('competence_stage', ChoiceDropdownFilter),
        ('competence_type', ChoiceDropdownFilter),
    )


@admin.register(EducationProgram)
class EducationProgramAdmin(admin.ModelAdmin):
    list_display = (
        'program_name',
        'competence',
        'program_type',
        'duration',
        'program_link'
    )
    list_filter = (
        ('competence', RelatedOnlyDropdownFilter),
        ('program_type', ChoiceDropdownFilter),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'project_type',
    )
    list_filter = (
        ('project_type', ChoiceDropdownFilter),
    )


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'event_type',
        'project',
        'start_date',
        'end_date',
        'event_link'
    )
    list_filter = (
        ('project', RelatedOnlyDropdownFilter),
        ('event_type', RelatedOnlyDropdownFilter),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'education_program',
        'project',
        'start_date',
        'end_date',
    )
    list_filter = (
        ('project', RelatedOnlyDropdownFilter),
        ('education_program', RelatedOnlyDropdownFilter),
    )