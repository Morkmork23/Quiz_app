# student_app/models.py
from django.db import models
from django.contrib.auth.models import User
from teacher_app.models import Class, Quiz

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    enrolled_classes = models.ManyToManyField('teacher_app.Class', related_name="students_in_class")

    def __str__(self):
        return self.user.username


class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.FloatField(blank=True, null=True)  # Store the score
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"
