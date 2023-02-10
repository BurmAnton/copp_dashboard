from django.urls import path

from . import views

urlpatterns = [
    #Events
    path('events/', views.events_page, name='events_page'),
]