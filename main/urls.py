from django.contrib import admin 
from django.urls import path, include 
from . import views 

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'), 
    path('upgrade_to_admin/<int:id>/', views.upgrade_to_admin, name='upgrade_to_admin'), 
    path('create_event/', views.create_event, name='create_event'),
    path('update_event/<str:title>/', views.update_event, name='update_event'),
    path('delete_event/<str:title>/', views.delete_event, name='delete_event'), 
    path('send_requete/', views.send_requete, name='send_requete'),
    path('view_requetes_admin/', views.view_requetes_admin, name='view_requetes_admin'),
    path('view_requetes_member/', views.view_requetes_member, name='view_requetes_user'),
    path('view_events/', views.view_events, name='view_events'),
    path('view_event/<str:title>/', views.view_event, name='view_event'),
    path('view_notifications/', views.view_notifications, name='view_notifications'),
    path('accept_requete/<str:id>/', views.accept_requete, name='accept_requete'),
    path('refuse_requete/<str:id>/', views.refuse_requete, name='refuse_requete'),
    path('mark_notification_as_read/<str:id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark_notification_as_unread/<str:id>/', views.mark_notification_as_unread, name='mark_notification_as_unread'),
    path('display_participation_status/<str:event_title>/', views.display_participation_status, name='display_participation_status'),
    path('import_events/', views.import_events, name='import_events'),
]