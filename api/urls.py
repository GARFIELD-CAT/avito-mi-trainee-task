from django.urls import path

from .views import GetResultAPIView, PollCreateAPIView, VoteCreateAPIView

urlpatterns = [
    path('v1/createPoll/', PollCreateAPIView.as_view(), name='create-poll'),
    path('v1/poll/', VoteCreateAPIView.as_view(), name='poll'),
    path('v1/getResult/', GetResultAPIView.as_view(), name='get-result-poll'),
]
