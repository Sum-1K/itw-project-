# tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Enrollment, Course, QuizResponse, CompletedLesson, Certificate, Lesson, Quiz

@shared_task
def issue_certificates():
    today = timezone.now().date()
    enrollments = Enrollment.objects.all()

    for enrollment in enrollments:
        course = enrollment.course
        user = enrollment.user

        # Check if the course has ended
        if course.end_date == today:
            # Calculate progress
            total_lessons = Lesson.objects.filter(course=course).count()
            total_quizzes = Quiz.objects.filter(course=course).count()
            completed_lessons = CompletedLesson.objects.filter(user=user, lesson__course=course).count()
            completed_quizzes = (
                QuizResponse.objects
                .filter(student=user, question__quiz__course=course)
                .values('question__quiz')
                .distinct()
                .count()
            )

            # Check if progress is 100%
            if total_lessons + total_quizzes > 0:
                progress_percentage = ((completed_lessons + completed_quizzes) / (total_lessons + total_quizzes)) * 100
                if progress_percentage == 100:
                    # Issue certificate if it does not already exist
                    if not Certificate.objects.filter(student=user, course=course).exists():
                        Certificate.objects.create(
                            student=user,
                            course=course,
                            date_issued=today,
                            certificate_url=f'/certificates/{user.id}/{course.id}/'
                        )
