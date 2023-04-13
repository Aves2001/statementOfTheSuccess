from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Student, Speciality, Faculty, Discipline, Teacher


class BaseNameMixin(resources.ModelResource):
    last_name = fields.Field(
        column_name='Прізвище',
        attribute='last_name')

    first_name = fields.Field(
        column_name='Ім`я',
        attribute='first_name')

    middle_name = fields.Field(
        column_name='По батькові',
        attribute='middle_name')


class TeacherResource(BaseNameMixin, resources.ModelResource):
    email = fields.Field(
        column_name="Електронна_почта",
        attribute='email')

    academic_status = fields.Field(
        column_name='Академічний_статус',
        attribute='academic_status')

    faculty = fields.Field(
        column_name='Факультет',
        attribute='faculty',
        widget=ForeignKeyWidget(Faculty, 'name')
    )

    class Meta:
        model = Teacher
        fields = export_order = ['email', 'last_name', 'first_name', 'middle_name', 'academic_status', 'faculty']
        exclude = ['id', ]
        import_id_fields = ['email', ]


class StudentResource(BaseNameMixin):
    number_of_the_scorebook = fields.Field(
        column_name='Залікова книжка студента',
        attribute='number_of_the_scorebook')

    admission_year = fields.Field(
        column_name='Рік вступу',
        attribute='admission_year')

    class Meta:
        model = Student
        exclude = ['id', ]
        export_order = ['number_of_the_scorebook', 'last_name', 'first_name', 'middle_name', 'admission_year']
        import_id_fields = ['number_of_the_scorebook', ]


class DisciplineResource(resources.ModelResource):
    # TODO залишити фіо одним полем чи розбити
    teacher = fields.Field(
        column_name='Викладач',
        attribute='teacher')

    def dehydrate_teacher(self, discipline):
        return discipline.teacher

    name = fields.Field(
        column_name='Дисципліна',
        attribute='name')

    semester_control_form = fields.Field(
        column_name='Форма семестроого контролю',
        attribute='semester_control_form')

    def dehydrate_semester_control_form(self, discipline):
        return discipline.semester_control_form

    class Meta:
        model = Discipline
        exclude = ['id', ]
        export_order = ['teacher', 'name', 'semester_control_form']
        import_id_fields = ['name', ]
