from rest_framework import serializers

from .models import Choice, Poll, Vote


class CreateChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text')
        model = Choice


class PollSerializer(serializers.ModelSerializer):
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


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('poll_id', 'choice_id')
        model = Vote


class ChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'text', 'votes_count')
        model = Choice

    def get_votes_count(self, obj):
        return obj.votes.count()


class GetResultSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(read_only=True, many=True)
    total_votes = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'title', 'description', 'total_votes', 'choices')
        model = Poll

    def get_total_votes(self, obj):
        return obj.votes.count()
