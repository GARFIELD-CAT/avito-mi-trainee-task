from typing import Any
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from .models import Poll, Vote
from .serializers import GetResultSerializer, CreatePollSerializer
from .serializers import CreateVoteSerializer


class PollCreateAPIView(generics.CreateAPIView):
    """Создание голосования с вариантами ответов."""
    queryset = Poll.objects.all()
    serializer_class = CreatePollSerializer

    def perform_create(self, serializer: BaseSerializer[Any]) -> None:
        serializer.save(creator=self.request.user)


class VoteCreateAPIView(generics.CreateAPIView):
    """Голосование за конкретный вариант."""
    queryset = Vote.objects.all()
    serializer_class = CreateVoteSerializer

    def perform_create(self, serializer: BaseSerializer[Any]) -> None:
        serializer.save(voter=self.request.user)


class GetResultAPIView(generics.GenericAPIView):
    """Получение результата по конкретному голосованию."""
    serializer_class = GetResultSerializer

    def post(self, request) -> Response:
        poll_id: int = request.data['poll_id']
        try:
            poll: Poll = get_object_or_404(Poll, id=poll_id)
        except ValueError as error:
            return Response(
                {'message': f'Ошибка - {error}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = GetResultSerializer(poll)
        return Response(serializer.data)
