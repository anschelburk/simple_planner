from . import views
from django.urls import path

urlpatterns = [
    path('api/create_event/', views.create_event, name='create_event'),
    path('api/get_events/', views.get_events, name='get_events'),
    path('api/update_event/', views.update_event, name='update_event'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('list/', views.list_view_items, name='list_view_items'),
    path('list/add_item/', views.list_add_item, name='list_add_item'),
    path('list/update_item/<int:pk>/', views.list_update_item, name='list_update_item'),
    ##########
    path('temp/create/', views.create_publisher_and_books, name='create_publisher_and_books'),
    # path('temp/success/', TemplateView.as_view(template_name='success.html'), name='success')
    # path('list/<int:list_id>/add_item/', views.list_add_item, name='list_add_item'),
    # path('list/<int:list_id>/update_item/<int:pk>/', views.list_update_item, name='list_update_item'),
]
