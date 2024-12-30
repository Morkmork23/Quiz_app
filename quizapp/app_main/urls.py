from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("login/", views.login_view, name="login_view"),
    path("register/", views.register_view, name="register_view"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", LogoutView.as_view(next_page='login_view'), name="logout"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
]
