from django.urls import path

from . import views

urlpatterns = [
    #Events
    path('', views.index, name='index'),
    path('events/', views.events_page, name='events_page'),
    path('events/<int:event_id>/registration/', views.event_reg, 
         name='event_reg'
    ),
    path('citizens/', views.citizens_list, name='citizens_list'),
    path('groups/', views.groups_page, name='groups_page')
]