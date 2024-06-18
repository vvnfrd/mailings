from django.db import models
from datetime import datetime

NULLABLE = {'blank' : True, 'null' : True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='почта')
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.CharField(max_length=200, **NULLABLE)

    def __str__(self):
        return f'Клиент {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    first_sent = models.DateTimeField(default=datetime.now)
    periodicity = models.IntegerField(default=7, verbose_name='периодичность')
    status = models.CharField(default='created', max_length=30, verbose_name='статус')

    def __str__(self):
        return f'Рассылка {self.first_sent}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Letter(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=500)

    def __str__(self):
        return f'Письмо {self.title}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class TryMailing(models.Model):
    last_try = models.DateTimeField(default=datetime.now, verbose_name='дата и время последней попытки')
    status_try = models.BooleanField(default=False, verbose_name='статус попытки')
    answer = models.CharField(max_length=400, **NULLABLE)

    def __str__(self):
        return f'Попытка {self.last_try}'

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'