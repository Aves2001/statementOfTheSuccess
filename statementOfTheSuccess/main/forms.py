from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, SetPasswordForm
from django.forms import ModelForm, ModelMultipleChoiceField
from .models import Teacher, Group, Grade, Record


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

    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()

        if self.instance.pk and self.fields['speciality'].initial is not None:
            self.fields['speciality'].initial.update(speciality=instance.pk)
            self.cleaned_data['speciality'].update(speciality=instance.pk)

            qs = self.fields['speciality'].initial.difference(self.cleaned_data['speciality'])
            for i in qs:
                self.fields['speciality'].initial.filter(id=i.id).update(speciality=None)
        self.save_m2m()
        return instance


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'account__input',
                                                               'type': "email",
                                                               'placeholder': 'Введіть свою почту'
                                                               }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'account__input',
                                                                 'type': "password",
                                                                 'placeholder': 'Введіть пароль',
                                                                 }))

    class Meta:
        model = Teacher
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'account__input',
                                                              'type': "text",
                                                              'placeholder': 'Прізвище',
                                                              }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'account__input',
                                                               'type': "text",
                                                               'placeholder': 'Ім`я',
                                                               }))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'account__input',
                                                                'type': "text",
                                                                'placeholder': 'По батькові',
                                                                }))

    class Meta:
        model = Teacher
        fields = ['last_name', 'first_name', 'middle_name', 'academic_status']

        widgets = {
            'academic_status': forms.TextInput(attrs={
                'class': 'account__input',
                'placeholder': 'Академічний статус',
            }),
        }


class AddRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['record_number', 'group', 'date', 'semester', 'total_hours', 'discipline', 'teacher']

        widgets = {
            'record_number': forms.NumberInput(attrs={
                'placeholder': 'Номер',
            }),
            'date': forms.SelectDateWidget(attrs={
                'placeholder': 'Дата',
            }),
            'group': forms.Select(),
            'discipline': forms.Select(attrs={
                'id': 'discipline_select',
            }),
            'teacher': forms.Select(attrs={
                'id': 'teacher_select',
            }),
        }
