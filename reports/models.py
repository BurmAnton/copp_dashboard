from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING

from datacenter.models import EducationProgram, Group, Event

# Create your models here.
class ReportTemplate(models.Model):
    name = models.CharField("Название отчёта", max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"


class Tag(models.Model):
    name = models.CharField("Тег", max_length=500, null=False, blank=False)

    TAG_TYPES = [
        ('PRGM', "Для программ"),
        ('GRP', "Для групп"),
        ('VNT', "Для мероприятий"),
        ('ALL', "Для всех"),
    ]
    tag_type = models.CharField("Тип тега", max_length=4, choices=TAG_TYPES, default='ALL', null=False, blank=False)

    programs = models.ManyToManyField(EducationProgram, verbose_name="Программы", related_name="tags", blank=True)
    groups = models.ManyToManyField(Group, verbose_name="Группы", related_name="tags", blank=True)
    events = models.ManyToManyField(Event, verbose_name="Мероприятия", related_name="tags", blank=True)
    
    def __str__(self):
        return f'{self.name} ({self.get_tag_type_display()})'

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class ReportField(models.Model):
    item_number = models.CharField("Номер пункта", max_length=15, null=False, blank=False)
    name = models.CharField("Название поля", max_length=500, null=False, blank=False)
    report = models.ForeignKey(ReportTemplate, verbose_name="Отчёт", related_name="fields", on_delete=CASCADE, null=False, blank=False)
    FIELD_TYPES = [
        ('PPL', "Человек"),
        ('PRGM', "Программ"),
        ('VNTS', "Мероприятий")
    ]
    field_type = models.CharField("Единица измерения", max_length=4, default='PPL', choices=FIELD_TYPES)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", related_name="fields", blank=True)
    stop_tags = models.ManyToManyField(Tag, verbose_name="Стоп-теги", related_name="stop_fields", blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Показатель"
        verbose_name_plural = "Показатели"


class TimeInterval(models.Model):
    name = models.CharField("Название интервала", max_length=500, null=False, blank=False)
    report = models.ForeignKey(ReportTemplate, verbose_name="Отчёт", related_name="intervals", on_delete=CASCADE, null=False, blank=False)

    PERIOD_TYPES = [
        ('YEAR', "Год"),
        ('QRTR', "Квартал"),
        ('MNTH', "Месяц"),
        ('DTS', "Конкр. даты")
    ]
    period = models.CharField("Единица измерения", max_length=4, default='QRTR', choices=PERIOD_TYPES)
    INTERVAL_TYPES = [
        ('GRWNGA', "Нарастающим (с открытия)"),
        ('GRWNG', "Нарастающим (за период)"),
        ('SNGL', "За выбранный"),
        ('DTS', "Конкр. даты")
    ]
    interval_type = models.CharField("Тип интервала", max_length=6, default='SNGL', choices=INTERVAL_TYPES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Временой интервал"
        verbose_name_plural = "Временые интервалы"