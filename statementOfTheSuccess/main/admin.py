from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats

from .forms import TeacherCreationForm, TeacherChangeForm, GroupAdminForm
from .models import Faculty, Speciality, Group, Student, Teacher, GroupStudent, Discipline, Grade, Record, \
    SemesterControlForm
from .resources import StudentResource, DisciplineResource, TeacherResource, RecordResource, GradeResource

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


@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    model = Faculty
    inlines = [SpecialityInline]


@admin.register(Speciality)
class SpecialityAdmin(ModelAdmin):
    list_display = ('name', 'faculty')
    form = GroupAdminForm


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


@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = ('get_name_group', 'course', 'start_year', 'end_year', 'speciality')
    list_filter = ('group_letter', 'number_group', 'course', 'start_year', 'end_year', 'speciality')
    search_fields = ('get_name_group',)
    ordering = ('group_letter', 'number_group')


@admin.register(Record)
class RecordAdmin(ImportExportModelAdmin):
    list_display = ('get_record_number', 'group', 'date', 'discipline',
                    'semester', 'total_hours', 'teacher', 'is_closed')
    fieldsets = (
        (None, {'fields': ('record_number', 'group', 'date', 'year', 'discipline',
                           'semester', 'total_hours', 'teacher', 'is_closed')}),
    )
    inlines = [GradeInline, ]
    resource_classes = [RecordResource]


@admin.register(Grade)
class GradeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Grade
    list_display = ('record', 'get_group', 'get_student', 'individual_study_plan_number',
                    'grade_ECTS', 'grade', 'grade_5', 'grade_date')
    fieldsets = (
        (None, {'fields': ('record', 'group_student', 'individual_study_plan_number',
                           'grade_ECTS', 'grade', 'grade_5', 'grade_date')}),
    )
    readonly_fields = ['grade_ECTS', 'grade_5']
    resource_classes = [GradeResource]


@admin.register(Discipline)
class DisciplineAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'teacher', 'semester_control_form')
    list_filter = ('teacher', 'semester_control_form')
    search_fields = ('teacher__last_name', 'name')
    model = Discipline
    resource_classes = [DisciplineResource]


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('number_of_the_scorebook', 'last_name', 'first_name', 'middle_name', 'admission_year')
    list_filter = ('admission_year', )
    search_fields = ('last_name', 'first_name')
    ordering = ('number_of_the_scorebook', )
    model = Student
    resource_classes = [StudentResource]


@admin.register(GroupStudent)
class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('group', 'student', )
    list_filter = ('group', )
    search_fields = ('group', 'student')
    ordering = ('group', )
    model = GroupStudent


admin.site.register(SemesterControlForm, ImportExportModelAdmin)
