from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query_results/', views.query_results, name='query_results'),
]
