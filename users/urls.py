from django.urls import path

from . import views

urlpatterns = [
    #auth
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]