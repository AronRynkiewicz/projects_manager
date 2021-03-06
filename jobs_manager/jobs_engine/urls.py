from django.urls import path
from . import views

app_name = 'jobs_engine'

urlpatterns = [
    path('', views.index, name='index'),
    path('/admin_panel', views.admin_panel, name='admin_panel'),
]