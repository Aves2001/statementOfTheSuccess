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

    speciality = ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name='Групи', is_stacked=False)
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['speciality'].initial = Group.objects.filter(speciality=self.instance.pk)

    def save_m2m(self):
        pass
    #     # if self.instance.pk:
    #     #     self.cleaned_data['group'].update(speciality=None)
    #     #     self.fields['group'].initial.update(speciality=None)

    #
    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()

        if self.instance.pk:
            self.fields['speciality'].initial.update(speciality=instance.pk)
            self.cleaned_data['speciality'].update(speciality=instance.pk)

            qs = self.fields['speciality'].initial.difference(self.cleaned_data['speciality'])
            for i in qs:
                self.fields['speciality'].initial.filter(id=i.id).update(speciality=None)
        self.save_m2m()
        return instance
