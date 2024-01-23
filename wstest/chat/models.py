from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, verbose_name='Имя пользователя', unique=True, error_messages={'unique': "Пользователь с таким именем уже "
                                                        "зарегистрирован"})
    password = models.CharField(max_length=255, verbose_name='Пароль')
    email = models.EmailField(unique=True, verbose_name='Почта',
                              error_messages={'unique': "Пользователь с таким адресом электронной почты уже "
                                                        "зарегистрирован"})

    registration_time = models.DateTimeField('Дата регистрации', auto_now_add=True)

class BoardRoom(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    main_position = models.CharField(max_length=100, verbose_name='Позиция', default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')

    class Types(models.TextChoices):
        PUBLIC = 'Публичная', 'Присоединиться может кто угодно'
        PRIVATE = 'Приватная', 'Для присоединения необходимо разрешение администратора'

    type = models.TextField(choices=Types.choices, verbose_name='Тип', default=Types.PUBLIC)

    class Statuses(models.TextChoices):
        ONLINE = 'Онлайн', 'Один или несколько администраторов в сети'
        OFFLINE = 'Офлайн', 'В сети нет ни одного администратора'

    status = models.TextField(choices=Statuses.choices, verbose_name='Статус', default=Statuses.ONLINE)
    admin = models.ForeignKey(CustomUser, verbose_name='Администратор', on_delete=models.CASCADE)
    creation_time = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return  self.name

    def get_absolute_url(self):
        return reverse('board', kwargs={'board_name': self.name})

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'




