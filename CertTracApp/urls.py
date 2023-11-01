from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query_results/', views.query_results, name='query_results'),
<<<<<<< Updated upstream
    path('session', views.session, name='session')
=======
    path('25', views.page25, name='25')
>>>>>>> Stashed changes
]
