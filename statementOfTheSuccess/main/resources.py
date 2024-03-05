from django import forms
from import_export import fields, resources, widgets
from import_export.forms import ImportForm, ConfirmImportForm
from import_export.widgets import ForeignKeyWidget

from .models import Student, Faculty, Discipline, Teacher, Record, Grade, Group, GroupStudent, Speciality, \
    SemesterControlForm


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

# TODO
class GroupImportForm(ImportForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True)


class GroupConfirmImportForm(ConfirmImportForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True)


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
        import_id_fields = ['last_name', 'first_name', 'middle_name']

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if not dry_run:
            for i in dataset:
                group = kwargs['group']
                student = Student.objects.filter(
                    last_name=i[0],
                    first_name=i[1],
                    middle_name=i[2],
                ).get()
                obj, created = GroupStudent.objects.update_or_create(
                    group=group,
                    student=student,
                )


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


class ConcatWidget(widgets.Widget):
    def __init__(self, fields, separator='-'):
        self.fields = fields
        self.separator = separator


    def clean(self, value, row=None, *args, **kwargs):
        print(value)
        return self.separator.join(str(row.get(f)) for f in self.fields if row.get(f))


class GroupResource(resources.ModelResource):
    # group_letter = fields.Field(
    #     column_name='',
    #     attribute='group_letter',
    # )
    # number_group = fields.Field(
    #     column_name='',
    #     attribute='number_group',
    # )

    group = fields.Field(
        # attribute='group_letter',
        column_name='Групи',
        # widget=ConcatWidget(['group_letter', 'number_group'], separator='-')
    )

    course = fields.Field(
        column_name='Курс',
        attribute='course')

    start_year = fields.Field(
        column_name='З якого року',
        attribute='start_year')

    end_year = fields.Field(
        column_name='По який рік',
        attribute='end_year')

    speciality = fields.Field(
        column_name='Cпеціальність',
        attribute='speciality',
        widget=ForeignKeyWidget(Speciality, 'name')
    ),

    class Meta:
        model = Group
        exclude = ['id', ]
        fields = ['group', 'course', 'start_year', 'end_year', 'speciality']
        # export_order = ['group_letter', 'number_group', 'group', 'course', 'start_year', 'end_year', 'speciality']
        import_id_fields = ['group_letter', 'number_group']
        # skip_unchanged = ('group_letter',)

    def dehydrate_group(self, group):
        return f'{group.group_letter}-{group.number_group}'

    def before_import_row(self, row, **kwargs):
        print(row)
        group = row.get('Група')
        if group:
            group_letter, number_group = group.split('-')
            row['group_letter'] = group_letter.strip()
            row['number_group'] = number_group.strip()

    def before_export(self, queryset, *args, **kwargs):
        for obj in queryset:
            obj.group = f'{obj.group_letter}-{obj.number_group}'

    def after_export(self, queryset, data, *args, **kwargs):
        for obj in queryset:
            obj.group = None
    # TODO група
    # def get_import_fields(self):
    #     import_fields = super().get_import_fields()
    #     print(import_fields)
    #     unwanted_fields = ['group_letter', 'number_group']
    #     import_fields = [field for field in import_fields if field.attribute not in unwanted_fields]
    #     print(import_fields)
    #     print("*" * 50)
    #     return import_fields
    #
    # def before_import_row(self, row, **kwargs):
    #     group = str(row.get('Група', ''))
    #     group_letter, number_group = group.split("-")
    #     row['group_letter'] = group_letter.strip()
    #     row['number_group'] = number_group.strip()


class SpecialityResource(resources.ModelResource):
    name = fields.Field(
        column_name='Спеціальність',
        attribute='name'
    )

    faculty = fields.Field(
        column_name='Факультет',
        attribute='faculty',
        widget=ForeignKeyWidget(Faculty, 'name')
    )

    class Meta:
        model = Speciality
        exclude = ['id', ]
        import_id_fields = ['name', 'faculty']


class FacultyResource(resources.ModelResource):
    name = fields.Field(
        column_name='Факультет',
        attribute='name'
    )

    class Meta:
        model = Faculty
        exclude = ['id', ]
        import_id_fields = ['name', ]


class SemesterControlFormResource(resources.ModelResource):
    semester_control_form = fields.Field(
        column_name='Форма_семестрового_контролю',
        attribute='semester_control_form'
    )

    class Meta:
        model = SemesterControlForm
        exclude = ['id', ]
        import_id_fields = ['semester_control_form', ]


class RecordResource(resources.ModelResource):
    get_record_number = fields.Field(
        column_name='Номер_відомості',
        attribute='get_record_number')

    def dehydrate_get_record_number(self, record):
        return record.get_record_number()

    group = fields.Field(
        column_name='Група',
        attribute='group')

    def dehydrate_group(self, record):
        return record.group

    date = fields.Field(
        column_name='Дата',
        attribute='date')

    discipline = fields.Field(
        column_name='Дисципліна',
        attribute='discipline')

    def dehydrate_discipline(self, record):
        return record.discipline

    semester = fields.Field(
        column_name='Семестр',
        attribute='semester')

    total_hours = fields.Field(
        column_name='Загальна_кількість_годин',
        attribute='total_hours')

    teacher = fields.Field(
        column_name='Викладач',
        attribute='teacher')

    def dehydrate_teacher(self, record):
        return record.teacher

    is_closed = fields.Field(
        column_name='Відомість_закрита',
        attribute='is_closed')

    class Meta:
        model = Record
        exclude = ['id', 'record_number', 'year']
        export_order = ['get_record_number', 'group', 'date', 'discipline',
                        'semester', 'total_hours', 'teacher', 'is_closed']
        import_id_fields = ['get_record_number', ]


class GradeResource(resources.ModelResource):
    record = fields.Field(
        column_name='Відомість',
        attribute='record')

    def dehydrate_record(self, grade):
        return grade.record.get_record_number()

    group = fields.Field(
        column_name='Група',
        attribute='group')

    def dehydrate_group(self, grade):
        return grade.group_student.group.get_name_group()

    student = fields.Field(
        column_name='Студент',
        attribute='student')

    def dehydrate_student(self, grade):
        return grade.group_student.student

    individual_study_plan_number = fields.Field(
        column_name='Номер_індивідуального_навчального_плану',
        attribute='individual_study_plan_number')

    grade = fields.Field(
        column_name='Оцінка',
        attribute='grade')

    grade_date = fields.Field(
        column_name='Дата_виставлення_оцінки',
        attribute='grade_date')

    class Meta:
        model = Grade
        exclude = ['id', 'group_student']
        export_order = ['record', 'group', 'student', 'individual_study_plan_number',
                        'grade', 'grade_date']
        import_id_fields = ['record', ]
