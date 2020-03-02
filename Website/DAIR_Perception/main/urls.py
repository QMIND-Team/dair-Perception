from django.urls import path
from . import views

urlpatterns = [
    path('', views.robot, name='home'),
    path('about/', views.about, name='about'),
    path('images/', views.images, name='images'),
    path('test/', views.test, name='test'),
]