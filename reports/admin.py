from django.contrib import admin

from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter, \
                                                     RelatedOnlyDropdownFilter

from reports.models import ReportField, ReportTemplate, Tag, TimeInterval

# Register your models here.
@admin.register(ReportTemplate)
class ReportTemplateypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(ReportField)
class ReportFieldAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'item_number',
        'report',
        'field_type'
    )
    list_filter = (
        ('field_type', ChoiceDropdownFilter),
        ('report', RelatedOnlyDropdownFilter)
    )

    filter_horizontal = (
        "tags", 
        "stop_tags", 
        "competencies",
        "disabilities",
        "projects",
        "event_types"
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tag_type'
    )
    list_filter = (
        ('tag_type', ChoiceDropdownFilter),
    )

    filter_horizontal = ("programs", "groups", "events")


@admin.register(TimeInterval)
class TimeIntervalAdmin(admin.ModelAdmin):
    list_display = (
        'report',
        'period',
        'interval_type'
    )
    list_filter = (
        ('period', ChoiceDropdownFilter),
        ('interval_type', ChoiceDropdownFilter),
        ('report', RelatedOnlyDropdownFilter)
    )
