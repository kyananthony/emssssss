from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.employee_login, name='login'),
    path('time_in/', views.time_in, name='time_in'),
    path('time_out/', views.time_out, name='time_out'),
    path('time_log/', views.time_log, name='time_log'),
]
