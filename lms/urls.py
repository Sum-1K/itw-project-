from django.urls import path

from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
   

    path('',views.home,name="home"),

    path('login/',views.login_view,name='login'),

    path('register/',views.register, name='register'),

    path('profile/',views.profile,name='profile'),

    # path('user_profile',views.user_profile,name='user_profile'),

    path('courses/',views.courses,name='courses'),

    path('course_details/<int:course_id>/', views.course_details, name='course_details'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.course_details, name='course_details_lesson'),
    

    path('admin_view/',views.admin_view,name='admin_view'),

    path('home_unregistered/',views.home_unregistered,name='home_unregistered'),

    # path('discussion/',views.discussion,name='discussion'),

    path('student_enrollments/',views.student_enrollments,name='student_enrollments'),

    # path('certificates/',views.certificates,name='certificates'),
     path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
    # path('lesson/<int:lesson_id>/', views.visit_lesson, name='visit_lesson'),
     path('my_courses/', views.my_courses, name='my_courses'),

    path('certificates/',views.certificates,name='certificates'),
    path('certificates/certificate_view/<int:certificate_id>',views.certificate_view,name='certificate_view'),
    path('logout/', views.logout_view, name='logout'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('add_quiz_questions/<int:quiz_id>/', views.add_quiz_questions, name='add_quiz_questions'),
    path('take_quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz_result/<int:quiz_id>/', views.quiz_result, name='quiz_result'),
    path('view_quiz_questions/<int:quiz_id>/',views.view_quiz_questions,name='view_quiz_questions'),
    path('add_quiz_options/<int:question_id>/', views.add_quiz_options, name='add_quiz_options'),

]
