from django.contrib import admin
from django.urls import path, include
from hrma import views
from hrma.views import *

urlpatterns = [
    path('', views.index, name="index"), 
    path('user_login', views.user_login, name="user_login"),
    path('user_logout', views.user_logout, name="user_logout"),
    path('landing', views.landing, name="landing"),
    path('employee', views.employee, name="employee"),
    path('addEmployee', views.addEmployee, name="addEmployee"),
    path('updateEmployee/<int:employee_id>/', views.updateEmployee, name="updateEmployee"),
    path('delete_user/<int:pid>/', views.delete_user, name="delete_user"),
    path('filter-employees/', views.filter_employees, name='filter_employees'),

]
