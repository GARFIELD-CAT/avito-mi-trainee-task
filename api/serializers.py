from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Poll, Vote


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('pk', 'title', 'description', 'text')
        models = Poll


