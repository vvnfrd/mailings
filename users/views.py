from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.core.mail import send_mail
from users.forms import UserRegisterForm, UserProfileForm, UserFormForManager
from users.models import User
from config import settings
import secrets

"""Сервис пользователя"""


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        token = secrets.token_hex(16)
        user.token = token
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            'Подтверждение регистрации',
            f'Для подтверждения регистрации перейдите по ссылке {url}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('main:mailing_list')

    def get_object(self, queryset=None):
        return self.request.user


"""Сервис менеджера"""


class UserListView(ListView):
    model = User


class UserDetailView(DetailView):
    model = User


class UserUpdateView(UpdateView):
    model = User
    form_class = UserFormForManager
    success_url = reverse_lazy('users:user_list')
    template_name = 'manager/user_form.html'

    def get_success_url(self):
        return reverse('users:user_info', args=[self.kwargs.get('pk')])
