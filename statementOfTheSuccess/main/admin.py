from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from .forms import TeacherCreationForm, TeacherChangeForm
from .models import Faculty, Speciality, Group, Student, Teacher, GroupStudent, Discipline, Grade, Record,\
    SemesterControlForm


class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'admission_year')


@admin.register(Teacher)
class TeacherAdmin(UserAdmin, ImportExportModelAdmin):
    add_form = TeacherCreationForm
    form = TeacherChangeForm
    model = Teacher

    list_display = ('email', 'last_name', 'first_name', 'middle_name', 'academic_status', 'faculty',
                    'is_staff', 'is_active',)
    list_filter = ('faculty', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_name', 'first_name', 'middle_name',
                           'academic_status', 'faculty')}),
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
    ordering = ('email',)


admin.site.register(Faculty)
admin.site.register(Speciality)
admin.site.register(Group)
admin.site.register(Student, StudentAdmin)
admin.site.register(GroupStudent)
admin.site.register(Discipline)
admin.site.register(Grade)
admin.site.register(Record)
admin.site.register(SemesterControlForm)

