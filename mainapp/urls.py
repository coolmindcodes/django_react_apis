from django.urls import path

from mainapp import views
from mainapp.views import AuthenticatedUser, PermissionApiView, RoleViewSet, UserApiView

urlpatterns = [
    path('users', views.users),

    path('register', views.register),
    path('user', AuthenticatedUser.as_view()),
    path('permissions', PermissionApiView.as_view()),
    path('login', views.login),
    path('logout', views.logout),
    path('roles', RoleViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('roles/<str:pk>', RoleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('users/<str:pk>', UserApiView.as_view())
]
