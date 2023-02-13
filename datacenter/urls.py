from django.urls import path

from . import views

urlpatterns = [
    #Events
    path('events/', views.events_page, name='events_page'),
    path('events/<int:event_id>/registration/', views.event_reg, 
         name='event_reg'
        )
]