from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, CreateView
from django.views.generic.list import ListView

from .forms import UserLoginForm, ProfileForm, AddRecordForm
from .models import Record, Grade, Teacher


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUser(LogoutView):
    pass


def index(request):
    return render(request, 'main/index.html')


class RecordList(LoginRequiredMixin, ListView):
    model = Record
    template_name = 'main/record.html'
    context_object_name = 'record'
    extra_context = {'title': 'Відомості'}

    # TODO права
    def get_queryset(self):
        if self.request.user.groups.filter(name='Деканат').exists():
            return Record.objects\
                .filter(Q(group__speciality__faculty=self.request.user.faculty),
                        Q(is_closed=True) |
                        Q(teacher=self.request.user.pk))\
                .order_by('-record_number')
        if self.request.user.groups.filter(name='Викладачі').exists():
            return Record.objects\
                .filter(teacher=self.request.user.pk)\
                .order_by('-record_number')


class RecordDetail(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'main/record-detail.html'
    context_object_name = 'grade'
    extra_context = {'title': 'Відомість'}

    def get_queryset(self):
        if self.request.user.groups.filter(name='Деканат').exists() or \
                self.request.user.groups.filter(name='Викладачі').exists():
            return Grade.objects.filter(record=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record'] = Record.objects.filter(pk=self.kwargs['pk'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='Деканат').exists():
            if self.request.user != Record.objects.filter(pk=self.kwargs['pk']).get().teacher:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AddRecord(LoginRequiredMixin, CreateView):
    model = Record
    form_class = AddRecordForm
    template_name = 'main/add-record.html'
    extra_context = {'title': 'Створити відомість'}

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='Деканат').exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class Profile(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = ProfileForm
    template_name = 'main/profile.html'
    extra_context = {'title': 'Редагування профіля'}

    def get_object(self, queryset=None):
        return self.request.user
