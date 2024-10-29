from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.contrib.auth import get_user_model
from django.db import transaction
# from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
import re
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Enrollment, User,Lesson,Certificate
from .models import Course,CompletedLesson
from django.contrib.auth import logout




def home(request):
     return render(request,'home.html')

    
def login_view(request):
    if request.method == 'POST':
        print("Form submitted")  # Check if form is submitted

        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        


    
        if not (username and password):
            messages.error(request, 'Please fill all fields.')
            return render(request, 'login.html')

        # Use authenticate to check credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')



def register(request):
    if request.method == "POST":
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        
        
        
       

        # Validation: Check if all fields are filled
        if not all([first_name,username,password,confirm_password, email, phone_number]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'register.html')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return render(request, 'register.html')

        if not re.match(r'^\d{10}$', phone_number):
            messages.error(request, "Phone number must be 10 digits.")
            return render(request, 'register.html')

        # Validation: Check if password and confirm_password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Validation: Check if email or phone_number is unique
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return render(request, 'register.html')

        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number is already registered.")
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return render(request, 'register.html')

        # Validation passed: Save the user
        # hashed_password = make_password(password)

        
        try:
            with transaction.atomic():  # Ensure atomic transaction
                # Create the CustomUser
                print("Creating user...")
               
                


                user = User.objects.create(
                      # Link to CustomUser
                    phone_number=phone_number,
                    email=email ,
                    username=username,
                    user_type='student',
                    first_name=first_name,
                    last_name=last_name,
                    password=make_password(password)
  

                )
                print(user.password)

                print("student record created successfully")
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')  # Redirect to the home page after successful registration

        except Exception as e:
   
            print("Error occurred during registration:", str(e))
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'register.html')

    return render(request, 'register.html')

        

    
def courses(request):
    
    all_courses = Course.objects.all()
    
    if request.user.is_authenticated:
        enrolled_courses = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
        available_courses = [course for course in all_courses if course.course_id not in enrolled_courses]
    else:
        # If user is not authenticated, show all courses
        available_courses = all_courses
    
    return render(request, 'courses.html', {'courses': available_courses})

@login_required
def profile(request):
     return render(request,'profile.html')


def admin_view(request):
     return render(request,'admin_view.html')





def course_details(request, course_id,lesson_id=None):
    print(course_id)
    print(lesson_id)
    course = Course.objects.get(course_id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('position')

    if lesson_id is None and lessons.exists():
        initial_lesson = lessons.first()
    else:
        initial_lesson = get_object_or_404(Lesson, lesson_id=lesson_id)

    # Mark the lesson as completed when it is loaded
    if request.user.is_authenticated:
        CompletedLesson.objects.get_or_create(user=request.user, lesson=initial_lesson)
    context = {
        'course': course,
        'lessons': lessons,
        'initial_lesson': initial_lesson,
    }
    return render(request, 'course_details.html', context)

def home_unregistered(request):
     return render(request,'home_unregistered.html')


@login_required
# def discussion(request):
   
#     return render(request,'discussion.html')

def student_enrollments(request):
    return render(request,'student_enrollments.html')

# def certificates(request):
#     return render(request,'certificates.html')


@login_required
def enroll_in_course(request, course_id):
    print(course_id)
    
    course = get_object_or_404(Course, course_id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        # Enrollment was successful
        messages.success(request, "You have successfully enrolled in the course!")
    else:
        # User is already enrolled
        messages.info(request, "You are already enrolled in this course.")

    return redirect('course_details', course_id=course_id)





def my_courses(request):
    # enrollments = Enrollment.objects.filter(user=request.user)
    # print("i am here")
    
    # for x in enrollments:
    #     print("values printing")
    #     print(x.user.first_name)
    # return render(request, 'my_courses.html', {'enrollments': enrollments})
    enrollments = Enrollment.objects.filter(user=request.user)
    progress_data = []
   

    for enrollment in enrollments:
       
        course = enrollment.course
        
        total_lessons=Lesson.objects.filter(course=course).count()
        # total_lessons = course.lessons.count()  
        completed_lessons = CompletedLesson.objects.filter(user=request.user, lesson__course=course).count()

        
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

        
        progress_data.append({
            'course': course,
            'progress_percentage': progress_percentage,
        })

    return render(request, 'my_courses.html', {'progress_data': progress_data})


@login_required
def certificates(request):
    certificate=Certificate.objects.filter(student=request.user)
    has_certificates=certificate.exists()
    context={
        'certificates':certificate,
        'has_certificates':has_certificates

    }
    return render(request,'certificates.html',context)

@login_required
def certificate_view(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id, student=request.user)

    context = {
        'certificate': certificate  # Pass the single certificate object
    }
    
    #certificate=get_object_or_404(Certificate, certificate_id=certificate_id)
    #cert = Certificate.objects.get(certificate_id=certificate_id)
    return render(request,'index.html',context)

def logout_view(request):
    logout(request)
    return redirect('home') 

def mark_lesson_completed(user, lesson):
    CompletedLesson.objects.get_or_create(user=user, lesson=lesson)