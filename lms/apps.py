
from django.apps import AppConfig

from django.db.utils import OperationalError, ProgrammingError

class LmsConfig(AppConfig):
    name = 'lms'

    def ready(self):
        try:
           
            self.schedule_generate_certificates()
        except (OperationalError, ProgrammingError):
           
            pass

    def schedule_generate_certificates(self):
 
        from .tasks import generate_certificates
        generate_certificates(repeat=10) 
