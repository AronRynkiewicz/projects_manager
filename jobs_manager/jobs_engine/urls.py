from django.urls import path
from . import views

app_name = 'jobs_engine'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('client_view', views.client_view, name='client_view'),
    path('employee_view', views.employee_view, name='employee_view'),
    path('create_user', views.create_user, name='create_user'),
    path('update_user/<str:pk>/', views.update_user, name='update_user'),
]