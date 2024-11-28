from django.urls import path

from mainapp import views

urlpatterns = [
    path('hello', views.hello, name='hello'),
]
