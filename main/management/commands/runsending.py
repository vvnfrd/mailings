
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
# from django_apscheduler import util


def my_job():
    print('test_run')


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute="*/1"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )

        try:
            print('start sending')
            scheduler.start()
        except KeyboardInterrupt:
            print("stop sending")
            scheduler.shutdown()
            print("sending shut down successfully!")
