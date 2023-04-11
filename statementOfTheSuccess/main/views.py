from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView

from .forms import UserLoginForm
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
        return Record.objects.filter(teacher=self.request.user.pk)


class RecordDetail(ListView):
    model = Grade
    template_name = 'main/record-detail.html'
    context_object_name = 'grade'
    extra_context = {'title': 'Відомість'}

    def get_queryset(self):
        return Grade.objects.filter(record=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record'] = Record.objects.filter(pk=self.kwargs['pk'])
        return context


class AddRecord(ListView):
    model = Record
    template_name = 'main/add-record.html'
    context_object_name = 'record'


class Profile(ListView):
    model = Teacher
    template_name = 'main/profile.html'
    context_object_name = 'teacher'
