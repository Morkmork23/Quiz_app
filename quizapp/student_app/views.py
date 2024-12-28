from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from teacher_app.models import Class
from .models import StudentProfile

def join_class(request):
    if request.method == 'POST':
        join_code = request.POST.get('class_code')
        student_profile = request.user.student_profile  # Get the student profile

        try:
            class_instance = Class.objects.get(join_code=join_code)
            class_instance.students.add(student_profile)  # Enroll student
            messages.success(request, f"Successfully joined {class_instance.name}!")
        except Class.DoesNotExist:
            messages.error(request, "Invalid class code.")

        return redirect('student_dashboard')

    return render(request, 'student_dashboard.html')

def dashboard(request):
    return render(request, 'student_dashboard.html')

def user_dashboard(request):
    return render(request, 'user_dashboard.html')


