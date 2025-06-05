from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name='news'),
    path('search/', views.search_view, name='search_view'),
    path('results/', views.result_view, name='result_view'),
]
