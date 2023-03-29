from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Record, Grade


def index(request):
    print(request)
    record_number = Record.objects.first()
    data = {
        'title': "Головна сторінка",
        'record_number': record_number.get_record_number
    }
    return render(request, 'main/index.html', data)


class RecordList(ListView):
    model = Record
    template_name = 'main/record.html'
    context_object_name = 'records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grade'] = Grade.objects.all()
        return context
