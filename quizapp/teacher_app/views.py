from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Class, Quiz, Question, Participant, Choice  # Import the models
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

@login_required
def create_quiz(request):
    if request.method == 'POST':
        # Get the quiz data from the form
        title = request.POST.get('title')
        description = request.POST.get('description')
        scheduled_date = request.POST.get('scheduled_date')
        duration_minutes = request.POST.get('duration_minutes')
        assigned_class_id = request.POST.get('assigned_class')
        assigned_class = Class.objects.get(id=assigned_class_id)

        # Create a new quiz
        quiz = Quiz.objects.create(
            assigned_class=assigned_class,
            title=title,
            description=description,
            scheduled_date=scheduled_date,
            duration_minutes=duration_minutes
        )

        # Process each question
        questions_data = request.POST.getlist('questions[][text]')
        question_types = request.POST.getlist('questions[][type]')
        correct_answers = request.POST.getlist('questions[][correct_answer]')
        choices_data = request.POST.getlist('questions[][choices][]')
        correct_choices = request.POST.getlist('questions[][correct_choices][]')

        for idx, question_text in enumerate(questions_data):
            question_type = question_types[idx]
            correct_answer = correct_answers[idx]

            # Create the question
            question = Question.objects.create(
                quiz=quiz,
                question_text=question_text,
                question_type=question_type,
                correct_answer=correct_answer
            )

            # If it's a multiple-choice question, create choices
            if question_type == 'MCQ':
                for choice_text, is_correct in zip(choices_data[idx::len(choices_data)], correct_choices):
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        is_correct=(is_correct == 'on')  # True if checkbox is checked
                    )

        return redirect('quiz_list')  # Redirect to the quiz list after creating the quiz

    # Fetch classes to display in the dropdown for class assignment
    classes = Class.objects.filter(teacher=request.user)
    return render(request, 'manage_quiz.html', {'classes': classes})

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
    # Get the quiz object
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Fetch the related questions
    questions = quiz.questions.all()  # Ensure related questions are loaded
    
    # Fetch the participants (students) for the quiz
    participants = quiz.participants.all()  # Assuming 'participants' is the related field for students
    
    # Fetch the class assigned to the quiz
    assigned_class = quiz.assigned_class  # Assuming this is the foreign key to the class
    
    # Fetch the students enrolled in that class (if needed)
    enrolled_students = assigned_class.students.all()  # Assuming the class has a 'students' related field
    
    # Pass the context to the template
    return render(request, 'manage_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'participants': participants,
        'assigned_class': assigned_class,  # Pass the assigned class to the template
        'enrolled_students': enrolled_students,  # Optionally pass enrolled students
    })

def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully.')
        return redirect('teacher_dashboard')

def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz_id = question.quiz.id
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully.')
        return redirect('manage_quiz', quiz_id=quiz_id)
    
@login_required
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

        # Create the question and associate it with the quiz
        question = Question.objects.create(
            quiz=quiz,
            question_text=question_text,
            question_type=question_type,
            correct_answer=correct_answer,
        )

        # For MCQ questions, handle the choices as well
        if question_type == 'MCQ':
            choices = request.POST.getlist('choices[]')
            correct_choices = request.POST.getlist('correct_choices[]')
            for index, choice_text in enumerate(choices):
                is_correct = str(index) in correct_choices
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=is_correct,
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
