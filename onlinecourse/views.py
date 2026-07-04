from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Question, Choice, Submission
from django.contrib import messages


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        submission = Submission.objects.create(user=request.user if request.user.is_authenticated else None, course=course)
        selected_choice_ids = []
        for lesson in course.lessons.all():
            for question in lesson.questions.all():
                key = f'choice_{question.id}'
                choice_id = request.POST.get(key)
                if choice_id:
                    try:
                        choice = Choice.objects.get(pk=int(choice_id), question=question)
                        submission.selected_choices.add(choice)
                        selected_choice_ids.append(choice.id)
                    except Choice.DoesNotExist:
                        pass
        submission.score = submission.get_score()
        submission.save()
        messages.success(request, 'Exam submitted successfully.')
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    return render(request, 'onlinecourse/submit.html', {'course': course})


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id, course=course)

    total_possible = 0
    results = []
    selected_choice_ids = set(submission.selected_choices.values_list('id', flat=True))

    for lesson in course.lessons.all():
        for question in lesson.questions.all():
            total_possible += question.grade
            selected = submission.selected_choices.filter(question=question).first()
            correct_choices = list(question.choices.filter(is_correct=True))
            is_correct = question.is_get_score(selected_choice_ids)
            results.append({
                'question': question,
                'selected': selected,
                'correct_choices': correct_choices,
                'is_correct': is_correct,
            })

    context = {
        'course': course,
        'submission': submission,
        'results': results,
        'total_score': submission.get_score(),
        'possible_score': total_possible,
        'score_received': submission.get_score() >= 0,
    }
    return render(request, 'onlinecourse/result.html', context)
