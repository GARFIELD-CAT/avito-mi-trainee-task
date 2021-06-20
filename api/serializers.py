from typing import List
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Choice, Poll, Vote


class CreateChoiceSerializer(serializers.ModelSerializer):
    """Сериализатор для создания вариантов ответов для голосования."""
    class Meta:
        fields = ('id', 'text')
        model = Choice


class CreatePollSerializer(serializers.ModelSerializer):
    """Сериализатор для создания голосования с вариантами ответов."""
    choices = CreateChoiceSerializer(many=True)

    class Meta:
        fields = ('id', 'title', 'description', 'choices')
        model = Poll

    # Переопределяем метод для создания нескольких вариантов ответа
    # в одном запросе.
    def create(self, validated_data) -> Poll:
        # Из словаря с валидными данными забираем все варианты ответов.
        choices = validated_data.pop('choices')
        # Создаем объект Poll из оставшихся в словаре данных.
        poll: Poll = Poll.objects.create(**validated_data)

        # Создаем объекты Choice.
        for choice in choices:
            Choice.objects.create(poll_id=poll, text=choice['text'])
        return poll


class CreateVoteSerializer(serializers.ModelSerializer):
    """Сериализатор для голосования за один вариант ответа."""
    voter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('poll_id', 'choice_id', 'voter')
        model = Vote
        # Пользователь в каждом голосовании может участвовать только 1 раз.
        validators = [
            UniqueTogetherValidator(
                queryset=Vote.objects.all(),
                fields=['poll_id', 'voter'],
                message='Нельзя проголосовать дважды в одном голосовании.'
            )
        ]

    def validate(self, data):
        """Метод проверяет, чтобы голос был отдан только
        за варианты ответов конкретного голосования.
        """
        # Id возможных вариантов ответа.
        choices_id: List[int] = []
        # Выбранное голосование.
        poll: Poll = data['poll_id']
        # Выбранный вариант ответа.
        choice: Choice = data['choice_id']
        # Выбираем все возможные варианты ответа выбранного голосования.
        poll_choices = poll.choices.all()
        # Если выбранного варианта ответа нет в вариантах нашего голосования,
        # вызываем ошибку.
        if choice not in poll_choices:
            # Получаем id возможных вариантов ответа у голосования.
            for elem in poll_choices:
                choices_id.append(elem.id)
            raise serializers.ValidationError(
                f'Можно голосовать только за варианты ответов '
                f'выбранного голосования. Id возможных вариантов: {choices_id}'
            )
        return data


class GetChoiceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения всех вариантов ответа у конкретного голосования.
    """
    votes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'text', 'votes_count')
        model = Choice

    # Метод помещяет в поле votes_count количество голосов для варианта ответа.
    def get_votes_count(self, obj: Choice) -> int:
        return obj.votes.count()


class GetResultSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации по конкретному голосованию."""
    # В запросе получаем poll_id.
    # Указываем сериализатору где смотреть значение этого поля в Poll.
    poll_id = serializers.PrimaryKeyRelatedField(
        source='id', queryset=Poll.objects.all()
    )
    choices = GetChoiceSerializer(read_only=True, many=True)
    total_votes = serializers.SerializerMethodField()

    class Meta:
        fields = ('poll_id', 'title', 'description', 'total_votes', 'choices')
        model = Poll
        read_only_fields = ('title', 'description')

    # Метод помещяет в поле total_votes количество голосов у голосования.
    def get_total_votes(self, obj: Poll) -> int:
        return obj.votes.count()
