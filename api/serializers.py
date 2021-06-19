from rest_framework import serializers

from .models import Choice, Poll, Vote


class CreateChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text')
        model = Choice


class CreatePollSerializer(serializers.ModelSerializer):
    choices = CreateChoiceSerializer(many=True)

    class Meta:
        fields = ('id', 'title', 'description', 'choices')
        model = Poll

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data)

        for choice in choices:
            Choice.objects.create(poll_id=poll, text=choice['text'])
        return poll


class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('poll_id', 'choice_id')
        model = Vote


class GetChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'text', 'votes_count')
        model = Choice

    def get_votes_count(self, obj):
        return obj.votes.count()


class GetResultSerializer(serializers.ModelSerializer):
    poll_id = serializers.PrimaryKeyRelatedField(
        source='id', queryset=Poll.objects.all()
    )
    choices = GetChoiceSerializer(read_only=True, many=True)
    total_votes = serializers.SerializerMethodField()

    class Meta:
        fields = ('poll_id', 'title', 'description', 'total_votes', 'choices')
        model = Poll
        read_only_fields = ('title', 'description')

    def get_total_votes(self, obj):
        return obj.votes.count()
