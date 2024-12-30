from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from teacher_app.models import Class


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
            teacher_username = class_instance.teacher.username  # Fetch the teacher's username
            if request.user in class_instance.students.all():
                messages.warning(request, f"You are already enrolled in: {class_instance.name}.")
            else:
                class_instance.students.add(request.user)
                messages.success(request, f"You have successfully joined the class: {class_instance.name}.")
            return redirect('students_dashboard')  # Ensure 'students_dashboard' exists in your URLs
        except Class.DoesNotExist:
            messages.error(request, "Invalid join code.")
            return redirect('join_class')  # Redirect back if class is not found

    return render(request, 'student_classes.html')


@login_required
def dashboard(request):
    enrolled_classes = request.user.enrolled_classes.all()
    
    # Prepare a list of dictionaries with class name and teacher's username
    class_teacher_data = []
    for class_instance in enrolled_classes:
        class_teacher_data.append({
            'class_name': class_instance.name,
            'teacher_username': class_instance.teacher.username  # Correctly access the teacher's username
        })
    
    return render(request, 'student_dashboard.html', {'class_teacher_data': class_teacher_data})


def user_dashboard(request):
    return render(request, 'user_dashboard.html')

def profile_manage(request):
    return render(request, 'profile_manage.html')

def student_classes(request):
    return render(request, 'student_classes.html')
