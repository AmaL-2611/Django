from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    grade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.text

    def is_get_score(self, selected_choice_ids):
        correct_choice_ids = set(self.choices.filter(is_correct=True).values_list('id', flat=True))
        selected_ids = set(self.choices.filter(id__in=selected_choice_ids).values_list('id', flat=True))
        return correct_choice_ids == selected_ids


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Instructor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class Learner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    selected_choices = models.ManyToManyField(Choice, blank=True)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} - {self.course.title} ({self.score})"

    def get_score(self):
        total_score = 0
        selected_choice_ids = set(self.selected_choices.values_list('id', flat=True))
        for lesson in self.course.lessons.all():
            for question in lesson.questions.all():
                if question.is_get_score(selected_choice_ids):
                    total_score += question.grade
        return total_score

    def get_total_possible_score(self):
        return sum(question.grade for lesson in self.course.lessons.all() for question in lesson.questions.all())
