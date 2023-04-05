from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, ModelMultipleChoiceField

from .models import Teacher, Group


class TeacherCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Teacher
        fields = ('email',)


class TeacherChangeForm(UserChangeForm):
    class Meta:
        model = Teacher
        fields = ('email',)


class GroupAdminForm(ModelForm):
    class Meta:
        model = Group
        exclude = []

    group = ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name='Групи', is_stacked=False)
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['group'].initial = Group.objects.filter(speciality=self.instance.pk)

    def save_m2m(self):
        pass

    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()
        if self.instance.pk:
            self.cleaned_data['group'].update(speciality=instance.pk)
            self.fields['group'].initial.update(speciality=instance.pk)
        self.save_m2m()
        return instance
