from django.urls import path
from . import views

app_name = 'jobs_engine'

urlpatterns = [
    path('', views.index, name='index'),
    path('client_view', views.client_view, name='client_view'),
    path('create_task', views.create_task, name='create_task'),
    path('employee_view', views.employee_view, name='employee_view'),
]