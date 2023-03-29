from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Teacher


class TeacherCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Teacher
        fields = ('email',)


class TeacherChangeForm(UserChangeForm):

    class Meta:
        model = Teacher
        fields = ('email',)