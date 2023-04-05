from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .services import current_year, max_value_current_year


class Faculty(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name="Факультет")

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультети'

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name="Спеціальність")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Факультет")

    class Meta:
        verbose_name = 'Спеціальність'
        verbose_name_plural = 'Спеціальності'

    def __str__(self):
        return self.name


class Group(models.Model):
    # todo
    group_letter = models.CharField(max_length=3,
                                    verbose_name="Літера групи")
    number_group = models.PositiveSmallIntegerField(verbose_name="Номер групи")

    course = models.PositiveSmallIntegerField(verbose_name="Курс",
                                              default=1,
                                              validators=[MinValueValidator(1), MaxValueValidator(10)])
    start_year = models.PositiveSmallIntegerField(default=current_year(),
                                                  validators=[MinValueValidator(1995), max_value_current_year],
                                                  verbose_name="З якого року")
    end_year = models.PositiveSmallIntegerField(default=current_year(),
                                                validators=[MinValueValidator(1995), max_value_current_year],
                                                verbose_name="По який рік")
    speciality = models.ForeignKey(Speciality,
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL,
                                   verbose_name="Напрям підготовки (спеціальність)")

    class Meta:
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'

    def __str__(self):
        return f"{self.group_letter}-{self.number_group} | [{self.start_year}-{self.end_year}]"

    def get_name_group(self):
        return f"{self.group_letter}-{self.number_group}"

    get_name_group.short_description = "Група"


class BaseUser(models.Model):
    class Meta:
        abstract = True

    last_name = models.CharField(_('Прізвище'), max_length=50, blank=False, null=False)
    first_name = models.CharField(_("Ім'я"), max_length=50, blank=False, null=False)
    middle_name = models.CharField(_('По батькові'), max_length=50, blank=False, null=False)


class Student(BaseUser):
    number_of_the_scorebook = models.BigAutoField(auto_created=True,
                                                  primary_key=True,
                                                  serialize=False,
                                                  verbose_name='Номер залікової книжки')
    admission_year = models.PositiveSmallIntegerField(null=True,
                                                      blank=True,
                                                      validators=[MinValueValidator(1995), max_value_current_year],
                                                      verbose_name="Рік вступу")

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенти'

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class GroupStudent(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = 'Групи-Студенти'

    def __str__(self):
        return f"{self.group} --> {self.student}"


class Teacher(AbstractBaseUser, PermissionsMixin, BaseUser):
    # todo
    email = models.EmailField(_('Електронна почта'), unique=True)
    date_joined = models.DateTimeField(_('Дата приєднання'), auto_now_add=True)

    is_staff = models.BooleanField(default=False, verbose_name='Доступ до адмінки')
    is_active = models.BooleanField(default=True, verbose_name='Активний профіль')

    academic_status = models.CharField(null=True, blank=True, max_length=100, verbose_name="Академічний статус")
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'middle_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Викладач'
        verbose_name_plural = 'Викладачі'

    def get_full_name(self):
        full_name = f"{self.last_name} {self.first_name} {self.middle_name}"
        return full_name.strip()

    def get_short_name(self):
        return f"{self.last_name} {str(self.first_name)[0]}. {str(self.middle_name)[0]}."

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        full_name = self.get_full_name()

        if self.academic_status is None:
            return full_name
        else:
            return f"{full_name} {self.academic_status}"


class SemesterControlForm(models.Model):
    semester_control_form = models.CharField(max_length=50,
                                             auto_created=True,
                                             primary_key=True,
                                             serialize=False,
                                             verbose_name="Форма семестрового контролю")

    class Meta:
        verbose_name = 'Форма семестрового контролю'
        verbose_name_plural = 'Форми семестрового контролю'

    def __str__(self):
        return self.semester_control_form


class Discipline(models.Model):
    name = models.CharField(max_length=150,
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name="Дисципліна")
    semester_control_form = models.ForeignKey(SemesterControlForm,
                                              null=True,
                                              blank=True,
                                              on_delete=models.SET_NULL,
                                              verbose_name="Форма семестрового контролю")
    teacher = models.ForeignKey(Teacher,
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL,
                                verbose_name="Викладач")

    class Meta:
        verbose_name = 'Дисципліна'
        verbose_name_plural = 'Дисципліни'

    def __str__(self):
        return self.name


def add_record_number():
    last_record_number = Record.objects.filter(year=current_year()).order_by('record_number').last()
    if not last_record_number:
        return 1
    return last_record_number.record_number + 1


class Record(models.Model):
    record_number = models.PositiveIntegerField(null=False,
                                                blank=False,
                                                default=add_record_number,
                                                validators=[MinValueValidator(1)],
                                                verbose_name="Номер відомості")
    date = models.DateField(null=False,
                            blank=False,
                            default=timezone.now,
                            verbose_name="Дата")
    year = models.PositiveSmallIntegerField(null=False, blank=False,
                                            default=current_year(),
                                            verbose_name="Рік")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name="Дисциплана")
    semester = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                                                verbose_name="Семестр")
    total_hours = models.PositiveSmallIntegerField(verbose_name="Загальна кількість годин")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Викладач")
    is_closed = models.BooleanField(default=False, verbose_name="Відомість закрита")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'record_number'], name='unique record_number')
        ]
        verbose_name = 'Відомість'
        verbose_name_plural = 'Відомості'

    def get_record_number(self):
        return f"{str(self.year)[-2:]}/{self.record_number}"

    def __str__(self):
        record_number = self.get_record_number()
        return f"№ {record_number} | {self.teacher} | {self.discipline}"

    get_record_number.short_description = str(record_number.verbose_name)


class Grade(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name="Відомість")
    group_student = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, verbose_name="Студент")
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                             verbose_name="Оцінка")
    grade_date = models.DateField(verbose_name="Дата виставлення оцінки")

    class Meta:
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'

    def __str__(self):
        return f"{self.record} | {self.group_student} | {self.grade}"
