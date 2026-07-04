from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Question, Choice, Submission
from django.contrib import messages


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        submission = Submission.objects.create(user=request.user if request.user.is_authenticated else None, course=course)
        total_score = 0
        for lesson in course.lessons.all():
            for question in lesson.questions.all():
                key = f'choice_{question.id}'
                choice_id = request.POST.get(key)
                if choice_id:
                    try:
                        choice = Choice.objects.get(pk=int(choice_id), question=question)
                        submission.selected_choices.add(choice)
                        if choice.is_correct:
                            total_score += question.grade
                    except Choice.DoesNotExist:
                        pass
        submission.score = total_score
        submission.save()
        messages.success(request, 'Exam submitted successfully.')
        return redirect('onlinecourse:show_exam_result', submission_id=submission.id)
    return render(request, 'onlinecourse/submit.html', {'course': course})


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    total_possible = 0
    results = []
    for lesson in submission.course.lessons.all():
        for question in lesson.questions.all():
            total_possible += question.grade
            chosen = submission.selected_choices.filter(question=question).first()
            results.append({'question': question, 'chosen': chosen, 'correct': [c for c in question.choices.filter(is_correct=True)]})

    context = {
        'submission': submission,
        'results': results,
        'total_possible': total_possible,
        'score_received': submission.is_get_score(),
    }
    return render(request, 'onlinecourse/result.html', context)
