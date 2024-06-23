# from django.shortcuts import render
import datetime
import time
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config import settings
from main.forms import MailingForm, ClientForm, LetterForm
from main.models import Client, Mailing, Letter

"""CRUD Клиентов"""


class ClientListView(ListView):
    model = Client
    template_name = 'main/client/client_list.html'
    # permission_required = 'catalog.view_product'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'main/client/client_info.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    # permission_required = 'catalog.add_product'
    success_url = reverse_lazy('main:client_list')
    template_name = 'main/client/client_form.html'


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    # permission_required = 'catalog.change_product'
    success_url = reverse_lazy('main:client_list')
    template_name = 'main/client/client_form.html'

    def get_success_url(self):
        return reverse('main:mailing_info', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    # permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('main:client_list')
    template_name = 'main/client/client_confirm_delete.html'


"""CRUD Рассылки"""


class MailingListView(ListView):
    model = Mailing
    template_name = 'main/mailing/mailing_list.html'
    # permission_required = 'catalog.view_product'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'main/mailing/mailing_info.html'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    # permission_required = 'catalog.add_product'
    success_url = reverse_lazy('main:mailing_list')
    template_name = 'main/mailing/mailing_form.html'


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    # permission_required = 'catalog.change_product'
    success_url = reverse_lazy('main:mailing_list')
    template_name = 'main/mailing/mailing_form.html'

    def get_success_url(self):
        return reverse('main:mailing_info', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    # permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('main:mailing_list')
    template_name = 'main/mailing/mailing_confirm_delete.html'


"""CRUD Письма"""


class LetterListView(ListView):
    model = Letter
    template_name = 'main/letter/letter_list.html'
    # permission_required = 'catalog.view_product'


class LetterDetailView(DetailView):
    model = Letter
    template_name = 'main/letter/letter_info.html'


class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterForm
    # permission_required = 'catalog.add_product'
    success_url = reverse_lazy('main:letter_list')
    template_name = 'main/letter/letter_form.html'


class LetterUpdateView(UpdateView):
    model = Letter
    form_class = LetterForm
    # permission_required = 'catalog.change_product'
    success_url = reverse_lazy('main:letter_list')
    template_name = 'main/letter/letter_form.html'

    def get_success_url(self):
        return reverse('main:letter_info', args=[self.kwargs.get('pk')])


class LetterDeleteView(DeleteView):
    model = Letter
    # permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('main:letter_list')
    template_name = 'main/letter/letter_confirm_delete.html'


"""Отправка писем/Рассылка"""


def send_mailing(pk):
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.datetime.now(zone)
    # mailings = Mailing.objects.filter(Q(status='created', first_sent=current_datetime))
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


def start(request, pk):

    # next_sent = first_sent + datetime.timedelta(days=periodicity)
    mailing = get_object_or_404(Mailing, pk=pk)
    periodicity = mailing.periodicity
    first_sent = mailing.first_sent


    scheduler = BackgroundScheduler()
    print(123)
    scheduler.add_job(send_mailing, 'cron', start_date=first_sent, day=periodicity, args=[pk], id=f'job_{pk}')
    scheduler.start()
    mailing.status = 'running'
    mailing.job_id = f'job_{pk}'
    mailing.save()
    return redirect('main:mailing_list')


def stop(request, pk):

    mailing = get_object_or_404(Mailing, pk=pk)
    scheduler = BackgroundScheduler()
    scheduler.pause_job(job_id=f'job_{pk}')
    mailing.status = 'paused'
    mailing.save()
    return redirect(reverse('main:mailing_list'))

