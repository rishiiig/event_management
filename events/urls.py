from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('add-event/', views.add_event, name='add_event'),
    path('admin-events/', views.admin_events, name='admin_events'),

    path("speaker_registration/", views.speaker_registration, name="speaker_registration"),
    path("sponsor_registration/", views.sponsor_registration, name="sponsor_registration"),

    path("show_speakers/", views.show_speakers, name="show_speakers"),


    # path('admin/events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('admin-events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('event_list/<str:event_type>/', views.events_by_type, name='events_by_type'),

    path('events/<str:event_type>/', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
    path('event/register/<int:event_id>/', views.register_ticket, name='register_ticket'),
    path('register/<int:event_id>/', views.register_ticket, name='register_event'),
]
