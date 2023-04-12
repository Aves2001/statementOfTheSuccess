from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats

from .forms import TeacherCreationForm, TeacherChangeForm, GroupAdminForm
from .models import Faculty, Speciality, Group, Student, Teacher, GroupStudent, Discipline, Grade, Record, \
    SemesterControlForm
from .resources import StudentResource

DEFAULT_FORMATS = [fmt for fmt in (
    base_formats.XLSX,
) if fmt.is_available()]


class ImportExportModelAdmin(ImportExportMixin, admin.ModelAdmin):
    formats = DEFAULT_FORMATS

    class Meta:
        abstract = True


class SpecialityInline(admin.TabularInline):
    model = Speciality


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
                           'semester', 'total_hours', 'teacher')}),
    )


admin.site.register(GroupStudent, ImportExportModelAdmin)
admin.site.register(Discipline, ImportExportModelAdmin)
admin.site.register(Grade, ImportExportModelAdmin)
admin.site.register(SemesterControlForm, ImportExportModelAdmin)


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('number_of_the_scorebook', 'last_name', 'first_name', 'middle_name', 'admission_year')
    model = Student
    resource_classes = [StudentResource]
