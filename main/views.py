import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
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

    def form_valid(self, client):
        if client.is_valid():
            new_obj = client.save()
            new_obj.author = self.request.user
            new_obj.save()

        return super().form_valid(client)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    # permission_required = 'catalog.change_product'
    success_url = reverse_lazy('main:client_list')
    template_name = 'main/client/client_form.html'

    def get_success_url(self):
        return reverse('main:client_info', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    # permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('main:client_list')
    template_name = 'main/client/client_confirm_delete.html'


"""CRUD Рассылки"""


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'main/mailing/mailing_list.html'
    # permission_required = 'catalog.view_product'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'main/mailing/mailing_info.html'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    # permission_required = 'catalog.add_product'
    success_url = reverse_lazy('main:mailing_list')
    template_name = 'main/mailing/mailing_form.html'

    def form_valid(self, mailing):
        if mailing.is_valid():
            new_obj = mailing.save()
            new_obj.author = self.request.user
            new_obj.save()

        return super().form_valid(mailing)


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

    def form_valid(self, letter):
        if letter.is_valid():
            new_obj = letter.save()
            new_obj.author = self.request.user
            new_obj.save()

        return super().form_valid(letter)


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

