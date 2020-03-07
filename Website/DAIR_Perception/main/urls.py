from django.urls import path
from . import views

urlpatterns = [
    path('', views.robot, name='home'),
    path('about/', views.about, name='about'),
    path('images/', views.images, name='images'),
    path('test/', views.test, name='test'),
    path('launch/clock/', views.launchClock, name='launchClock'),
    path('launch/bottle/', views.launchBottle, name='launchBottle'),
    path('launch/giraffe/', views.launchGiraffe, name='launchGiraffe'),
    path('launch/plant/', views.launchPlant, name='launchPlant'),
    path('stop/', views.stop, name='stop'),
]