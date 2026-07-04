from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seed the database with a sample course, lessons, questions and choices.'

    def handle(self, *args, **options):
        from onlinecourse.models import Course, Lesson, Question, Choice

        if Course.objects.filter(title='Sample Course').exists():
            self.stdout.write('Sample data already present.')
            return

        course = Course.objects.create(title='Sample Course', description='A sample course created by seed script')

        lesson1 = Lesson.objects.create(course=course, title='Lesson 1', content='Content for lesson 1')
        lesson2 = Lesson.objects.create(course=course, title='Lesson 2', content='Content for lesson 2')

        q1 = Question.objects.create(lesson=lesson1, text='What is 2 + 2?', grade=1)
        Choice.objects.create(question=q1, text='3', is_correct=False)
        Choice.objects.create(question=q1, text='4', is_correct=True)

        q2 = Question.objects.create(lesson=lesson1, text='What is the capital of France?', grade=1)
        Choice.objects.create(question=q2, text='Berlin', is_correct=False)
        Choice.objects.create(question=q2, text='Paris', is_correct=True)

        q3 = Question.objects.create(lesson=lesson2, text='Select the correct statement', grade=2)
        Choice.objects.create(question=q3, text='Sun rises in the west', is_correct=False)
        Choice.objects.create(question=q3, text='Sun rises in the east', is_correct=True)

        self.stdout.write(self.style.SUCCESS('Sample course and questions created.'))
