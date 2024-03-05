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
    readonly_fields = ['record', 'group_student', 'individual_study_plan_number',
                       'grade_ECTS', 'grade_5', 'grade_date']
    fields = ['group_student', 'individual_study_plan_number', 'grade_ECTS', 'grade', 'grade_5', 'grade_date']

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
    fieldsets = (
        (None, {'fields': ('record_number', 'group', 'date', 'year', 'discipline',
                           'semester', 'total_hours', 'teacher')}),
    )
    readonly_fields = ['record_number', 'group', 'date', 'year', 'discipline',
                       'semester', 'total_hours', 'teacher', 'is_closed']
    inlines = [GradeInline, ]
    resource_classes = [RecordResource]

    def get_readonly_fields(self, request, obj=None):
        # Якщо створюється новий об'єкт, заборонити readonly_fields
        if not obj:
            return []
        return self.readonly_fields

    def get_fields(self, request, obj=None):
        # Якщо об'єкт не передано (створення нового запису), показати всі поля
        if not obj:
            return (
                'record_number', 'group', 'date', 'year', 'discipline', 'semester', 'total_hours', 'teacher',
                'is_closed')
        # Інакше, показати всі поля, крім тих, які вказані в readonly_fields
        return [field.name for field in self.model._meta.fields if field.name not in self.readonly_fields]

    def get_form(self, request, obj=None, **kwargs):
        # Перевірка, чи редагуємо існуючий об'єкт, а не створюємо новий
        if obj:
            # Якщо так, показуємо інлайни
            self.inlines = [GradeInline, ]
        else:
            # Якщо не, не показуємо інлайни
            self.inlines = []
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Отримати список студентів для вибраної групи
        group_students = GroupStudent.objects.filter(group=obj.group)
        # Створити екземпляр Grade для кожного студента у групі
        for group_student in group_students:
            print(group_student)
            Grade.objects.create(
                record=obj,
                group_student=group_student,
                # Додайте інші необхідні поля Grade тут, наприклад, grade_date
            )

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
    readonly_fields = ['record', 'group_student', 'get_group', 'get_student', 'individual_study_plan_number',
                       'grade_ECTS', 'grade_5', 'grade_date']
    resource_classes = [GradeResource]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.grade_ECTS = obj.get_grade_ECTS()
            obj.grade_5 = obj.get_grade_5()
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:  # Перевіряємо, чи створюється новий об'єкт
            form.base_fields['grade'].required = True  # Робимо поле обов'язковим для нових об'єктів
        return form


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
