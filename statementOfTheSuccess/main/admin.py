from pprint import pprint

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats

from .forms import TeacherCreationForm, TeacherChangeForm, GroupAdminForm
from .models import Faculty, Speciality, Group, Student, Teacher, Discipline, Grade, Record, \
    SemesterControlForm, GroupStudent
from .resources import StudentResource, DisciplineResource, TeacherResource, RecordResource, GradeResource, \
    GroupConfirmImportForm, GroupImportForm, GroupResource, SpecialityResource, FacultyResource, \
    SemesterControlFormResource

admin.site.index_title = "Буковинський Університет"

DEFAULT_FORMATS = [fmt for fmt in (
    base_formats.XLSX,
) if fmt.is_available()]


class ImportExportModelAdmin(ImportExportMixin, admin.ModelAdmin):
    formats = DEFAULT_FORMATS

    class Meta:
        abstract = True


class SpecialityInline(admin.TabularInline):
    model = Speciality


class GradeInline(admin.TabularInline):
    model = Grade
    extra = 0
    fields = ['group_student', 'individual_study_plan_number', 'grade_ECTS', 'grade', 'grade_5', 'grade_date']

    def get_readonly_fields(self, request, obj=None):
        # Поля, які завжди повинні залишатися лише для читання
        always_readonly = ['record', 'group_student', 'individual_study_plan_number', 'grade_date', 'grade_ECTS', 'grade_5']

        # Перевірка, чи користувач у групі "Деканат"
        if request.user.groups.filter(name="Деканат").exists():
            return always_readonly if obj is None else ['grade_ECTS', 'grade_5', ]
        else:
            return always_readonly

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
            'admin/js/grade_set-group_student.js',
        )


@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    model = Faculty
    inlines = [SpecialityInline]
    resource_classes = [FacultyResource]


@admin.register(Speciality)
class SpecialityAdmin(ImportExportModelAdmin):
    list_display = ('name', 'faculty')
    form = GroupAdminForm
    resource_classes = [SpecialityResource]


@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin, UserAdmin):
    add_form = TeacherCreationForm
    form = TeacherChangeForm
    model = Teacher
    resource_classes = [TeacherResource]
    list_display = ('email', 'last_name', 'first_name', 'middle_name', 'academic_status', 'faculty',
                    'is_staff', 'is_active',)
    list_filter = ('faculty', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_name', 'first_name', 'middle_name',
                           'academic_status', 'faculty', 'groups')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'last_name', 'first_name', 'middle_name', 'academic_status', 'faculty',
                       'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'last_name')
    ordering = ('last_name',)
    # readonly_fields = ('is_staff',)


@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = ('get_name_group', 'course', 'start_year', 'end_year', 'speciality')
    list_filter = ('group_letter', 'number_group', 'course', 'start_year', 'end_year', 'speciality')
    search_fields = ('get_name_group',)
    ordering = ('group_letter', 'number_group')
    resource_classes = [GroupResource]


