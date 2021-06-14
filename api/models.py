from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Poll(models.Model):
    """Голосование с вариантами ответов."""
    title = models.CharField(
        verbose_name='Название голосования',
        max_length=200,
        help_text='Заполните название голосования',
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание голосования',
        blank=True,
        help_text='Заполните описание голосования'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='polls',
        help_text='Организатор голосования выбирается автоматически',
        verbose_name='Организатор голосования'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        help_text='Дата заполняется автоматически'
    )
    active = models.BooleanField(
        verbose_name='Активность голосования',
        default=True,
        help_text='Выберите активно ли голосование'
    )

    def __str__(self):
        return self.title

