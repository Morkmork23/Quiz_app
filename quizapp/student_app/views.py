from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from teacher_app.models import Class
from .models import StudentProfile

def join_class(request):
    if request.method == 'POST':
        join_code = request.POST.get('class_code')
        
        try:
            student_profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            messages.error(request, "Student profile not found.")
            return redirect('student_dashboard')

        try:
            class_instance = Class.objects.get(join_code=join_code)
            if class_instance.students.filter(id=student_profile.id).exists():
                messages.warning(request, "You are already enrolled in this class.")
            else:
                class_instance.students.add(student_profile)
                messages.success(request, f"Successfully joined {class_instance.name}!")
        except Class.DoesNotExist:
            messages.error(request, "Invalid class code.")
        
        return redirect('student_dashboard')

    return render(request, 'student_dashboard.html')

def dashboard(request):
    return render(request, 'student_dashboard.html')

def user_dashboard(request):
    return render(request, 'user_dashboard.html')


