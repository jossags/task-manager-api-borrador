from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name='logout'),
    path('tasks/', views.task_list_create, name='task_list_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
]