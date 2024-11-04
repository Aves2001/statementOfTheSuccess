import os
from io import BytesIO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy
from django.utils.html import escape
from django.views import View
from django.views.generic import UpdateView, TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from xhtml2pdf import pisa

from .forms import UserLoginForm, ProfileForm
from .models import Record, Grade, Teacher, Discipline
from .serializers import RecordSerializer, GradeSerializer
from .services import fetch_pdf_resources
from statementOfTheSuccess import settings


class RecordListAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RecordSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Деканат').exists():
            return Record.objects \
                .filter(
                Q(group__speciality__faculty=self.request.user.faculty),
                # Q(is_closed=True) |
                # Q(teacher=self.request.user.pk)
            ) \
                .order_by('-record_number')
        if self.request.user.groups.filter(name='Викладачі').exists():
            return Record.objects \
                .filter(teacher=self.request.user.pk) \
                .order_by('-record_number')

    # def list(self, request, **kwargs):


class RecordDetailListAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer

    def get_queryset(self):
        # Отримайте URL-шлях з запиту
        url_path = self.request.path
        # Розбийте URL-шлях по символу "/" і виберіть останній елемент
        record_id = url_path.split('/')[-1]

        print('qqqqq')
        print(record_id)
        # Перевірте, чи передано id відомості
        if record_id:
            # Отримайте відомість за заданим id
            try:
                record = Record.objects.get(pk=record_id)
            except Record.DoesNotExist:
                return Grade.objects.none()  # Поверніть порожній queryset, якщо відомість не знайдено

            # Перевірте, чи користувач має доступ до цієї відомості (якщо потрібно)
            if not record.is_accessible_to_user(self.request.user):
                return Grade.objects.none()  # Поверніть порожній queryset, якщо користувач не має доступу

            # Поверніть оцінки, прив'язані до цієї відомості
            return record.grades.all()  # Припустимо, що у вас є зв'язок "grades" на моделі Record, який посилається на оцінки
        else:
            return Grade.objects.none()  # Поверніть порожній queryset, якщо id відомості не передано

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['record_id'] = self.request.GET.get('id')
        return context


# class RecordDetailListAPI(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = GradeSerializer
#
#     def get_queryset(self):
#         record_id = self.request.query_params.get('record_id')
#         if record_id:
#             if self.request.user.groups.filter(name='Деканат').exists() or \
#                     self.request.user.groups.filter(name='Викладачі').exists():
#                 return Grade.objects.filter(record=record_id)
#         else:
#             # TODO
#             return ""


# @method_decorator(csrf_exempt, name='dispatch')
# class YourModelTableView(SingleTableView):
#     model = Grade
#     table_class = EditableGradeTable
#     template_name = 'main/record-detail.html'
#
#     def get_data(self):
#         queryset = Grade.objects.all()
#         data = [{'pk': obj.pk, 'name': obj.name, 'description': obj.description} for obj in queryset]
#         return data
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         Grade.objects.create(name=data['name'], description=data['description'])
#         return JsonResponse({'status': 'ok'})
#
#     def put(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         instance = Grade.objects.get(pk=data['pk'])
#         instance.name = data['name']
#         instance.description = data['description']
#         instance.save()
#         return JsonResponse({'status': 'ok'})
#
#     def delete(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         instance = Grade.objects.get(pk=data['pk'])
#         instance.delete()
#         return JsonResponse({'status': 'ok'})


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUser(LogoutView):
    pass


def index(request):
    return render(request, 'main/index.html')


class RecordList(LoginRequiredMixin, TemplateView):
    template_name = 'main/record.html'
    extra_context = {'title': 'Відомості'}


#
# class RecordListJson(LoginRequiredMixin, BaseDatatableView):
#     model = Record
#     columns = ['record_number', 'date', 'group', 'total_hours', 'discipline', 'teacher']
#
#     def get_initial_queryset(self):
#         if self.request.user.groups.filter(name='Деканат').exists():
#             return Record.objects \
#                 .filter(Q(group__speciality__faculty=self.request.user.faculty),
#                         Q(is_closed=True) |
#                         Q(teacher=self.request.user.pk)) \
#                 .order_by('-record_number')
#         if self.request.user.groups.filter(name='Викладачі').exists():
#             return Record.objects \
#                 .filter(teacher=self.request.user.pk) \
#                 .order_by('-record_number')
#
#     def filter_queryset(self, qs):
#         search = self.request.GET.get('search[value]', None)
#         if search:
#             qs = qs.filter(
#                 Q(record_number=search) |
#                 Q(discipline=search)
#             )
#         return qs
#
#     def prepare_results(self, qs):
#         data = []
#
#         for item in qs:
#             item_data = {
#                 'id': escape(item.pk, ),
#                 'record_number': escape(item.get_record_number(), ),
#                 'date': escape(item.date, ),
#                 'name_group': escape(item.group.get_name_group, ),
#                 'total_hours': escape(item.total_hours, ),
#                 'discipline': escape(str(item.discipline), ),
#                 'teacher': escape(str(item.teacher), )
#             }
#             data.append(item_data)
#         return data


class RecordDetail(LoginRequiredMixin, TemplateView):
    template_name = 'main/record-detail.html'
    extra_context = {'title': 'Відомість'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record'] = Record.objects.filter(pk=self.kwargs['pk'])[0]
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='Деканат').exists():
            if self.request.user != Record.objects.filter(pk=self.kwargs['pk']).get().teacher:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


#
# class AddRecord(LoginRequiredMixin, TemplateView):
#     template_name = 'main/add-record.html'
#     extra_context = {'title': 'Створити відомість'}
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.groups.filter(name='Деканат').exists():
#             return self.handle_no_permission()
#         return super().dispatch(request, *args, **kwargs)
#
#
# class AddRecordListJson(RecordListJson):
#     def get_initial_queryset(self):
#         return Record.objects.all()
#

class Profile(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = ProfileForm
    template_name = 'main/profile.html'
    extra_context = {'title': 'Редагування профіля'}

    def get_object(self, queryset=None):
        return self.request.user


def get_teacher_for_discipline(request, discipline_id):
    discipline = Discipline.objects.get(pk=discipline_id)
    teacher_id = discipline.teacher.id
    return JsonResponse({'teacher_id': teacher_id})


class RedirectToAdmin(View):
    def get(self, request, pk):
        record = Record.objects.get(pk=pk)
        pdf_path = os.path.join(settings.MEDIA_ROOT, f"record_{pk}.pdf")

        if record.is_closed:
            # Перевірка існування PDF-файлу
            if os.path.exists(pdf_path):
                # Якщо файл існує, повертаємо посилання для відкриття в новій вкладці
                return redirect(f'/media/record_{pk}.pdf')

            # Якщо файл не існує, створюємо PDF
            rows_per_page = 20
            grades = list(record.grade_set.all())
            pages = [grades[i:i + rows_per_page] for i in range(0, len(grades), rows_per_page)]

            context = {
                'record': record,
                'pages': pages,
            }

            template_path = 'main/document.html'
            html = render_to_string(template_path, context, request=request)
            return HttpResponse(html)

            result = BytesIO()

            # Створення PDF
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result, encoding='utf-8', link_callback=fetch_pdf_resources)
            if pdf.err:
                return HttpResponse('Error generating PDF', status=500)

            # Збереження PDF у файл
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(result.getvalue())

            # Повернення посилання для відкриття нової вкладки
            return redirect(f'/media/record_{pk}.pdf')

        else:
            return redirect(f'/admin/main/record/{pk}/change/')
