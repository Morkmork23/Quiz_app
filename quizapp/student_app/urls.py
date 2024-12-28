from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="students_dashboard"),
    path('join_class/', views.join_class, name='join_class'),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
]