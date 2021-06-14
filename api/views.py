from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer


class APIPoll(APIView):
    """Создание голосования с вариантами ответов."""
    def post(self, request):
        # many = True?
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIVote(APIView):
    """Голосование за конкретный вариант."""
    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(voter=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
