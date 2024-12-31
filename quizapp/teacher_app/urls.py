from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="teachers_dashboard"),
    path("create-class/", views.create_class, name="create_class"),
    path("create-quiz/", views.create_quiz, name="create_quiz"),
    path("class-list/", views.class_list, name="class_list"),
    path('generate-join-code/<int:class_id>/', views.generate_join_code, name='generate_join_code'),
    path("manage-class/<int:class_id>/", views.manage_class, name="manage_class"),
    path('manage-quiz/<int:quiz_id>/', views.manage_quiz, name='manage_quiz'),
    path("view-results/<int:quiz_id>/", views.view_results, name="view_results"),

    path('quiz/manage/<int:quiz_id>/', views.manage_quiz, name='manage_quiz'),
    path('quiz/delete/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('question/add/<int:quiz_id>/', views.add_question, name='add_question'),
    path('question/edit/<int:question_id>/', views.edit_question, name='edit_question'),
    path('question/delete/<int:question_id>/', views.delete_question, name='delete_question'),
]