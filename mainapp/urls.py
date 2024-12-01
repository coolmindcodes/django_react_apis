from django.urls import path

from mainapp import views
from mainapp.views import AuthenticatedUser

urlpatterns = [
    path('users', views.users),

    path('register', views.register),
    path('user', AuthenticatedUser.as_view()),

    path('login', views.login),
    path('logout', views.logout),
]
