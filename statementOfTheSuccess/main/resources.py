from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Student, Speciality, Faculty


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
