from . import views
from django.urls import path

urlpatterns = [
    path('api/create_event/', views.create_event, name='create_event'),
    path('api/get_events/', views.get_events, name='get_events'),
    path('api/update_event', views.update_event, name='update_event'),
    path('calendar/', views.calendar_view, name='calendar'),
]