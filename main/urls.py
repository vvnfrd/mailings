from django.urls import path
from main.views import ClientListView, ClientDetailView, MailingListView, MailingDetailView, MailingCreateView, \
    MailingUpdateView, MailingDeleteView, ClientCreateView, ClientUpdateView, ClientDeleteView, LetterListView, \
    LetterDetailView, LetterCreateView, LetterUpdateView, LetterDeleteView, send_mailing
from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    #CRUD Рассылок
    path('', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_info'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),

    #CRUD Клиентов
    path('client-list', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_info'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    #CRUD Писем
    path('letter-list', LetterListView.as_view(), name='letter_list'),
    path('letter/<int:pk>/', LetterDetailView.as_view(), name='letter_info'),
    path('letter/create/', LetterCreateView.as_view(), name='letter_create'),
    path('letter/update/<int:pk>/', LetterUpdateView.as_view(), name='letter_update'),
    path('letter/delete/<int:pk>/', LetterDeleteView.as_view(), name='letter_delete'),

    #Включение поштучной рассылки
    path('one-time-mailing/<int:pk>/', send_mailing, name='one_time_mailing'),
]