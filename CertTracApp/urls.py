from django.urls import path
from . import views
from .views import search

urlpatterns = [
    path('', views.index, name='index'),
    # New URL patterns for the navigation bar
    path('addtutorsession',    views.add_tutor_session,    name = 'add_hours'),
    path('add25loggedhours',   views.add_25_logged_hours,  name = 'page25'   ),
    path('addsubtopicsession', views.add_subtopic_session, name = 'session'  ),
    path('add_tutor', views.addTutor, name = 'add_tutor'),
    path('help', views.help, name = 'help'),
    path('search/', search, name='search'), 
]
