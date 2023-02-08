# Generated by Django 4.1.6 on 2023-02-07 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, null=True, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Отчество')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Мужской'), ('F', 'Женский')], max_length=1, null=True, verbose_name='Пол')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('email', models.EmailField(blank=True, max_length=320, null=True, verbose_name='Email')),
                ('phone_number', models.CharField(blank=True, max_length=40, null=True, verbose_name='Номер телефона')),
                ('snils_number', models.CharField(blank=True, max_length=11, null=True, verbose_name='Номер СНИЛС')),
                ('is_russian_citizen', models.BooleanField(default=True, verbose_name='Гражданин РФ')),
                ('education_type', models.CharField(blank=True, choices=[('SPVO', 'Закончил СПО/ВО'), ('STDN', 'Студент ВО/СПО'), ('SCHL', 'Ученик 6-11 классов'), ('OTHR', 'Другой')], max_length=4, null=True, verbose_name='Образование')),
                ('is_employed', models.BooleanField(default=False, verbose_name='Занятость в момент регистрации')),
                ('is_employed_after', models.BooleanField(default=False, verbose_name='Занятость после обучения')),
            ],
            options={
                'verbose_name': 'Гражданин',
                'verbose_name_plural': 'Граждане',
            },
        ),
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название компетенции')),
                ('block', models.CharField(blank=True, choices=[('IT', 'Информационные и коммуникационные технологии'), ('SR', 'Сфера услуг'), ('BD', 'Строительство и строительные технологии'), ('MF', 'Производство и инженерные технологии'), ('DS', 'Творчество и дизайн'), ('TR', 'Транспорт и логистика'), ('ED', 'Образование')], max_length=2, null=True, verbose_name='Блок')),
                ('competence_stage', models.CharField(blank=True, choices=[('MN', 'Основная'), ('PR', 'Презентационная')], max_length=2, null=True, verbose_name='Стадия')),
                ('competence_type', models.CharField(blank=True, choices=[('RU', 'WorldSkills Russia'), ('WSI', 'WorldSkills International'), ('WSE', 'WorldSkills Eurasia')], max_length=3, null=True, verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Компетенция',
                'verbose_name_plural': 'Компетенции',
            },
        ),
        migrations.CreateModel(
            name='DisabilityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='ОВЗ')),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Инвалидность',
                'verbose_name_plural': 'Инвалидности',
            },
        ),
        migrations.CreateModel(
            name='EducationProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=500, verbose_name='Название программы')),
                ('program_type', models.CharField(blank=True, choices=[('DPOPK', 'ДПО ПК'), ('DPOPP', 'ДПО ПП'), ('POP', 'ПО П'), ('POPP', 'ПО ПП'), ('POPK', 'ПО ПК'), ('DO', 'ДО')], max_length=5, null=True, verbose_name='Тип программы')),
                ('duration', models.IntegerField(verbose_name='Длительность (ак. часов)')),
                ('program_link', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ссылка на программу')),
                ('competence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='datacenter.competence', verbose_name='Компетенция')),
            ],
            options={
                'verbose_name': 'Программа',
                'verbose_name_plural': 'Программы',
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Тип мероприятия')),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Тип мероприятия',
                'verbose_name_plural': 'Типы мероприятий',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название проекта')),
                ('project_type', models.CharField(blank=True, choices=[('FED', 'Федеральный'), ('REG', 'Региональный'), ('COPP', 'ЦОПП')], max_length=5, null=True, verbose_name='Тип программы')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название группы')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Дата начала обучения')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Дата окончания обучения')),
                ('citizens', models.ManyToManyField(blank=True, to='datacenter.citizen', verbose_name='Участники')),
                ('education_program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='datacenter.educationprogram', verbose_name='Программа обучения')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='datacenter.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название мероприятия')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('event_link', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ссылка на публикацию')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Примечания')),
                ('event_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datacenter.eventtype', verbose_name='Описание')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='datacenter.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Тип мероприятия',
                'verbose_name_plural': 'Типы мероприятий',
            },
        ),
        migrations.AddField(
            model_name='citizen',
            name='disability_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='datacenter.disabilitytype', verbose_name='ОВЗ'),
        ),
    ]
