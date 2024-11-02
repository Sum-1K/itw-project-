# from background_task import background
# from django.utils import timezone
# from .models import Certificate, Course, CompletedLesson  # Adjust based on your actual import paths
# from django.contrib.auth.models import User

# @background(schedule=60)  # Adjust the schedule as necessary (in seconds)
# def generate_certificates():
#     today = timezone.now().date()  # Get today's date
#     courses = Course.objects.filter(end_date__lt=today)  # Get courses past their end date

#     for course in courses:
#         students = User.objects.filter(enrolled_courses=course)  # Get all students in the course

#         for student in students:
#             total_lessons = course.lesson_set.count()  # Total lessons in the course
#             completed_lessons = CompletedLesson.objects.filter(user=student, lesson__course=course).count()  # Completed lessons
#             progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0  # Calculate progress

#             # Check if progress is 100% and a certificate does not already exist
#             if progress == 100 and not Certificate.objects.filter(student=student, course=course).exists():
#                 # Create a certificate record
#                 Certificate.objects.create(
#                     student=student,
#                     course=course,
#                     date_issued=today,
#                 )

# # You may also want to call this task somewhere in your application, such as in your views or on startup
# generate_certificates(repeat=60)  # This will schedule it to run every 60 seconds
from background_task import background
from django.utils import timezone
from .models import Course, Certificate, CompletedLesson,Quiz,QuizResponse,Enrollment
from django.contrib.auth.models import User

@background(schedule=0)  # Run every 24 hours (86400 seconds)
def generate_certificates():
    print("function called")
    today = timezone.now().date() 
    students_with_full_progress = Enrollment.objects.filter(
    progress=100,
    course__end_date__lt=today
    ).select_related('user')
    for enrollment in students_with_full_progress:
        student_name = f"{enrollment.user.first_name} {enrollment.user.last_name}"
        

        # Create a certificate record
        if not Certificate.objects.filter(student=enrollment.user,course=enrollment.course).exists():
            print("student name is: ",student_name)
            Certificate.objects.create(
                student=enrollment.user,
                course=enrollment.course,
                date_issued=today,
            )
            Certificate.save()

    # python manage.py process_tasks
    

    