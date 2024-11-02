from django.apps import AppConfig
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class LmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms'
    def ready(self):
        from django.db.utils import OperationalError, ProgrammingError
        
        try:
            # Ensure task creation only after migrations are complete
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.DAYS,
            )

            PeriodicTask.objects.get_or_create(
                interval=schedule,
                name='Daily certificate issuance task',
                task='lms.tasks.issue_certificates',
            )
        except (OperationalError, ProgrammingError):
            # These errors may occur if the database is not initialized yet
            pass
