# Generated by Django 4.1.7 on 2024-11-04 07:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main.models
import main.services


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('last_name', models.CharField(max_length=50, verbose_name='Прізвище')),
                ('first_name', models.CharField(max_length=50, verbose_name="Ім'я")),
                ('middle_name', models.CharField(max_length=50, verbose_name='По батькові')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Електронна почта')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата приєднання')),
                ('is_staff', models.BooleanField(default=True, verbose_name='Доступ до редагування')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активний профіль')),
                ('academic_status', models.CharField(blank=True, max_length=100, null=True, verbose_name='Академічний статус')),
            ],
            options={
                'verbose_name': 'Викладач',
                'verbose_name_plural': 'Викладачі',
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Дисципліна')),
            ],
            options={
                'verbose_name': 'Дисципліна',
                'verbose_name_plural': 'Дисципліни',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Факультет')),
            ],
            options={
                'verbose_name': 'Факультет',
                'verbose_name_plural': 'Факультети',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_letter', models.CharField(max_length=3, verbose_name='Літера групи')),
                ('number_group', models.PositiveSmallIntegerField(verbose_name='Номер групи')),
                ('course', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Курс')),
                ('start_year', models.PositiveSmallIntegerField(default=2024, validators=[django.core.validators.MinValueValidator(1995), main.services.max_value_current_year], verbose_name='З якого року')),
                ('end_year', models.PositiveSmallIntegerField(default=2024, validators=[django.core.validators.MinValueValidator(1995), main.services.max_value_current_year], verbose_name='По який рік')),
            ],
            options={
                'verbose_name': 'Група',
                'verbose_name_plural': 'Групи',
            },
        ),
        migrations.CreateModel(
            name='SemesterControlForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_control_form', models.CharField(max_length=50, unique=True, verbose_name='Форма семестрового контролю')),
            ],
            options={
                'verbose_name': 'Форма семестрового контролю',
                'verbose_name_plural': 'Форми семестрового контролю',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='Прізвище')),
                ('first_name', models.CharField(max_length=50, verbose_name="Ім'я")),
                ('middle_name', models.CharField(max_length=50, verbose_name='По батькові')),
                ('number_of_the_scorebook', models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='Номер залікової книжки')),
                ('admission_year', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1995), main.services.max_value_current_year], verbose_name='Рік вступу')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенти',
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Спеціальність')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.faculty', verbose_name='Факультет')),
            ],
            options={
                'verbose_name': 'Спеціальність',
                'verbose_name_plural': 'Спеціальності',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_number', models.PositiveIntegerField(default=main.models.add_record_number, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Номер відомості')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('year', models.PositiveSmallIntegerField(default=2024, verbose_name='Рік')),
                ('semester', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Семестр')),
                ('total_hours', models.PositiveSmallIntegerField(verbose_name='Загальна кількість годин')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Відомість закрита')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.discipline', verbose_name='Дисциплана')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.group', verbose_name='Група')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Викладач')),
            ],
            options={
                'verbose_name': 'Відомість',
                'verbose_name_plural': 'Відомості',
            },
        ),
        migrations.CreateModel(
            name='GroupStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.group', verbose_name='Група')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student', verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Групи-Студенти',
                'verbose_name_plural': 'Групи-Студенти',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='speciality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.speciality', verbose_name='Напрям підготовки (спеціальність)'),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('individual_study_plan_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер індивідуального навчального плану')),
                ('grade', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Оцінка')),
                ('grade_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата виставлення оцінки')),
                ('group_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.groupstudent', verbose_name='Студент')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.record', verbose_name='Відомість')),
            ],
            options={
                'verbose_name': 'Оцінка',
                'verbose_name_plural': 'Оцінки',
            },
        ),
        migrations.AddField(
            model_name='discipline',
            name='semester_control_form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.semestercontrolform', verbose_name='Форма семестрового контролю'),
        ),
        migrations.AddField(
            model_name='discipline',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Викладач'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.faculty', verbose_name='Факультет'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='record',
            constraint=models.UniqueConstraint(fields=('year', 'record_number'), name='unique record_number'),
        ),
        migrations.AddConstraint(
            model_name='group',
            constraint=models.UniqueConstraint(fields=('group_letter', 'number_group'), name='unique group'),
        ),
    ]
