from django.urls import path
from . import views

# todo
urlpatterns = [
    path('', views.index, name='home'),
    path('records', views.RecordList.as_view(), name='records'),
    path('add-record', views.index, name='add-record'),
]
