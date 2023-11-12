from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query_results/', views.query_results, name='query_results'),
    path('25', views.page25, name='25'),
    path('add_tutor', views.addTutor, name='add_tutor'),
    path('help', views.help, name='help'),
        # New URL patterns for the navigation bar
    path('view_edit_tutor_hours/', views.view_edit_tutor_hours, name='view_edit_tutor_hours'),
    path('add_tutor_hours/', views.add_tutor_hours, name='add_tutor_hours'),
    path('edit_tutor_hours/<int:tutor_hours_id>/', views.edit_tutor_hours, name='edit_tutor_hours'),
    path('input_hours/', views.input_hours, name='input_hours'),
    path('input_completed_courses/', views.input_completed_courses, name='input_completed_courses'),
    path('add_remove_tutors/', views.add_remove_tutors, name='add_remove_tutors'),
]
