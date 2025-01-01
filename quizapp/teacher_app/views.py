from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Class, Quiz, Question, Participant  # Import the models
from django.http import JsonResponse

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

from django.http import JsonResponse

def create_quiz(request):
    if request.method == 'POST':
        # Quiz details
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        assigned_class_id = request.POST.get('assigned_class')
        scheduled_date = request.POST.get('scheduled_date')
        duration_minutes = request.POST.get('duration_minutes')

        # Validate required fields
        if not title or not assigned_class_id or not scheduled_date or not duration_minutes:
            messages.error(request, "Please fill in all required fields.")
            return redirect('create_quiz')

        try:
            assigned_class = Class.objects.get(id=assigned_class_id)
        except Class.DoesNotExist:
            messages.error(request, "Selected class does not exist.")
            return redirect('create_quiz')

        # Create quiz
        quiz = Quiz.objects.create(
            title=title,
            description=description,
            assigned_class=assigned_class,
            scheduled_date=scheduled_date,
            duration_minutes=int(duration_minutes),
        )

        # Handle questions
        questions_data = request.POST.getlist('questions')
        for question_data in questions_data:
            question_text = question_data.get('text')
            question_type = question_data.get('type')
            correct_answer = question_data.get('correct_answer')

            # Create the question
            Question.objects.create(
                quiz=quiz,
                question_text=question_text,
                question_type=question_type,
                correct_answer=correct_answer,
            )

        messages.success(request, "Quiz and questions created successfully!")
        return JsonResponse({'success': True, 'quiz_id': quiz.id})

    # Fetch data for rendering
    classes = Class.objects.all()
    return render(request, 'quiz_creation.html', {'classes': classes})

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


def manage_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    participants = Participant.objects.filter(quiz=quiz)
    return render(request, 'manage_quiz.html', {'quiz': quiz, 'participants': participants})

def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully.')
        return redirect('quiz_management')

def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz_id = question.quiz.id
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully.')
        return redirect('manage_quiz', quiz_id=quiz_id)
    
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        question_type = request.POST.get('question_type')
        correct_answer = request.POST.get('correct_answer')

        # Validate the form data
        if not question_text or not question_type or not correct_answer:
            messages.error(request, "Please provide all fields for the question.")
            return redirect('manage_quiz', quiz_id=quiz.id)

        # Create the question
        Question.objects.create(
            quiz=quiz,
            question_text=question_text,
            question_type=question_type,
            correct_answer=correct_answer,
        )
        messages.success(request, "Question added successfully!")
        return redirect('manage_quiz', quiz_id=quiz.id)

    return redirect('manage_quiz', quiz_id=quiz.id)

def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        question_type = request.POST.get('question_type')
        correct_answer = request.POST.get('correct_answer')

        # Validate the form data
        if not question_text or not question_type or not correct_answer:
            messages.error(request, "Please provide all fields for the question.")
            return redirect('manage_quiz', quiz_id=question.quiz.id)

        # Update the question
        question.question_text = question_text
        question.question_type = question_type
        question.correct_answer = correct_answer
        question.save()
        messages.success(request, "Question updated successfully!")
        return redirect('manage_quiz', quiz_id=question.quiz.id)

    return redirect('manage_quiz', quiz_id=question.quiz.id)
