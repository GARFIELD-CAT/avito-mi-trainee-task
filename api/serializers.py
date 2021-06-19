from rest_framework import serializers

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
    class Meta:
        fields = ('poll_id', 'choice_id')
        model = Vote


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
