
from background_task import background
from django.utils import timezone
from .models import Course, Certificate, CompletedLesson,Quiz,QuizResponse,Enrollment


@background(schedule=0)  
def generate_certificates():
    print("function called")
    today = timezone.now().date() 
    students_with_full_progress = Enrollment.objects.filter(
    progress=100,
    course__end_date__lt=today
    ).select_related('user')
    for enrollment in students_with_full_progress:
        student_name = f"{enrollment.user.first_name} {enrollment.user.last_name}"
        

        
        if not Certificate.objects.filter(student=enrollment.user,course=enrollment.course).exists():
            print("student name is: ",student_name)
            Certificate.objects.create(
                student=enrollment.user,
                course=enrollment.course,
                date_issued=today,
            )
            Certificate.save()

    # python manage.py process_tasks
    

    