from django.contrib import auth
from django.urls import path, include
from . import views

# todo
urlpatterns = [
    path('', views.index, name='home'),
    path('profile', views.Profile.as_view(), name='profile'),
    # path("accounts/", include("django.contrib.auth.urls")),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.LogoutUser.as_view(), name='logout'),
    path('record', views.RecordList.as_view(), name='record'),
    path('add-record', views.AddRecord.as_view(), name='add-record'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('record-detal/<int:pk>/', views.RecordDetail.as_view(), name='record-detail'),
]
