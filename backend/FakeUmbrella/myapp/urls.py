from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.company_list),
    path('chartpage/', views.chartpage),
#    path('listpage/', views.listpage),
    path('test/', views.test),
]