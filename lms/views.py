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
from .models import Enrollment, User,Lesson
from .models import Course



def home(request):
     return render(request,'home.html')

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

       
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             if user.is_active:
#                 auth_login(request, user)
#                 messages.success(request, "Login successful!")
#                 return redirect('home')  # Adjust the 'home' URL to where you want to redirect after login
#             else:
#                 messages.error(request, "This account is inactive.")
#         else:
#             messages.error(request, "Invalid username or password.")

#     return render(request, 'login.html')
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             # Log the user in
#             auth_login(request, user)
#             return redirect('home')  # Redirect to your home page or dashboard
#         else:
#             # Invalid login credentials
#             messages.error(request, "Invalid username or password")
#             return render(request, 'login.html')
    
#     return render(request, 'login.html')
# def login(request):
    # if request.method == "POST":
    #     form = AuthenticationForm(request, data=request.POST)
    #     if form.is_valid():
    #         user = form.get_user()
    #         auth_login(request, user)
    #         return redirect('home')
    #     else:
    #         messages.error(request, "Invalid username or password.")
            
    
    # form = AuthenticationForm()
    # return render(request, 'login.html', {'form': form})
    
    
def login_view(request):
    if request.method == 'POST':
        print("Form submitted")  # Check if form is submitted

        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        

                

    #     if not (username and password):
    #         print("here")
    #         messages.error(request, 'Please fill all fields.')
    #         return render(request, 'login.html')

    #     try:
    #         user=User.objects.all()
       
    #         for u in user:
    #             if u.username==username and u.password==password:
    #                 print("person found")
    #                 return redirect('home')
    #         print('invalid username or password')
            

           
 

    #     except Exception as e:
    #         messages.error(request, f'An error occurred: {str(e)}')
    #         print("Error:", str(e))  # Catch any unexpected errors

    # return render(request, 'login.html')
    
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
               
                

                # Create the Patient record and link it to the user
                user = User.objects.create(
                      # Link to CustomUser
                    phone_number=phone_number,
                    email=email ,
                    username=username,
                    user_type='student',
                    first_name=first_name,
                    last_name=last_name,
                    password=make_password(password)
                    # Assuming Patient model has this field

                )
                print(user.password)

                print("student record created successfully")
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')  # Redirect to the home page after successful registration

        except Exception as e:
            # Log the error to help with debugging
            print("Error occurred during registration:", str(e))
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'register.html')

    # Render the form initially or in case of an error
    return render(request, 'register.html')

        
    #     try:
    #         user = User(
    #             first_name=first_name,
    #             last_name=last_name,
    #             username=username,
    #             # password=password,
    #             email=email,
    #             phone_number=phone_number,
    #             user_type='student'
                 
                
                
              
    #         )
    #         user.password = make_password(password) 
    #         user.save()
    #         messages.success(request, "Registration successful!")
    #         return redirect('login')  # Redirect to the login page after successful registration
    #     except ValidationError as e:
    #         messages.error(request, f"Error: {str(e)}")

    # return render(request, 'register.html')


# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # username=form.cleaned_data.get('username')
#             messages.success(request, "Registration successful!")
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})
    
def courses(request):
     courses=Course.objects.all()

     return render(request,'courses.html',{'courses':courses})

@login_required
def profile(request):
     return render(request,'profile.html')

# @login_required
# def user_profile(request):
#     user = request.user
#     enrollments = Enrollment.objects.filter(user=user)
#     certificates = Certificate.objects.filter(student=user)
#     notifications = Notification.objects.filter(user=user, is_read=False)

#     # Calculate overall progress
#     overall_progress = enrollments.aggregate(Avg('progress'))['progress__avg'] or 0

#     context = {
#         'user': user,
#         'enrollments': enrollments,
#         'certificates': certificates,
#         'notifications': notifications,
#         'overall_progress': overall_progress,
#     }
    
#     return render(request, 'user_profile.html', context)

def admin_view(request):
     return render(request,'admin_view.html')


@login_required
def course_details(request,course_id):
    print("view called")
     
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('position')  # Order by position
    initial_lesson = lessons.first()  # Default to the first lesson based on position
    print("reached halfway")
    return render(request, 'course_detail.html', {
        'course': course,
        'lessons': lessons,
        'initial_lesson': initial_lesson,
    })
     
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
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        # Enrollment was successful
        messages.success(request, "You have successfully enrolled in the course!")
    else:
        # User is already enrolled
        messages.info(request, "You are already enrolled in this course.")

    return redirect('home')

@login_required
def visit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=lesson.course)

    # Update progress
    total_lessons = lesson.course.lesson_set.count()
    visited_lessons = enrollment.progress * total_lessons  # Assuming progress is a float value (0.0 to 1.0)
    
    # Increment visited lessons count
    visited_lessons += 1

    # Calculate new progress
    new_progress = visited_lessons / total_lessons
    enrollment.progress = new_progress
    enrollment.save()

    return render(request, 'lesson_detail.html', {'lesson': lesson, 'enrollment': enrollment})

def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'my_courses.html', {'enrollments': enrollments})