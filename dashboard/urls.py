from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('log/<int:log_id>/', views.view_log, name='view_log'),
]
