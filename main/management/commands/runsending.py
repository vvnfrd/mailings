import pytz
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from main.models import Mailing, Letter
from datetime import datetime, timedelta


# from django_apscheduler.models import DjangoJobExecution
# from django_apscheduler import util


def my_job():

    for mailing in Mailing.objects.filter(status=True):
        zone = pytz.timezone(settings.TIME_ZONE)
        send_date = datetime.strftime(mailing.first_sent, '%Y-%m-%d %H:%M:%S')
        now_date = datetime.strftime(datetime.now(zone), '%Y-%m-%d %H:%M:%S')
        print(send_date, now_date)
        if send_date <= now_date:
            clients = mailing.email.all()
            email_list = []
            for i in clients:
                email_list.append(i.email)
            send_mail(
                subject=Letter.objects.get(pk=mailing.letter_id).title,
                message=Letter.objects.get(pk=mailing.letter_id).body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=email_list
            )
            mailing.first_sent += timedelta(days=mailing.periodicity)
            mailing.save()


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
