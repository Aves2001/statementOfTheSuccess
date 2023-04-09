from django.urls import path
from . import views

# todo

urlpatterns = [
    path('', views.index, name='home'),
    path('record', views.RecordList.as_view(), name='record'),
    path('add-record', views.AddRecord.as_view(), name='add-record'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('record-detal/<int:pk>/', views.RecordDetail.as_view(), name='record-detail'),
]
