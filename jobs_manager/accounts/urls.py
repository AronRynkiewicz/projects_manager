from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('create_user', views.create_user, name='create_user'),
    path('update_user/<str:pk>/', views.update_user, name='update_user'),
    path('delete_user/<str:pk>/', views.delete_user, name='delete_user'),
]