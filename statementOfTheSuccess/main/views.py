from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from .models import Record, Grade, Teacher


def index(request):
    return render(request, 'main/index.html')


class RecordList(ListView):
    model = Record
    template_name = 'main/record.html'
    context_object_name = 'record'
    extra_context = {'title': 'Відомості'}

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['grade'] = Grade.objects.all()
    #     return context


class RecordDetail(DetailView):
    model = Grade
    template_name = 'main/record-detail.html'
    context_object_name = 'grade'
    extra_context = {'title': 'Відомість'}

    def get_queryset(self):
        return Grade.objects.filter(record=Record.pk)


class AddRecord(ListView):
    model = Record
    template_name = 'main/add-record.html'
    context_object_name = 'record'


class Profile(ListView):
    model = Teacher
    template_name = 'main/profile.html'
    context_object_name = 'teacher'
