from django.urls import path
from . import views

app_name = 'jobs_engine'

urlpatterns = [
    path('', views.index, name='index'),
    path('client_view', views.client_view, name='client_view'),
    path('create_task', views.create_task, name='create_task'),
    path('employee_view', views.employee_view, name='employee_view'),
    path('tasks_view', views.tasks_view, name='tasks_view'),
    path('single_task_view/<str:pk>/', views.single_task_view, name='single_task_view'),
    path('download/<str:pk>/', views.download, name='download'),
    path('comment_view/<str:pk>/', views.comment_view, name='comment_view'),
    path('finished_view/<str:pk>/', views.finished_view, name='finished_view'),
]