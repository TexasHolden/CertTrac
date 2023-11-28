from django.urls import path
from . import views
from .views import search

urlpatterns = [
    path('', views.render_team_meetings, name='team_meetings'),
    # New URL patterns for the navigation bar
    path('renderteammeeting',   views.render_team_meetings,  name = 'team_meetings'),
    path('addtutorsession',     views.add_tutor_session,     name = 'add_hours'),
    path('add25loggedhours',    views.add_25_logged_hours,   name = 'page25'   ),
    path('addsubtopicsession',  views.add_subtopic_session,  name = 'session'  ),
    path('editsubtopicsession', views.edit_subtopic_session, name = 'session_'),
    path('add_tutor',           views.addTutor,              name = 'add_tutor'),
    path('help',                views.help,                  name = 'help'     ),
    path('search/',             views.search,                name = 'search'     ), 

    path('update_level_logic', views.update_level_logic, name='update_level_logic'),
    path('update_level',       views.update_level,       name='update_level'      ),

    path('edittutor', views.edit_tutor, name = 'edit_tutor'),
    path('edittakes', views.edit_takes, name = 'edit_takes'),
]
