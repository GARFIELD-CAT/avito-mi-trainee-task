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


class Choice(models.Model):
    """Вариант ответа."""
    poll_id = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='choices',
        help_text='Выберите голосование',
        verbose_name='Голосование'
    )
    text = models.CharField(
        verbose_name='Вариант ответа',
        max_length=255,
        help_text='Заполните текст ответа',
        unique=True
    )

    def __str__(self):
        return self.text


class Vote(models.Model):
    """Голос избирателя."""
    voter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='votes',
        help_text='Избиратель выбирается автоматически',
        verbose_name='Избиратель'
    )
    poll_id = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='votes',
        help_text='Выберите голосование',
        verbose_name='Голосование'
    )
    choice_id = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        help_text='Выберите вариант ответа',
        verbose_name='Вариант ответа'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['voter', 'poll_id'],
                name='unique_vote'
            )
        ]
