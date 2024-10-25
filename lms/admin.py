# from django.contrib import admin


# from .models import User
# from .models import Notification
# from .models import Enrollment
# from .models import DiscussionForum
# from .models import Course


# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ('username', 'email', 'is_staff', 'is_active', 'user_type','phone_number')
#     list_filter = ('is_staff', 'is_active', 'user_type')
#     search_fields = ('username', 'email')
#     ordering = ('username',)
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )

# admin.site.register(User, CustomUserAdmin)

# # @admin.register(User)
# # class UserAdmin(admin.ModelAdmin):
# #     list_display = ('username', 'email', 'phone_number', 'user_type', 'date_joined')  # Add other fields you want to display
# #     search_fields = ('username', 'email')  # Enable searching by username and email
# #     list_filter = ('user_type',)  # Enable filtering by user_type

# # class NotificationAdmin(admin.ModelAdmin):
#     # list_display = ('user', 'content', 'date_sent', 'is_read', 'course')  # Fields to display in list view
#     # list_filter = ('is_read', 'date_sent', 'course')  # Add filters
#     # search_fields = ('content', 'user__username')  # Enable search functionality

# # admin.site.register(Notification, NotificationAdmin)
# admin.site.register(Notification)
# admin.site.register(Enrollment)
# admin.site.register(DiscussionForum)
# admin.site.register(Course)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,  Enrollment,  Course

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active', 'user_type', 'phone_number')
    list_filter = ('is_staff', 'is_active', 'user_type')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    # Fields to display and edit when viewing or editing a user
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    # Fields to display and edit when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'phone_number', 'first_name', 'last_name', 'profile_picture',
                'user_type', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'
            ),
        }),
    )

admin.site.register(User, CustomUserAdmin)
# admin.site.register(Notification)
admin.site.register(Enrollment)
# admin.site.register(DiscussionForum)
admin.site.register(Course)
