from django.urls import path
from . import views

app_name = 'jobs_engine'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('client_view', views.client_view, name='client_view'),
    path('employee_view', views.employee_view, name='employee_view'),
    path('create_credentials', views.create_credentials, name='create_credentials'),
    path('create_profile', views.create_profile, name='create_profile'),
    path('manage_clients', views.manage_clients, name='manage_clients'),
    path('manage_employees', views.manage_employees, name='manage_employees'),
]