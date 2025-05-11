from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create_poll, name='create_poll'),
    path('poll/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('results/<int:poll_id>/', views.poll_results, name='poll_results'),
    path('delete/<int:poll_id>/', views.delete_poll, name='delete_poll'),
    path('my_polls/', views.my_polls, name='my_polls'),
]
