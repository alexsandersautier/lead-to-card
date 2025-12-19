from django.urls import path
from event import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('confirmation/', views.confirmation, name='confirmation'),
]