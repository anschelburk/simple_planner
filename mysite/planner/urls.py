from . import views
from django.urls import path

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/create_event/', views.create_event, name='create_event'),
    path('api/get_events/', views.get_events, name='get_events'),
]