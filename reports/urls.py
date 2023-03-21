from django.urls import path

from . import views

urlpatterns = [
    #Events
    path('', views.reports_page, name='reports_page'),
    path('report/<int:report_id>/generate/', views.generate_report, name='generate_report'),
]