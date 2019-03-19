from django.urls import path
from mysite import views

urlpatterns = [
    path('', views.index),
    path('chartpage/', views.chartpage),
    path('listpage/', views.listpage),
]