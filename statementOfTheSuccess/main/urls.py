from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers

from . import views
from .views import get_teacher_for_discipline

router = routers.DefaultRouter()
router.register(prefix="RecordListAPI", viewset=views.RecordListAPI, basename='RecordListAPI')
router.register(prefix="RecordDetailListAPI", viewset=views.RecordDetailListAPI, basename='RecordDetailListAPI')

# todo
urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('', views.index, name='home'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('record/', views.RecordList.as_view(), name='record'),
    # path('add-record/', views.AddRecord.as_view(), name='add-record'),
    # path('record_list_json/', views.RecordListJson.as_view(), name='RecordListJson'),
    # path('add_record_list_json/', views.RecordListJson.as_view(), name='AddRecordListJson'),
    # path('record-detal/<int:pk>/', views.RecordDetail.as_view(), name='record-detail'),
    path('record-detal/<int:pk>/', views.RedirectToAdmin.as_view(), name='record-detail'),
    path('get_teacher_for_discipline/<int:discipline_id>/', get_teacher_for_discipline,
         name='get_teacher_for_discipline'),
    # path('record/<int:pk>/pdf/', RecordPDFView.as_view(), name='record_pdf'),
    # path('record/<int:pk>/redirect/', RedirectToAdmin.as_view(), name='redirect_to_admin'),
]
