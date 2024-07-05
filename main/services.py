from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from main.models import Mailing, Letter


def send_mailing(request, pk):
    print(request)
    mailings = Mailing.objects.get(pk=pk)
    letter_pk = mailings.letter_id
    clients = mailings.email.all()
    email_list = []
    for i in clients:
        print(i.email)
        email_list.append(i.email)

    send_mail(
            subject=Letter.objects.get(pk=letter_pk).title,
            message=Letter.objects.get(pk=letter_pk).body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list
    )
    return HttpResponseRedirect(reverse_lazy('main:mailing_list'))