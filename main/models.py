from django.db import models
from datetime import datetime

NULLABLE = {'blank' : True, 'null' : True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='почта')
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.CharField(max_length=200, verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'Клиент {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Letter(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    body = models.CharField(max_length=500, verbose_name='Текст')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Mailing(models.Model):
    # email = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='почты', **NULLABLE)
    email = models.ManyToManyField(Client, verbose_name='почты')
    """ДОДЕЛАТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
    first_sent = models.DateTimeField(verbose_name='Дата и время будущей отправки')
    next_sent = models.DateTimeField(verbose_name='Дата и время следующей отправки', **NULLABLE)
    periodicity = models.IntegerField(default=7, verbose_name='периодичность')
    status = models.BooleanField(default=False, verbose_name='статус')
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, verbose_name='письмо', **NULLABLE)

    def __str__(self):
        return f'Рассылка {self.first_sent}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

class TryMailing(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка', **NULLABLE)
    last_try = models.DateTimeField(default=datetime.now, verbose_name='дата и время последней попытки')
    status_try = models.BooleanField(default=False, verbose_name='статус попытки')
    answer = models.CharField(max_length=400, **NULLABLE)

    def __str__(self):
        return f'Попытка {self.last_try}'

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'