# from django.apps import AppConfig

# class LmsConfig(AppConfig):
#     name = 'lms'

#     def ready(self):
#         # Import the task function here to prevent circular import issues
#         from .tasks import generate_certificates
#         generate_certificates()  # Schedule the task
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db.utils import OperationalError, ProgrammingError

class LmsConfig(AppConfig):
    name = 'lms'

    def ready(self):
        try:
            # Schedule the task if it hasn't been scheduled already
            self.schedule_generate_certificates()
        except (OperationalError, ProgrammingError):
            # Handle the case where database tables aren't ready (like during migration setup)
            pass

    def schedule_generate_certificates(self):
    # This function will be called after migrations are done
        from .tasks import generate_certificates
        generate_certificates(repeat=10)  # Schedule the task here
