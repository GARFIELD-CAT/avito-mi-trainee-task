from rest_framework import serializers

from .models import Poll, Vote


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('pk', 'title', 'description', 'text')
        models = Poll


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('poll_id', 'choice_id')
        models = Vote
