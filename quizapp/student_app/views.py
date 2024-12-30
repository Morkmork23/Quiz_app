from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from teacher_app.models import Class
from .models import StudentProfile

@login_required
def join_class(request):
    if request.method == "POST":
        print("POST Data:", request.POST)  # Log all POST data
        join_code = request.POST.get("join_code", "").strip()  # Ensure this is 'join_code'
        if not join_code:
            messages.error(request, "Join code cannot be empty.")
            return redirect('join_class')  # Redirect back to the join class page
        try:
            class_instance = Class.objects.get(join_code__iexact=join_code)  # Case-insensitive match
            if request.user in class_instance.students.all():
                messages.warning(request, f"You are already enrolled in: {class_instance.name}.")
            else:
                class_instance.students.add(request.user)
                messages.success(request, f"You have successfully joined the class: {class_instance.name}.")
        except Class.DoesNotExist:
            messages.error(request, "Invalid join code.")
        return redirect('students_dashboard')  # Ensure 'students_dashboard' exists in your URLs
    
    return render(request, 'student_classes.html')

@login_required
def dashboard(request):
    # Assuming you have the enrolled_classes field directly in the user model (if using StudentProfile)
    enrolled_classes = request.user.enrolled_classes.all()  # If using StudentProfile, this may change
    return render(request, 'student_dashboard.html', {'enrolled_classes': enrolled_classes})

def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def profile_manage(request):
    return render(request, 'profile_manage.html')

def student_classes(request):
    return render(request, 'student_classes.html')
