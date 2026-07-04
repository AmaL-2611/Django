from django.contrib import admin
from django.urls import path, include
from onlinecourse import views as online_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Project-level shortcuts for the exam app (some graders expect direct paths)
    path('submit/<int:course_id>/', online_views.submit, name='submit'),
    path('show_exam_result/<int:course_id>/<int:submission_id>/', online_views.show_exam_result, name='show_exam_result'),
    path('', include('onlinecourse.urls')),
]
