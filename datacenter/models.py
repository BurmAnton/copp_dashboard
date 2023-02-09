from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING

# Create your models here.
class DisabilityType(models.Model):
    name = models.CharField("ОВЗ", max_length=100)
    description = models.CharField("Описание", max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = "Инвалидность"
        verbose_name_plural = "Инвалидности"

    def __str__(self):
        return  f"{self.name}"


class Citizen(models.Model):
    first_name = models.CharField("Имя", max_length=30, null=True)
    last_name = models.CharField("Фамилия", max_length=50, null=True)
    middle_name = models.CharField("Отчество", max_length=60, blank=True, null=True)
    
    SEX_CHOICES = [
        ('M', "Мужской"),
        ('F', "Женский")
    ]
    sex = models.CharField("Пол", max_length=1, choices=SEX_CHOICES, blank=True, null=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True)
    
    email = models.EmailField("Email", max_length=320, blank=True, null=True)
    phone_number = models.CharField("Номер телефона", max_length=40, blank=True, null=True)

    snils_number = models.CharField("Номер СНИЛС", max_length=11, blank=True, null=True)
    is_russian_citizen = models.BooleanField("Гражданин РФ", default=True)
    
    EDUCATION_CHOICES = [
        ('SPVO', "Закончил СПО/ВО"),
        ('STDN', "Студент ВО/СПО"),
        ('SCHL', 'Ученик 6-11 классов'),
        ('OTHR', "Другой")
    ]
    education_type = models.CharField("Образование", max_length=4, choices=EDUCATION_CHOICES, blank=True, null=True)
    is_employed = models.BooleanField("Занятость в момент регистрации", default=False)
    is_employed_after = models.BooleanField("Занятость после обучения", default=False)
    
    disability_type = models.ForeignKey(DisabilityType, verbose_name="ОВЗ", on_delete=DO_NOTHING, blank=True, null=True)

    class Meta:
        verbose_name = "Гражданин"
        verbose_name_plural = "Граждане"

    def __str__(self):
        if self.middle_name is not None:
            return  f'{self.last_name} {self.first_name} {self.middle_name}'
        return f'{self.last_name} {self.first_name}'


class EventType(models.Model):
    name = models.CharField("Тип мероприятия", max_length=100)
    description = models.CharField("Описание", max_length=300, blank=True, null=True)
    
    class Meta:
        verbose_name = "Тип мероприятия"
        verbose_name_plural = "Типы мероприятий"

    def __str__(self):
        return  f"{self.name}"


class Competence(models.Model):
    name = models.CharField("Название компетенции", max_length=200)
    
    СOMPETENCE_BLOCKS = (
        ('IT', 'Информационные и коммуникационные технологии'),
        ('SR', 'Сфера услуг'),
        ('BD', 'Строительство и строительные технологии'),
        ('MF', 'Производство и инженерные технологии'),
        ('DS', 'Творчество и дизайн'),
        ('TR', 'Транспорт и логистика'),
        ('ED', 'Образование')
    )
    block = models.CharField(max_length=2, choices=СOMPETENCE_BLOCKS, verbose_name='Блок', blank=True, null=True)
    СOMPETENCE_STAGES = (
        ('MN', 'Основная'),
        ('PR', 'Презентационная')
    )
    competence_stage = models.CharField(max_length=2, choices=СOMPETENCE_STAGES, verbose_name='Стадия', blank=True, null=True)
    СOMPETENCE_TYPES = (
        ('RU', 'WorldSkills Russia'),
        ('WSI', 'WorldSkills International'),
        ('WSE', 'WorldSkills Eurasia')
    )
    competence_type = models.CharField(max_length=3, choices=СOMPETENCE_TYPES, verbose_name='Тип', blank=True, null=True)

    class Meta:
        verbose_name = "Компетенция"
        verbose_name_plural = "Компетенции"

    def __str__(self):
        return self.name


class EducationProgram(models.Model):
    program_name = models.CharField("Название программы", max_length=500)
    competence = models.ForeignKey(Competence, verbose_name="Компетенция", on_delete=CASCADE, related_name='programs')
    PROGRAM_TYPES = (
        ('DPOPK', 'ДПО ПК'),
        ('DPOPP', 'ДПО ПП'),
        ('POP', 'ПО П'),
        ('POPP', 'ПО ПП'),
        ('POPK', 'ПО ПК'),
        ('DO', 'ДО')
    )
    program_type = models.CharField(max_length=5, choices=PROGRAM_TYPES, verbose_name='Тип программы', blank=True, null=True)
    duration = models.IntegerField("Длительность (ак. часов)", null=False, blank=False)
    program_link =  models.CharField("Ссылка на программу", max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"

    def __str__(self):
        return f"{self.program_name} ({self.get_program_type_display()}, {self.duration} ч.)"


class Project(models.Model):
    name = models.CharField("Название проекта", max_length=200)
    PROJECT_TYPES = (
        ('FED', 'Федеральный'),
        ('REG', 'Региональный'),
        ('COPP', 'ЦОПП'),
    )
    project_type = models.CharField(max_length=5, choices=PROJECT_TYPES, verbose_name='Тип программы', blank=True, null=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return f"{self.name} ({self.get_project_type_display()})"


class Event(models.Model):
    name = models.CharField("Название мероприятия", max_length=250)
    event_type = models.ForeignKey(EventType, verbose_name="Описание", on_delete=CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, verbose_name="Проект", on_delete=CASCADE, related_name='events', blank=True, null=True)
    
    start_date = models.DateField("Дата начала", null=False, blank=False)
    end_date = models.DateField("Дата окончания", null=False, blank=False)

    event_link = models.CharField("Ссылка на публикацию", max_length=200, blank=True, null=True)
    notes = models.TextField("Примечания", blank=True, null=True)
    
    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return  f"{self.name}"


class Group(models.Model):
    name = models.CharField("Название группы", max_length=500)
    education_program = models.ForeignKey(EducationProgram, verbose_name="Программа обучения", on_delete=CASCADE, related_name='groups', blank=True, null=True)
    project = models.ForeignKey(Project, verbose_name="Проект", on_delete=CASCADE, related_name='groups', blank=True, null=True)
    
    citizens = models.ManyToManyField(Citizen, verbose_name="Участники", blank=True)

    start_date = models.DateField("Дата начала обучения", blank=True, null=True)
    end_date = models.DateField("Дата окончания обучения", blank=True, null=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return  f"{self.name}"