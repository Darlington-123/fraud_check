from django.urls import path
from .import views

app_name = 'scams'
urlpatterns=[
    path('', views.home_view, name='home'),
    path('report/', views.report_view, name='report'),
    
]