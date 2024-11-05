
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,  Enrollment,  Course,Lesson,Certificate,DiscussionForum,CompletedLesson,Quiz,QuizQuestion,QuizOption,QuizResponse


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active', 'user_type', 'phone_number')
    list_filter = ('is_staff', 'is_active', 'user_type')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )  
 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone_number', 'first_name', 'last_name', 'profile_picture',
                'user_type', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser','groups','user_permissions'
            ),
        }),
    )

admin.site.register(User, CustomUserAdmin)

admin.site.register(Enrollment)
admin.site.register(DiscussionForum)
admin.site.register(Course)

admin.site.register(Lesson)
admin.site.register(Certificate)
admin.site.register(CompletedLesson)
admin.site.register(Quiz)
admin.site.register(QuizResponse)
admin.site.register(QuizQuestion)
admin.site.register(QuizOption)


