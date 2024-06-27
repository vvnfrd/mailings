from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import path, reverse_lazy
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>', email_verification, name='email-confirm'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html',
                                                        email_template_name='users/password_reset_email.html',
                                                      success_url=reverse_lazy('users:password_reset_done')),
                                                        name='password_reset'),
    path('password-reset/done/', PasswordResetView.as_view(template_name='users/password_reset_done.html'),
                                                        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                                              success_url=reverse_lazy('users:login')), name='password_reset_confirm')
]