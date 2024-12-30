from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="teachers_dashboard"),
    path("create-class/", views.create_class, name="create_class"),
    path("create-quiz/", views.create_quiz, name="create_quiz"),
    path("class-list/", views.class_list, name="class_list"),
    path('generate-join-code/<int:class_id>/', views.generate_join_code, name='generate_join_code'),
    path("manage-class/<int:class_id>/", views.manage_class, name="manage_class"),
    path("view-results/<int:quiz_id>/", views.view_results, name="view_results"),
]