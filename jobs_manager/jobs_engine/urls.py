from django.urls import path
from . import views

app_name = 'jobs_engine'

urlpatterns = [
    path('', views.index, name='index'),
    path('client_view', views.client_view, name='client_view'),
    path('employee_view', views.employee_view, name='employee_view'),
]