from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('manager_panel', views.manager_panel, name='manager_panel'),
    path('create_team', views.create_team, name='create_team'),
    path('update_team/<str:pk>/', views.update_team, name='update_team'),
    path('delete_team/<str:pk>/', views.delete_team, name='delete_team'),
    path('add_team/<str:pk>/', views.add_team, name='add_team'),
    path('create_user', views.create_user, name='create_user'),
    path('search_user', views.search_user, name='search_user'),
    path('update_user/<str:pk>/', views.update_user, name='update_user'),
    path('delete_user/<str:pk>/', views.delete_user, name='delete_user'),
]