@admin.register(Record)
class RecordAdmin(ImportExportModelAdmin):
    list_display = ('get_record_number', 'group', 'date', 'discipline',
                    'semester', 'total_hours', 'teacher', 'is_closed')
    list_filter = ('is_closed', 'teacher')
    fieldsets = (
        (None, {'fields': ('record_number', 'group', 'date', 'year', 'discipline',
                           'semester', 'total_hours', 'teacher', 'is_closed')}),
    )
    readonly_fields = ['record_number', 'group', 'date', 'year', 'discipline',
                       'semester', 'total_hours', 'teacher']
    inlines = [GradeInline]
    resource_classes = [RecordResource]

    def get_queryset(self, request):
        # Отримуємо початковий набір даних
        qs = super().get_queryset(request)

        # Фільтруємо записи, якщо користувач не є суперкористувачем
        if request.user.is_superuser or request.user.groups.filter(name="Деканат").exists():
            return qs  # Якщо суперкористувач, показати всі записи
        # Інакше, показати лише записи, що належать поточному користувачу (наприклад, 'teacher')
        return qs.filter(teacher=request.user)

    def get_readonly_fields(self, request, obj=None):
        # Робимо поля тільки для читання при редагуванні об'єкта
        if obj:
            return self.readonly_fields
        # Всі поля можна редагувати при створенні нового об'єкта
        return []

    def get_fields(self, request, obj=None):
        # При створенні нової відомості не показувати поле 'is_closed'
        if not obj:
            return ('record_number', 'group', 'date', 'year', 'discipline', 'semester', 'total_hours', 'teacher')
        # Інакше показати всі поля
        return super().get_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        # Display the inline forms conditionally based on whether an object is being edited or created
        if obj:
            self.inlines = [GradeInline]
        else:
            self.inlines = []
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # When creating a new record, add Grade objects for each student in the group
        if not change:
            group_students = GroupStudent.objects.filter(group=obj.group)
            for group_student in group_students:
                Grade.objects.create(
                    record=obj,
                    group_student=group_student,
                    # Set other fields as necessary
                )

    def has_change_permission(self, request, obj=None):
        # Надати право редагувати тільки викладачам, які відповідають полю teacher
        if obj and obj.teacher == request.user or request.user.groups.filter(name="Деканат").exists():
            return True
        # elif request.user.is_superuser:
        #     return True  # Суперкористувач завжди може редагувати
        return False

    def has_import_permission(self, request):
        # Дозволити імпорт тільки суперкористувачам
        return request.user.is_superuser

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
            'admin/js/get_teacher_for_discipline.js',
        )


@admin.register(Grade)
class GradeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Grade
    list_display = ('record', 'get_group', 'get_student', 'individual_study_plan_number',
                    'grade_ECTS', 'grade', 'grade_5', 'grade_date')
    fieldsets = (
        (None, {'fields': ('record', 'group_student', 'individual_study_plan_number',
                           'grade_ECTS', 'grade', 'grade_5', 'grade_date')}),
    )
    readonly_fields = ['grade_ECTS', 'grade_5', 'grade_date']
    resource_classes = [GradeResource]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if obj.grade:
                obj.grade_ECTS = obj.get_grade_ECTS()
                obj.grade_5 = obj.get_grade_5()
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # if obj is None:  # Перевіряємо, чи створюється новий об'єкт
        #     form.base_fields['grade'].required = True  # Робимо поле обов'язковим для нових об'єктів
        return form

    def has_module_permission(self, request):
        # Дозволити доступ тільки для головного адміністратора
        return request.user.is_superuser


@admin.register(Discipline)
class DisciplineAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'teacher', 'semester_control_form')
    list_filter = ('teacher', 'semester_control_form')
    search_fields = ('teacher__last_name', 'name')
    model = Discipline
    resource_classes = [DisciplineResource]


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('number_of_the_scorebook', 'last_name', 'first_name', 'middle_name',
                    'admission_year', 'group_list_field_display')
    list_filter = ('admission_year',)
    search_fields = ('last_name', 'first_name')
    ordering = ('number_of_the_scorebook',)
    model = Student
    resource_classes = [StudentResource]
    import_form_class = GroupImportForm
    confirm_form_class = GroupConfirmImportForm

    def group_list_field_display(self, student):
        return ", ".join([str(group_student.group.get_name_group())
                          for group_student in GroupStudent.objects
                         .filter(student=student).order_by('group').all()])

    group_list_field_display.short_description = "ГРУПИ"

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)
        if import_form:
            initial['group'] = import_form.cleaned_data['group']
        return initial

    def get_import_data_kwargs(self, request, *args, **kwargs):
        form = kwargs.get('form')
        if form:
            print(form.cleaned_data['group'])
            return form.cleaned_data
        return {}


@admin.register(GroupStudent)
class GroupStudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('group', 'student',)
    list_filter = ('group',)
    search_fields = ('group', 'student')
    ordering = ('group',)
    model = GroupStudent


@admin.register(SemesterControlForm)
class DisciplineAdmin(ImportExportModelAdmin):
    model = SemesterControlForm
    resource_classes = [SemesterControlFormResource]
