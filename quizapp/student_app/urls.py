from django.urls import path
from . import views 

urlpatterns = [
    path("students_dashboard/", views.dashboard, name="students_dashboard"),
    path('students_dashboard/join_class/', views.join_class, name='join_class'),
    path("students_dashboard/user_dashboard/", views.user_dashboard, name="user_dashboard"),
    path("profile_manage/", views.profile_manage, name="profile_manage"),
]
