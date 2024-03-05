from rest_framework import serializers
from .models import Record, Group, Discipline, Teacher, Grade, GroupStudent, Student


####################################################################################################
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['get_name_group']


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['name']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['get_full_name']


class RecordSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    discipline = DisciplineSerializer()
    teacher = TeacherSerializer()

    class Meta:
        model = Record
        fields = ['id', 'record_number', 'date', 'group', 'total_hours', 'discipline', 'teacher']


####################################################################################################


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'middle_name']


class GroupStudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    student = StudentSerializer()

    class Meta:
        model = GroupStudent
        fields = ['group', 'student']


class GradeSerializer(serializers.ModelSerializer):
    # group_student = GroupStudentSerializer()

    class Meta:
        model = Grade
        fields = ['id', 'group_student', 'individual_study_plan_number', 'grade_ECTS', 'grade', 'grade_5', 'grade_date']
