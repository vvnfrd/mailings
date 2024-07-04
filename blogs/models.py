from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    text = models.TextField(max_length=1000, verbose_name='текст')
    image = models.ImageField(upload_to='materials/', verbose_name='изображение продукта', **NULLABLE)
    views_counter = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')
    create_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'