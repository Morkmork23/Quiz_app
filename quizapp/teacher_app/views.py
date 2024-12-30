from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Class, Quiz  # Import the models

@login_required
def dashboard(request):
    
    classes = Class.objects.filter(teacher=request.user)  # Ensure 'teacher' is a valid field
    quizzes = Quiz.objects.filter(assigned_class__teacher=request.user)  # Ensure the relationship exists
    return render(request, 'teacher_dashboard.html', {'classes': classes, 'quizzes': quizzes})


@login_required
def create_class(request):
    if request.method == "POST":
        class_name = request.POST.get("class_name")
        if not class_name:
            messages.error(request, "Class name is required.")
            return redirect('create_class')
        
        new_class = Class.objects.create(name=class_name, teacher=request.user)
        messages.success(request, f"Class '{new_class.name}' created successfully!")
        return redirect('class_list')

    return render(request, 'create_class.html')

def create_quiz(request):
    return HttpResponse("Create Quiz Page")

@login_required
def manage_class(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)
    enrolled_students = class_instance.students.all()

    if request.method == 'POST':
        if 'rename' in request.POST:
            new_name = request.POST.get('new_name')
            if new_name:
                class_instance.name = new_name
                class_instance.save()
        elif 'delete' in request.POST:
            class_instance.delete()
            return redirect('class_list')
        if 'remove_student' in request.POST:
            student_id = request.POST.get('student_id')
            student_to_remove = class_instance.students.get(id=student_id)
            class_instance.students.remove(student_to_remove)
            messages.success(request, f"Removed {student_to_remove.user.username} from class.")

    return render(request, 'manage_class.html', {
        'class': class_instance,
        'students': enrolled_students
    })


def view_results(request, quiz_id):
    return HttpResponse(f"View Results Page for Quiz ID {quiz_id}")

@login_required
def class_list(request):
    classes = Class.objects.filter(teacher=request.user)
    return render(request, 'class_list.html', {'classes': classes})

@login_required
def generate_join_code(request, class_id):
    try:
        class_instance = Class.objects.get(id=class_id, teacher=request.user)
        class_instance.generate_join_code()  # Calls the model method to generate the join code
        join_code = class_instance.join_code  # Get the generated join code
        messages.success(request, f"Join code generated: {join_code}")
    except Class.DoesNotExist:
        messages.error(request, "Class not found.")
    return redirect('manage_class', class_id=class_id)


