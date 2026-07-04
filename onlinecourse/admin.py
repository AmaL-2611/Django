from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from .models import Course, Lesson, Question, Choice, Submission, Instructor, Learner


class ChoiceInline(TabularInline):
    model = Choice
    extra = 1


class QuestionInline(StackedInline):
    model = Question
    extra = 1
    show_change_link = True


class QuestionAdmin(ModelAdmin):
    list_display = ('text', 'lesson', 'grade')
    inlines = [ChoiceInline]


class LessonAdmin(ModelAdmin):
    list_display = ('title', 'course')
    inlines = [QuestionInline]


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Submission)
